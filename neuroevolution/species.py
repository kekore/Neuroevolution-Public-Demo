from neuroevolution.nodes_genome import NodesGenome
from neuroevolution.genome import Genome
from typing import List, Union


class Species:
    def __init__(self, identifier: int, representative_nodes_genome: NodesGenome):
        self.identifier: int = identifier
        self.representative_nodes_genome: NodesGenome = representative_nodes_genome
        self.genomes: List[Genome] = []
        self.best_genome: Union[None, Genome] = None
        self.recent_improvement: Union[None, float] = None
        self.no_improvement_iterations: int = 0

    def does_match(self, genome: Genome) -> bool:
        return self.representative_nodes_genome.is_same(genome.nodes_genome)

    def evaluate(self):
        # sort
        self.genomes.sort(key=lambda genome: genome.fitness, reverse=True)
        # update best genome if new appeared and update recent improvement
        if self.best_genome is None:
            self.best_genome = self.genomes[0]
        elif self.genomes[0].fitness > self.best_genome.fitness:
            previous_best = self.best_genome.fitness
            self.best_genome = self.genomes[0]
            self.recent_improvement = self.best_genome.fitness - previous_best
        else:
            self.recent_improvement = 0.0
        # update no improvement iterations in row
        if self.recent_improvement is None or self.recent_improvement > 0:
            self.no_improvement_iterations = 0
        else:
            self.no_improvement_iterations += 1
