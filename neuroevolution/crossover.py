from neuroevolution.genome import Genome
from neuroevolution.nodes_genome import NodesGenome
from neuroevolution.links_genome import LinksGenome
from neuroevolution.link_gene import LinkGene
from numpy.random import normal
import random
from copy import copy
from typing import Union


class Crosser:
    def __init__(self, neuroevolution_instance):
        self.nev = neuroevolution_instance

    def cross(self, genome1: Genome, genome2: Genome):
        # prepare new nodes genome
        new_nodes_genome = NodesGenome()
        new_nodes_genome.input_genes = genome1.nodes_genome.input_genes
        new_nodes_genome.output_genes = genome1.nodes_genome.output_genes
        new_nodes_genome.hidden_genes = genome1.nodes_genome.hidden_genes.copy()

        # choose link genes
        new_links_genome = LinksGenome()  # prepare new links genome
        for link_gene in genome1.links_genome.link_genes.values():  # iterate through first links genome
            # check if same link exists in second genome
            same_link: Union[None, LinkGene] = genome2.links_genome.has_link(link_gene.outgoing_gene, link_gene.ingoing_gene)
            # if same link exists, count average weight or choose randomly (depending on config)
            if same_link is not None:
                # determine weight value
                if random.random() < self.nev.config.average_crossover_chance:
                    new_weight: float = (link_gene.weight+same_link.weight)/2
                else:
                    if random.random() < 0.5:
                        new_weight = link_gene.weight
                    else:
                        new_weight = same_link.weight
                new_weight += normal(0.0, self.nev.config.weight_shift_standard_deviation)

                new_link_gene = LinkGene(link_gene.outgoing_gene, link_gene.ingoing_gene, new_weight, None)
                if link_gene.is_disabled == same_link.is_disabled:
                    new_link_gene.is_disabled = link_gene.is_disabled
                else:
                    if random.random() < 0.5:
                        new_link_gene.is_disabled = False
                    else:
                        new_link_gene.is_disabled = True
                new_links_genome.add_gene(new_link_gene)

            # if same link doesn't exist in second genome, but it's legal for new genome - copy it
            elif new_nodes_genome.is_link_possible(link_gene.outgoing_gene, link_gene.ingoing_gene):
                new_links_genome.add_gene(copy(link_gene))

        for link_gene in genome2.links_genome.link_genes.values():  # now iterate through second genome
            # do not consider same links (they were considered above)
            if genome1.links_genome.has_link(link_gene.outgoing_gene, link_gene.ingoing_gene) is None:
                # same as above - if link is legal for new genome - just copy it
                if new_nodes_genome.is_link_possible(link_gene.outgoing_gene, link_gene.ingoing_gene):
                    new_links_genome.add_gene(copy(link_gene))

        return Genome(new_nodes_genome, new_links_genome)
