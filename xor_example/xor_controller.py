from neuroevolution.controllers import ProblemController
from xor_example.xor_thread import Xor
import numpy as np


class XorController(ProblemController):
    def __init__(self, network_controller, demo):
        super(XorController, self).__init__(network_controller, demo)
        self.problem = Xor(demo)

    def prepare(self):
        pass

    def run_test(self):
        self.problem.start()
        while True:
            problem = self.problem.out_queue.get(block=True)
            if problem is None:
                break
            network_output = self.network_controller.process_input(np.array(problem))
            for output_index in range(len(network_output)):
                if network_output[output_index] is None:
                    network_output[output_index] = 0
            answer = (problem, [network_output[0]])
            self.problem.in_queue.put(answer)
        self.problem.join()
        self.score = self.problem.score
