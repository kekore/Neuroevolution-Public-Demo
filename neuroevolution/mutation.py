from neuroevolution.genome import Genome
from neuroevolution.link_gene import LinkGene
from neuroevolution.node_gene import NodeGene
import random
from typing import Union


class Mutator:
    def __init__(self, neuroevolution_instance):
        self.nev = neuroevolution_instance
        self.mutating_genome: Union[None, Genome] = None

    def mutate(self, genome: Genome):
        self.mutating_genome = genome
        mutations_occurred = 0

        if self.nev.config.do_new_link_mutation:
            if self.new_link_mutation():
                mutations_occurred += 1
            if mutations_occurred >= self.nev.config.max_mutations_once:
                return
        if self.nev.config.do_divide_link_mutation and self.nev.allow_new_species:
            if self.divide_link_mutation():
                mutations_occurred += 1
            if mutations_occurred >= self.nev.config.max_mutations_once:
                return
        if self.nev.config.do_alter_disabled_mutation:
            if self.alter_disabled_mutation():
                mutations_occurred += 1
            if mutations_occurred >= self.nev.config.max_mutations_once:
                return
        if self.nev.config.do_enable_link_mutation:
            if self.enable_link_mutation():
                mutations_occurred += 1
            if mutations_occurred >= self.nev.config.max_mutations_once:
                return
        if self.nev.config.do_weight_shift_mutation:
            if self.weight_shift_mutation():
                mutations_occurred += 1
            if mutations_occurred >= self.nev.config.max_mutations_once:
                return
        if self.nev.config.do_randomize_weight_mutation:
            if self.randomize_weight_mutation():
                mutations_occurred += 1
            if mutations_occurred >= self.nev.config.max_mutations_once:
                return
        if self.nev.config.do_randomize_all_weights_mutation:
            if self.randomize_all_weights_mutation():
                mutations_occurred += 1
            if mutations_occurred >= self.nev.config.max_mutations_once:
                return

    def new_link_mutation(self) -> bool:
        if random.random() >= self.nev.config.new_link_prob:
            return False

        # get list of possible new links
        possible_new_links = self.mutating_genome.get_possible_new_links()
        if len(possible_new_links) == 0:
            return False
        # pick random link from this list and (if it's legal) add it to genome
        random_new_link = random.choice(possible_new_links)
        outgoing_node = random_new_link[0]
        ingoing_node = random_new_link[1]
        # try to add/check chosen link, if caught RecursionIllegal, it means it makes loop - erase this
        # link from possible_new_links and chose again
        while not self.nev.add_or_check_link(outgoing_node, ingoing_node):
            possible_new_links.remove(random_new_link)
            if len(possible_new_links) == 0:
                return False
            random_new_link = random.choice(possible_new_links)
            outgoing_node = random_new_link[0]
            ingoing_node = random_new_link[1]

        # prepare new link gene
        weight = random.uniform(self.nev.config.weight_interval[0], self.nev.config.weight_interval[1])
        new_link_gene = LinkGene(outgoing_node, ingoing_node, weight, False)
        self.mutating_genome.links_genome.add_gene(new_link_gene)
        return True

    def divide_link_mutation(self) -> bool:
        if random.random() >= self.nev.config.divide_link_prob or len(self.mutating_genome.links_genome.link_genes) == 0:
            return False

        # pick random link to divide
        random_link: LinkGene = random.choice(list(self.mutating_genome.links_genome.link_genes.values()))
        # create new hidden node
        new_node: NodeGene = NodeGene.get_random_hidden(self.nev.get_next_node_identifier(), self.nev.config.hidden_functions_set)
        # add new node to mutating genome
        self.mutating_genome.nodes_genome.hidden_genes.append(new_node)

        # create first new link
        outgoing_node = random_link.outgoing_gene
        ingoing_node = new_node
        self.nev.add_or_check_link(outgoing_node, ingoing_node)
        new_link1: LinkGene = LinkGene(outgoing_node, ingoing_node, 1.0, False)
        self.mutating_genome.links_genome.add_gene(new_link1)

        # create second new link
        outgoing_node = new_node
        ingoing_node = random_link.ingoing_gene
        self.nev.add_or_check_link(outgoing_node, ingoing_node)
        new_link2 = LinkGene(outgoing_node, ingoing_node, random_link.weight, False)
        self.mutating_genome.links_genome.add_gene(new_link2)

        if random.random() < self.nev.config.disabling_prob:
            random_link.is_disabled = True

        return True

    def alter_disabled_mutation(self) -> bool:
        if random.random() >= self.nev.config.alter_disabled_prob or len(self.mutating_genome.links_genome.link_genes) == 0:
            return False

        # choose link to alter
        random_link: LinkGene = random.choice(list(self.mutating_genome.links_genome.link_genes.values()))
        random_link.is_disabled = not random_link.is_disabled

        return True

    def enable_link_mutation(self) -> bool:
        if random.random() >= self.nev.config.enable_link_prob or len(self.mutating_genome.links_genome.link_genes) == 0:
            return False

        # get disabled links
        disabled_links = []
        for link in self.mutating_genome.links_genome.link_genes.values():
            if link.is_disabled:
                disabled_links.append(link)

        if len(disabled_links) == 0:
            return False

        # choose link to enable
        random_link: LinkGene = random.choice(disabled_links)
        random_link.is_disabled = False

        return True

    def weight_shift_mutation(self):
        if random.random() >= self.nev.config.weight_shift_prob or len(self.mutating_genome.links_genome.link_genes) == 0:
            return False

        # choose link to shift weight
        random_link: LinkGene = random.choice(list(self.mutating_genome.links_genome.link_genes.values()))
        random_link.weight *= random.uniform(self.nev.config.weight_shift_interval[0], self.nev.config.weight_shift_interval[1])

        return True

    def randomize_weight_mutation(self):
        if random.random() >= self.nev.config.randomize_weight_prob or len(self.mutating_genome.links_genome.link_genes) == 0:
            return False

        # choose link to randomize weight
        random_link: LinkGene = random.choice(list(self.mutating_genome.links_genome.link_genes.values()))
        random_link.weight = random.uniform(self.nev.config.weight_interval[0], self.nev.config.weight_interval[1])

        return True

    def randomize_all_weights_mutation(self):
        if random.random() >= self.nev.config.randomize_all_weights_prob or len(self.mutating_genome.links_genome.link_genes) == 0:
            return False

        for link_gene in self.mutating_genome.links_genome.link_genes.values():
            if random.random() < self.nev.config.single_randomization_prob:
                link_gene.weight = random.uniform(self.nev.config.weight_interval[0], self.nev.config.weight_interval[1])

        return True
