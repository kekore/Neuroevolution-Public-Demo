from neuroevolution.nodes_genome import NodesGenome
from neuroevolution.links_genome import LinksGenome
from neuroevolution.node_gene import NodeGene
from neuroevolution.link_gene import LinkGene
from copy import copy
from typing import List, Union, Tuple
import random
import pickle


class Genome:
    def __init__(self, nodes_genome: NodesGenome, links_genome: LinksGenome):
        self.nodes_genome: NodesGenome = nodes_genome
        self.links_genome: LinksGenome = links_genome
        self.fitness: Union[None, float] = None
        self.species = None

    def get_possible_new_links(self) -> List[Tuple[NodeGene, NodeGene]]:
        possible_links: List[Tuple[NodeGene, NodeGene]] = []

        for outgoing_node in self.nodes_genome.input_genes + self.nodes_genome.hidden_genes:
            for ingoing_node in self.nodes_genome.hidden_genes + self.nodes_genome.output_genes:
                # if it would be a duplicate - skip it
                if self.links_genome.link_genes.get((outgoing_node, ingoing_node)) is not None:
                    continue
                if self.nodes_genome.is_link_possible(outgoing_node, ingoing_node):
                    possible_links.append((outgoing_node, ingoing_node))

        return possible_links

    def get_random_similar(self, neuroevolution_instance):
        nodes_genome_copy = copy(self.nodes_genome)
        links_genome_copy = self.links_genome.get_copy()
        for link_gene in links_genome_copy.link_genes.values():
            link_gene.weight = random.uniform(neuroevolution_instance.config.weight_interval[0], neuroevolution_instance.config.weight_interval[1])
        return Genome(nodes_genome_copy, links_genome_copy)

    @classmethod
    def get_random_genome(cls, neuroevolution_instance, input_genes: List[NodeGene], output_genes: List[NodeGene]):
        # create nodes genome
        nodes_genome: NodesGenome = NodesGenome()
        nodes_genome.input_genes = input_genes
        nodes_genome.output_genes = output_genes

        # create links genome
        links_genome: LinksGenome = LinksGenome()
        for input_gene in nodes_genome.input_genes:
            for output_gene in nodes_genome.output_genes:
                if random.random() < neuroevolution_instance.config.init_connection_prob:
                    neuroevolution_instance.add_or_check_link(input_gene, output_gene)
                    weight_interval = neuroevolution_instance.config.weight_interval
                    weight = random.uniform(weight_interval[0], weight_interval[1])
                    link_gene = LinkGene(input_gene, output_gene, weight, False)
                    links_genome.add_gene(link_gene)

        # prevent genome with 0 links (empty network with no single link)
        if len(links_genome.link_genes) == 0:
            input_gene = random.choice(nodes_genome.input_genes)
            output_gene = random.choice(nodes_genome.output_genes)
            neuroevolution_instance.add_or_check_link(input_gene, output_gene)
            weight_interval = neuroevolution_instance.config.weight_interval
            weight = random.uniform(weight_interval[0], weight_interval[1])
            link_gene = LinkGene(input_gene, output_gene, weight, False)
            links_genome.add_gene(link_gene)

        return cls(nodes_genome, links_genome)

    def save(self, file_name: Union[str, None] = None):
        if file_name is None:
            file_name = "genome" + str(id(self)) + ".pkl"
        with open(file_name, 'wb') as otp:
            pickle.dump(self, otp, pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def load(file_name: str):
        with open(file_name, 'rb') as inp:
            return pickle.load(inp)

    def __str__(self):
        string = "Individual [ " + str(id(self)) + " ]\n"
        if self.fitness is None:
            string += "Fitness: Not tested\n"
        else:
            string += "Fitness: <" + str(self.fitness) + ">\n"
        string += "Species identifier: { " + str(self.species.identifier) + " }\n"
        string += self.nodes_genome.__str__() + "\n"
        string += self.links_genome.__str__()
        return string
