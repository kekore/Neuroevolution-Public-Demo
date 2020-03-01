from neuroevolution.controllers import ProblemController
import numpy as np
import gym
from time import sleep


class AtlantisGame:
    def __init__(self, demo):
        self.score = 0
        self.do_render = demo
        self.env = gym.make("AtlantisDeterministic-v4")

    def reset(self):
        self.score = 0
        return self.process_img(self.env.reset())

    def receive_action(self, action):
        if self.do_render:
            self.env.render()
            sleep(0.02)
        state, reward, done, info = self.env.step(action)
        self.score += reward
        if info.get('ale.lives') < 6:
            return self.score
        return self.process_img(state)

    @staticmethod
    def process_img(img):
        img = img[20:116, 8:184]
        img = img[::6, ::6]
        return np.dot(img[..., :3], [0.299, 0.587, 0.144]).flatten()


class AtlantisController(ProblemController):
    def __init__(self, network_controller, demo):
        super().__init__(network_controller, demo)
        self.game = AtlantisGame(demo)
        self.do_shot = False

    def run_test(self):
        state = self.game.reset()
        while not isinstance(state, float):
            if not self.do_shot:
                for o in range(len(state)):
                    state[o] = state[o] / 255

                network_output = self.network_controller.process_input(state)
                state = self.game.receive_action(network_output.index(max(network_output))+1)
                self.do_shot = True
            else:
                self.game.receive_action(0)
                self.do_shot = False

        self.score = state
        self.game.env.close()
