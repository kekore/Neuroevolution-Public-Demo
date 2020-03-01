from neuroevolution.controllers import ProblemController
from neuroevolution.genome import Genome
from multiprocessing import Process, Queue
import psutil
from typing import List, Type, Tuple


class TestCluster:
    def __init__(self, network_ctrler_cls, problem_ctrler_cls, processes_amount: int):
        self.to_test_queue = Queue()  # outgoing queue
        self.tested_queue = Queue()  # ingoing queue
        # create test processes
        self.processes: List[TestProcess] = []
        for process_index in range(processes_amount):
            new_process = TestProcess(network_ctrler_cls, problem_ctrler_cls, self.to_test_queue, self.tested_queue)
            self.processes.append(new_process)
            new_process.start()
        self.pause()

    def perform_tests(self, genomes_to_test: List[Genome]):
        self.resume()
        # put genomes to outgoing queue
        for genome_index, genome in enumerate(genomes_to_test):
            # pass index of the genome not to lose genome tracking due to multiprocessing
            self.to_test_queue.put((genome_index, genome))
        # loop to collect results - they will appear in unknown order, that's what index is passed for
        for genome_counter in range(len(genomes_to_test)):
            result: Tuple[int, float] = self.tested_queue.get()
            genomes_to_test[result[0]].fitness = result[1]
            print("TESTING PROGRESS: " + str(round(100 * genome_counter / len(genomes_to_test), 2)) + "%")
        self.pause()

    def pause(self):
        for process in self.processes:
            psutil.Process(process.pid).suspend()

    def resume(self):
        for process in self.processes:
            psutil.Process(process.pid).resume()

    def close(self):
        self.resume()
        for process in self.processes:
            process.terminate()


class TestProcess(Process):
    def __init__(self, network_ctrler_cls, problem_ctrler_cls, to_test_queue, tested_queue):
        super(TestProcess, self).__init__()
        self.to_test_queue = to_test_queue  # ingoing queue
        self.tested_queue = tested_queue  # outgoing queue
        self.network_ctrler_cls = network_ctrler_cls
        self.problem_ctrler_cls = problem_ctrler_cls

    def run(self):
        # run in a loop and test every genome received from queue
        genome_tuple: Tuple[int, Genome] = self.to_test_queue.get()
        while genome_tuple is not None:
            genome = genome_tuple[1]
            # create controllers and run test
            problem_controller: Type[ProblemController] = self.problem_ctrler_cls(self.network_ctrler_cls(genome), False)
            problem_controller.run_test()
            # fetch the score and put it to the outgoing queue
            self.tested_queue.put((genome_tuple[0], problem_controller.score))
            genome_tuple = self.to_test_queue.get()
