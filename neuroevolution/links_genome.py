from neuroevolution.link_gene import LinkGene
from neuroevolution.node_gene import NodeGene
from copy import copy
from typing import Dict, Tuple, Union


class DuplicatedLink(RuntimeError):
    def __init__(self, message):
        super().__init__(message)


class LinksGenome:
    def __init__(self):
        self.link_genes: Dict[Tuple[NodeGene, NodeGene], LinkGene] = {}

    def add_gene(self, link_gene: LinkGene):
        if self.link_genes.get((link_gene.outgoing_gene, link_gene.ingoing_gene)) is not None:
            raise DuplicatedLink("ERROR: TRIED TO ADD EXISTING LINK!")
        self.link_genes[(link_gene.outgoing_gene, link_gene.ingoing_gene)] = link_gene

    def has_link(self, outgoing_node: NodeGene, ingoing_node: NodeGene) -> Union[None, LinkGene]:
        return self.link_genes.get((outgoing_node, ingoing_node))

    def get_copy(self):
        new_links_genome = LinksGenome()
        for link_gene in self.link_genes.values():
            new_links_genome.add_gene(copy(link_gene))
        return new_links_genome

    def __str__(self):
        string = "Links[" + str(len(self.link_genes)) + "]:\n"
        for link_gene in self.link_genes.values():
            string += "(" + str(link_gene.outgoing_gene.identifier) + "=[" + str(round(link_gene.weight, 4)) +\
                      "]>" + str(link_gene.ingoing_gene.identifier)
            if link_gene.is_disabled:
                string += " DISABLED"
            string += ")"
        return string
