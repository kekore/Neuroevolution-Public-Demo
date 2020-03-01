from genetic_nn.neuron import *
from typing import List, Type
from collections import deque


class VectorLenMismatch(RuntimeError):
    def __init__(self, message):
        super().__init__(message)


class Network:
    """
    Neural network with DAG topology
    """
    def __init__(self):
        self.input_neurons: List[InputNeuron] = []
        self.output_neurons: List[OutputNeuron] = []
        self.hidden_neurons: List[HiddenNeuron] = []
        self.bias_neurons = []

    def guess(self, input_vec: List[float]) -> List[float]:
        """
        Takes vector of float values and produces an output vector.
        :param input_vec: vector of float values that have to be proceeded
        :raises: :class:'VectorLenMisMatch': Size of input does not equal amount of input neurons
        :return: result of neural network calculations - vector of float values
        """
        if len(input_vec) != len(self.input_neurons):
            raise VectorLenMismatch("ERROR: SIZE OF INPUT DOES NOT EQUAL AMOUNT OF INPUT NEURONS!")

        # pass input to input neurons
        for i in range(len(self.input_neurons)):
            self.input_neurons[i].receive_input(input_vec[i])

        # prepare calculation queue - put input neurons and bias into queue plus all neurons that have 0 ingoing links
        initial_list = self.bias_neurons + self.input_neurons
        for neuron in self.hidden_neurons + self.output_neurons:
            if neuron.ingoing_links_amount == 0:
                initial_list.append(neuron)

        queue = deque(initial_list)
        # perform calculations
        while queue:
            ready_list = queue[0].process_input()
            queue += ready_list
            queue.popleft()

        # take and return output
        output = []
        for o in self.output_neurons:
            output.append(o.get_output())
        return output

    def add_bias_neuron(self, identifier):
        self.bias_neurons.append(BiasNeuron(identifier))

    def add_input_neuron(self, identifier):
        self.input_neurons.append(InputNeuron(identifier))

    def add_hidden_neuron(self, identifier, act_function: Type[FuncAbstract]):
        self.hidden_neurons.append(HiddenNeuron(identifier, act_function))

    def add_output_neuron(self, identifier, act_function: Type[FuncAbstract]):
        self.output_neurons.append(OutputNeuron(identifier, act_function))
