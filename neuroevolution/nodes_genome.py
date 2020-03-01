from neuroevolution.node_gene import NodeGene, NodeType
from typing import List


class NodesGenome:
    def __init__(self):
        self.input_genes: List[NodeGene] = []
        self.output_genes: List[NodeGene] = []
        self.hidden_genes: List[NodeGene] = []

    def add_gene(self, node_gene: NodeGene):
        if node_gene.node_type == NodeType.OUTPUT:
            self.output_genes.append(node_gene)
        elif node_gene.node_type == NodeType.HIDDEN:
            self.hidden_genes.append(node_gene)
        else:  # type is INPUT or BIAS
            self.input_genes.append(node_gene)

    def is_same(self, nodes_genome) -> bool:
        nodes1 = self.input_genes + self.output_genes + self.hidden_genes
        nodes2 = nodes_genome.input_genes + nodes_genome.output_genes + nodes_genome.hidden_genes
        return set(nodes1) == set(nodes2)

    def has_hidden_node(self, hidden_node_gene: NodeGene) -> bool:
        if hidden_node_gene in self.hidden_genes:
            return True
        return False

    def is_link_possible(self, outgoing_node: NodeGene, ingoing_node: NodeGene) -> bool:
        """
        This method checks ONLY if it's link between input/hidden and hidden/output!
        It doesn't check if it would duplicate existing link or make loop.
        (Because NodesGenome is low level structure - it has no information about config nor LinksGenome.)
        """
        found_outgoing = False
        for node_gene in self.input_genes + self.hidden_genes:
            if node_gene == outgoing_node:
                found_outgoing = True
                break
        if not found_outgoing:
            return False
        for node_gene in self.hidden_genes + self.output_genes:
            if node_gene == ingoing_node:
                return True
        return False

    def __str__(self):
        string = "Input genes:\n"
        for i in self.input_genes:
            string += "([input id: " + str(i.identifier) + "])"
        string += "\nOutput genes:\n"
        for o in self.output_genes:
            string += "([output id: " + str(o.identifier) + "][" + str(o.act_function) + "])"
        string += "\nHidden genes:\n"
        for h in self.hidden_genes:
            string += "([hidden id: " + str(h.identifier) + "][" + str(h.act_function) + "])"
        return string
