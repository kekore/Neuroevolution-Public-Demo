from neuroevolution.config import Config
from neuroevolution.population import Population
from neuroevolution.species import Species
from neuroevolution.node_gene import NodeGene
from neuroevolution.reproduction import Reproducer
from neuroevolution.genome import Genome
from neuroevolution.testing import TestCluster
from neuroevolution.util import LogUtil, CsvUtil
from collections import deque
from time import time
from typing import List, Tuple, Union, Set
import pickle


class Neuroevolution:
    def __init__(self, config: Config):
        self.config: Config = config

        self.current_population: Union[None, Population] = None
        self.species: List[Species] = []
        self.next_species_identifier: int = 0

        self.global_links_matrix: Set[Tuple[NodeGene, NodeGene]] = set()

        self.next_node_identifier: int = 0
        self.current_iteration: int = -1
        self.reproducer: Reproducer = Reproducer(self)
        self.allow_new_species = None

        self.in_progress: bool = False

        self.best_genome = None

    def proceed(self):
        test_cluster = TestCluster(self.config.network_ctrler_cls, self.config.problem_ctrler_cls,
                                   self.config.test_processes)
        # initialize
        if not self.in_progress:
            self.initialize()
            self.in_progress = True

        while self.current_iteration < self.config.max_iterations and \
                (self.best_genome is None or self.config.fitness_target is None or
                 self.best_genome.fitness < self.config.fitness_target):
            iteration_start_time = time()
            self.current_iteration += 1

            self.assign_to_species()
            self.test_current_population(test_cluster)

            if self.config.save_csv:
                CsvUtil.proceed(self)

            self.evaluate_results()
            self.current_population = self.reproducer.create_next_population()

            LogUtil.proceed(self, self.config.save_logs)

            print("Iteration time: " + str(time() - iteration_start_time))
            if self.config.save_progress:
                self.save_progress()

        test_cluster.close()
        return self.best_genome

    def initialize(self):
        input_genes = []
        for input_index in range(self.config.input_size):
            input_genes.append(NodeGene.get_input(self.get_next_node_identifier()))
        if self.config.has_bias_neuron:
            input_genes.append(NodeGene.get_bias(self.get_next_node_identifier()))
        output_genes = []
        for output_index in range(self.config.output_size):
            output_genes.append(NodeGene.get_output(self.get_next_node_identifier(), self.config.output_function))

        genome_list: List[Genome] = []
        # get random genomes
        for g in range(self.config.offspring_quantity):
            new_random_genome = Genome.get_random_genome(self, input_genes, output_genes)
            genome_list.append(new_random_genome)

        self.current_population = Population(genome_list)

    def assign_to_species(self):
        for species in self.species:
            species.genomes = []
        for survivor in self.current_population.survivors:
            survivor.species.genomes.append(survivor)
        for genome in self.current_population.new_genomes:
            self.assign_genome_to_species(genome)

        # add some similar copies to new species
        for species in self.species:
            if len(species.genomes) == 1:
                for copy_index in range(self.config.new_species_clones_amount):
                    new_similar_genome = species.genomes[0].get_random_similar(self)
                    self.current_population.new_genomes.append(new_similar_genome)
                    self.assign_genome_to_species(new_similar_genome)

    def evaluate_results(self):
        species_index = 0
        while species_index < len(self.species):
            self.species[species_index].evaluate()
            if self.best_genome is None or (self.species[species_index].best_genome is not None and
                                            self.species[species_index].best_genome.fitness is not None and
                                            self.species[
                                                    species_index].best_genome.fitness > self.best_genome.fitness):
                self.best_genome = self.species[species_index].best_genome

            # delete species if went stagnating
            if self.config.stagnation_limit is not None and \
                    self.species[species_index].no_improvement_iterations >= self.config.stagnation_limit and \
                    len(self.species) > 1:
                del self.species[species_index]
            else:
                species_index += 1

        if len(self.species) >= self.config.max_existing_species:
            self.allow_new_species = False
        else:
            self.allow_new_species = True

    def add_or_check_link(self, outgoing_node: NodeGene, ingoing_node: NodeGene):
        if (not self.config.allow_recurrent) and self.check_recursion(outgoing_node, ingoing_node):
            return False
        if (outgoing_node, ingoing_node) not in self.global_links_matrix:
            self.global_links_matrix.add((outgoing_node, ingoing_node))
        return True

    def assign_genome_to_species(self, genome: Genome):
        # check if genome matches any existing species
        for species in self.species:
            if species.does_match(genome):
                species.genomes.append(genome)
                genome.species = species
                return
        # if not - create new species and assign this genome to it
        new_species = Species(self.get_next_species_identifier(), genome.nodes_genome)
        self.species.append(new_species)
        new_species.genomes.append(genome)
        genome.species = new_species

    def get_next_node_identifier(self):
        identifier = self.next_node_identifier
        self.next_node_identifier += 1
        return identifier

    def get_next_species_identifier(self):
        name = self.next_species_identifier
        self.next_species_identifier += 1
        return name

    def check_recursion(self, outgoing_node: NodeGene, ingoing_node: NodeGene) -> bool:
        """Checks if potential new link would make the "full graph" recurrent"""
        if outgoing_node == ingoing_node:
            return True

        checked = []
        queue = deque([ingoing_node])

        while queue:
            if (queue[0], outgoing_node) in self.global_links_matrix:
                return True
            for link in self.global_links_matrix:
                if link[0] == queue[0]:
                    if ((queue[0], link[1]) in self.global_links_matrix) and (link[1] not in checked):
                        queue.append(link[1])
            checked.append(queue.popleft())

        return False

    def test_current_population(self, test_cluster):
        print("TESTING GENERATION " + str(self.current_iteration))
        test_cluster.perform_tests(self.current_population.new_genomes)
        print("TESTING DONE")

    def save_progress(self):
        self.save_alg()
        best_genome_file_name = "bestGenome" + str(id(self)) + ".pkl"
        self.best_genome.save(best_genome_file_name)

    def save_alg(self):
        file_name = "nev" + str(id(self)) + ".pkl"
        with open(file_name, 'wb') as output:
            pickle.dump(self, output,
                        pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def load_alg(file_name: str):
        with open(file_name, 'rb') as inp:
            return pickle.load(inp)
