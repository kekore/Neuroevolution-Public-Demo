from neuroevolution.crossover import Crosser
from neuroevolution.mutation import Mutator
from neuroevolution.population import Population
from neuroevolution.genome import Genome
from neuroevolution.config import ParentChoosingMethod
from math import ceil
import random
from typing import List, Tuple, Union


class Reproducer:
    def __init__(self, neuroevolution_instance):
        self.nev = neuroevolution_instance
        self.crosser: Crosser = Crosser(self.nev)
        self.mutator: Mutator = Mutator(self.nev)

    def create_next_population(self) -> Population:
        # prepare survivors list for new population
        survivors: List[Genome] = self.get_survivors()
        # prepare new genomes_list
        new_genomes_list: List[Genome] = self.reproduce()

        # give each genome an opportunity to mutate
        for genome in new_genomes_list:
            self.mutator.mutate(genome)

        return Population(new_genomes_list, survivors)

    def get_survivors(self) -> List[Genome]:
        all_survivors: List[Genome] = []
        for species in self.nev.species:
            survivors_amount = ceil(self.nev.config.survival_percentage * len(species.genomes))
            all_survivors += species.genomes[:survivors_amount]
        return all_survivors

    def reproduce(self) -> List[Genome]:
        new_genome_list: List[Genome] = []

        single_species_offspring_amount = ceil(self.nev.config.offspring_quantity/len(self.nev.species))
        print(single_species_offspring_amount)
        # crossover the fittest genomes
        for species in self.nev.species:
            breeding_individuals_amount = ceil(self.nev.config.breeding_percentage * len(species.genomes))
            if breeding_individuals_amount == 1:
                breeding_individuals_amount = 2
            breeding_individuals = species.genomes[:breeding_individuals_amount]
            for offspring_index in range(single_species_offspring_amount):
                parent1, parent2 = self.choose_parents(breeding_individuals)
                new_genome: Genome = self.crosser.cross(parent1, parent2)
                new_genome_list.append(new_genome)
        return new_genome_list

    # \/\/\/ PARENT CHOOSING \/\/\/
    def choose_parents(self, breeding_individuals: List[Genome]) -> Tuple[Genome, Genome]:
        if self.nev.config.parent_choosing_method == ParentChoosingMethod.RANDOM:
            return Reproducer.random_choice(breeding_individuals)
        else:
            return Reproducer.shifted_roulette_choice(breeding_individuals)

    @staticmethod
    def random_choice(individuals_list: List[Genome]) -> Tuple[Genome, Genome]:
        parent1: Genome = random.choice(individuals_list)
        parent2: Genome = random.choice(individuals_list)
        while parent1 == parent2:
            parent2 = random.choice(individuals_list)
        return parent1, parent2

    @staticmethod
    def shifted_roulette_choice(individuals_list: List[Genome]) -> Tuple[Genome, Genome]:
        worst_fitness: float = individuals_list[0].fitness
        for individual in individuals_list:
            if individual.fitness < worst_fitness:
                worst_fitness = individual.fitness

        shifted_values: List[float] = []
        for individual in individuals_list:
            shifted_value = individual.fitness - worst_fitness
            shifted_values.append(shifted_value)

        values_sum: float = sum(shifted_values)
        random_value1: float = random.uniform(0, values_sum)
        random_value2: float = random.uniform(0, values_sum)
        parent1: Union[Genome, None] = None
        parent2: Union[Genome, None] = None

        for shifted_index in range(len(shifted_values)):
            random_value1 -= shifted_values[shifted_index]
            if random_value1 <= 0 and parent1 is None:
                parent1 = individuals_list[shifted_index]
                if parent2 is not None and parent1 == parent2:
                    if individuals_list.index(parent1) == 0:
                        parent1 = individuals_list[1]
                    else:
                        parent1 = individuals_list[0]

            random_value2 -= shifted_values[shifted_index]
            if random_value2 <= 0 and parent2 is None:
                parent2 = individuals_list[shifted_index]
                if parent1 is not None and parent2 == parent1:
                    if individuals_list.index(parent2) == 0:
                        parent2 = individuals_list[1]
                    else:
                        parent2 = individuals_list[0]
            if parent1 is not None and parent2 is not None:
                break

        return parent1, parent2
    # /\/\/\ PARENT CHOOSING /\/\/\
