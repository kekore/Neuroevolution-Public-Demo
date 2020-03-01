from neuroevolution.controllers import NetworkController
from neuroevolution.genome import Genome
from neuroevolution.node_gene import NodeType
from genetic_nn.network import Network
from genetic_nn.act_functions import *
from typing import List, Type


class NetController(NetworkController):
    def __init__(self, genome: Genome):
        super(NetController, self).__init__(genome)
        # create neurons and connections basing on genome
        self.network = Network()

        # add nodes basing on nodes genome
        for input_gene in genome.nodes_genome.input_genes:
            if input_gene.node_type == NodeType.INPUT:
                self.network.add_input_neuron(input_gene.identifier)
            else:
                self.network.add_bias_neuron(input_gene.identifier)
        for output_gene in genome.nodes_genome.output_genes:
            self.network.add_output_neuron(output_gene.identifier, NetController.translate_function(output_gene.act_function))
            for hidden_gene in genome.nodes_genome.hidden_genes:
                self.network.add_hidden_neuron(hidden_gene.identifier, NetController.translate_function(hidden_gene.act_function))

        # create links basing on links genome
        for link_gene in genome.links_genome.link_genes.values():
            if link_gene.is_disabled:  # skip disabled links
                continue
            # find outgoing node
            outgoing_node = None
            for node in self.network.bias_neurons + self.network.input_neurons + self.network.hidden_neurons:
                if node.identifier == link_gene.outgoing_gene.identifier:
                    outgoing_node = node
                    break
            # find ingoing node
            ingoing_node = None
            for node in self.network.hidden_neurons + self.network.output_neurons:
                if node.identifier == link_gene.ingoing_gene.identifier:
                    ingoing_node = node
                    break
            outgoing_node.link_to(ingoing_node, link_gene.weight)

    def process_input(self, input_vector: List[float]) -> List[float]:
        return self.network.guess(input_vector)

    @staticmethod
    def translate_function(func_name) -> Type[FuncAbstract]:
        if func_name == "IDENTITY":
            return Identity
        elif func_name == "SIGMOID":
            return Sigmoid
        elif func_name == "TANH":
            return TanH
        elif func_name == "STEP":
            return BinaryStep
        elif func_name == "RELU":
            return Relu
        elif func_name == "SIGMOID5":
            return Sigmoid5
        else:
            return TanH
