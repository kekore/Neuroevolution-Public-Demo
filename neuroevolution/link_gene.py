from neuroevolution.node_gene import NodeGene


class LinkGene:
    def __init__(self, outgoing_gene: NodeGene, ingoing_gene: NodeGene, weight: float, is_disabled: bool):
        self.outgoing_gene: NodeGene = outgoing_gene
        self.ingoing_gene: NodeGene = ingoing_gene
        self.weight: float = weight
        self.is_disabled: bool = is_disabled
