from threading import Thread, Lock
from queue import Queue
from typing import Tuple, List


class Xor(Thread):
    def __init__(self, demo):
        super(Xor, self).__init__()
        self.in_queue = Queue()
        self.out_queue = Queue()
        self.next_problem = [0, 0]
        self.problem_lock = Lock()
        self.end = False
        self.score = 0
        self.score_lock = Lock()
        self.demo = demo

    def run(self):
        while True:
            if self.out_queue.empty():
                self.out_queue.put(self.get_next_problem())
            if self.end:
                break
            answer = self.in_queue.get()
            self.check_answer(answer)
        if self.demo:
            with self.score_lock:
                print("Scored: " + str(self.score))

    def get_next_problem(self):
        with self.problem_lock:
            problem = self.next_problem
            if problem == [0, 0]:
                self.next_problem = [1, 0]
            elif problem == [1, 0]:
                self.next_problem = [0, 1]
            elif problem == [0, 1]:
                self.next_problem = [1, 1]
            elif problem == [1, 1]:
                self.next_problem = None
            else:
                self.end = True
        return problem

    def check_answer(self, answer: Tuple[List[float], List[float]]):
        with self.score_lock:
            if answer[0] in [[0, 0], [1, 1]]:
                self.score += 1 - abs(0 - answer[1][0])
            else:
                self.score += 1 - abs(1 - answer[1][0])
