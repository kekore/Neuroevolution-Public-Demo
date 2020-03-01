class NetworkController:
    """Abstract class for network controller"""
    def __init__(self, genome):
        # create an instance of neural network basing on given genome and store it in network field
        self.network = None

    def process_input(self, input_vector):
        # enter given input to the network and return the output
        pass


class ProblemController:
    def __init__(self, network_controller: NetworkController, demo: bool):
        self.score = None
        self.network_controller: NetworkController = network_controller

    def run_test(self):
        # perform full test and set up the score value
        pass

    def state_to_input_vector(self, state):
        # process state and return input vector for the network
        pass

    def output_vector_to_action(self, output_vector):
        # process network output and return action to perform
        pass
