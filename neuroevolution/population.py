from neuroevolution.genome import Genome
from typing import List


class Population:
    def __init__(self, genome_list: List[Genome], survivors: List[Genome] = None):
        self.new_genomes: List[Genome] = genome_list
        if survivors is None:
            self.survivors: List[Genome] = []
        else:
            self.survivors: List[Genome] = survivors

    def get_population_real_size(self):
        return len(self.survivors) + len(self.new_genomes)

    def get_fitness_list(self) -> List[float]:
        all_fitnesses = []
        for genome in self.survivors + self.new_genomes:
            all_fitnesses.append(genome.fitness)
        return all_fitnesses
