import numpy as np
from typing import List, Tuple, Union, Type
from genetic_nn.act_functions import FuncAbstract


class IllegalLink(RuntimeError):
    def __init__(self, message):
        super().__init__(message)


class IllegalOperation(RuntimeError):
    def __init__(self, message):
        super().__init__(message)


class Neuron:
    """Neuron abstract class"""
    def __init__(self, identifier: int):
        self.identifier: int = identifier
        self.ingoing_links_amount: int = 0
        self.outgoing_links: List[Tuple[Neuron, float]] = []  # float is the weight of connection

    def link_to(self, neuron, weight: float):
        """
        Links this neuron A into given neuron B with given weight. Neuron A will feed forward calculations into
        every single neuron that neuron A is connected to.
        """
        if isinstance(neuron, InputNeuron):
            raise IllegalLink("ERROR: TRIED TO CONNECT NEURON TO INPUT NEURON!")
        for out_link in self.outgoing_links:
            if neuron == out_link[0]:
                raise IllegalLink("ERROR: THIS NEURON IS ALREADY CONNECTED TO GIVEN NEURON!")

        neuron.ingoing_links_amount += 1
        self.outgoing_links.append((neuron, weight))

    def receive_input(self, value, weight=1.0) -> bool:
        """
        This method is called by neuron A linked into this neuron B when A calculated its output and feeds it forward.
        For hidden and output neurons, it pushes given value into input vector and given weight into weight vector.
        When size of input vector is equal to ingoing_links_amount (neuron received all expected values),
        this neuron is ready to process.
        :rtype: bool
        :return: True when this neuron is ready to process (received values from every input neuron)
                False when this neuron is not ready to process
        """
        pass

    def process_input(self) -> List:
        """
        If this neuron is ready, it calculates its output value and feeds forward the output value into all neurons
        that this neuron is linked to. Also collects information which of those neurons got ready to process.
        :rtype: list
        :return: List of neurons that got ready to process after receiving the value from this neuron.
        """
        pass


class InputNeuron(Neuron):
    def __init__(self, identifier: int):
        super(InputNeuron, self).__init__(identifier)
        self.output = None  # Output of the neuron. For input neuron it's set up with receive_input method.

    def receive_input(self, value, weight=1.0) -> bool:
        """It's basically used for setting the value of this particular input neuron."""
        self.output = value
        return True

    def process_input(self) -> List:
        if self.output is None:
            raise IllegalOperation("ERROR: process_input OPERATION ON INPUT NEURON (ID: " + str(self.identifier) + ") IS ILLEGAL - INPUT WASN'T SET")
        ready_neurons = []
        for out_link in self.outgoing_links:
            if out_link[0].receive_input(self.output, out_link[1]):
                ready_neurons.append(out_link[0])
        self.output = None  # flush output
        return ready_neurons


class HiddenNeuron(Neuron):
    def __init__(self, identifier: int, activation_function: Type[FuncAbstract]):
        super(HiddenNeuron, self).__init__(identifier)
        self.activation_function: Type[FuncAbstract] = activation_function
        self.input = []
        self.weights = []

    def receive_input(self, value, weight=1.0) -> bool:
        self.input.append(value)
        self.weights.append(weight)
        if len(self.input) == self.ingoing_links_amount:
            return True
        return False

    def process_input(self) -> List:
        if len(self.input) != self.ingoing_links_amount:
            raise IllegalOperation("ERROR: process_input OPERATION ON HIDDEN NEURON (ID: %s) IS ILLEGAL - LENGTH OF INPUT VECTOR IS %s BUT NEURON HAS %s ENTRIES!" % (str(self.identifier), len(self.input), self.ingoing_links_amount))

        if len(self.input) == 0:
            output = 0
        else:
            output = self.activation_function.func(np.dot(self.input, self.weights))
        # print("Output: %s" % output)
        self.input = []  # flush input
        self.weights = []  # flush weights
        ready_neurons = []
        for out_link in self.outgoing_links:
            if out_link[0].receive_input(output, out_link[1]):
                ready_neurons.append(out_link[0])
        return ready_neurons


class OutputNeuron(Neuron):
    def __init__(self, identifier: int, activation_function: Type[FuncAbstract]):
        super(OutputNeuron, self).__init__(identifier)
        self.activation_function = activation_function
        self.input = []
        self.weights = []
        self.output = None

    def link_to(self, neuron, weight: float):
        raise IllegalLink("ERROR TRIED TO LINK OUTPUT NEURON TO SOME OTHER NEURON!")

    def receive_input(self, value, weight=1.0) -> bool:
        self.input.append(value)
        self.weights.append(weight)
        if len(self.input) == self.ingoing_links_amount:
            return True
        return False

    def process_input(self) -> List:
        if len(self.input) > self.ingoing_links_amount:
            raise IllegalOperation("ERROR: process_input OPERATION ON OUTPUT NEURON (ID: %s) IS ILLEGAL - LENGTH OF INPUT VECTOR IS %s BUT NEURON HAS %s ENTRIES!" % (str(self.identifier), len(self.input), self.ingoing_links_amount))

        if len(self.input) == 0:
            self.output = 0
        else:
            # print(np.dot(self.input, self.weights))
            self.output = self.activation_function.func(np.dot(self.input, self.weights))
        # print("Output: %s" % self.output)
        self.input = []  # flush input
        self.weights = []  # flush weights
        return []

    def get_output(self) -> Union[float, None]:
        """
        Method used to take values of output vector of the neural network.
        :return: Output value of this neuron.
        """
        if self.output is None:
            output = 0
        else:
            output = self.output
        self.output = None  # flush output
        return output


class BiasNeuron(Neuron):
    def __init__(self, identifier: int):
        super(BiasNeuron, self).__init__(identifier)
        self.output = 1

    def receive_input(self, value: float, weight=1.0) -> bool:
        raise IllegalOperation("ERROR: TRIED TO SET OUTPUT OF BIAS NEURON!")

    def process_input(self) -> List:
        ready_neurons = []
        for out_link in self.outgoing_links:
            if out_link[0].receive_input(self.output, out_link[1]):
                ready_neurons.append(out_link[0])
        return ready_neurons
