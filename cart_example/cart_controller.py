from neuroevolution.controllers import ProblemController
import gym
from time import sleep
import numpy as np
from statistics import mean


class CartGame:
    def __init__(self, demo):
        self.score = 0
        self.do_render = demo
        self.env = gym.make("CartPole-v1")
        self.time = 0

    def reset(self, seed):
        self.score = 0
        self.time = 0
        self.env.seed(seed)
        return self.env.reset()

    def receive_action(self, action):
        if self.do_render:
            self.env.render()
            sleep(0.03)
        state, reward, done, info = self.env.step(action)
        self.score += reward
        if done or self.time >= 300:
            return self.score
        self.time += 1
        return state


class CartController(ProblemController):
    def __init__(self, network_controller, demo):
        super().__init__(network_controller, demo)
        self.game = CartGame(demo)
        self.scores = []

    def run_test(self):
        for episode in range(20):
            state = self.game.reset(1 + episode * 2)
            while not isinstance(state, float):
                state = self.game.receive_action(int(self.network_controller.process_input(np.array(state))[0]))
            self.scores.append(state)
        self.score = mean(self.scores)
        self.game.env.close()
