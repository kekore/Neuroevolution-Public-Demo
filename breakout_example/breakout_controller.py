from neuroevolution.controllers import ProblemController
import gym
from time import sleep
from typing import List


class BreakoutGame:
    def __init__(self, demo):
        self.score = 0
        self.do_render = demo
        self.env = gym.make("Breakout-ramNoFrameskip-v4")

    def reset(self):
        self.score = 0
        return self.env.reset()

    def receive_action(self, action):
        if self.do_render:
            self.env.render()
            sleep(0.01)
        state, reward, done, info = self.env.step(action)
        self.score += reward
        if info.get('ale.lives') < 5 or self.score == 864 or done:
            return self.score
        return state


class BreakoutController(ProblemController):
    def __init__(self, network_controller, demo):
        super().__init__(network_controller, demo)
        self.game = BreakoutGame(demo)

    def run_test(self):
        self.game.reset()
        state = self.game.receive_action(1)
        while not isinstance(state, float):
            filtered_state = [(state[70]-92)/92, (state[99]-124)/68, (state[101]-90)/90]
            network_output = self.network_controller.process_input(filtered_state)
            state = self.game.receive_action(self.choose_action_tanh(network_output))

        self.score = state
        self.game.env.close()

    @staticmethod
    def choose_action_tanh(network_output: List[float]) -> int:
        if network_output[0] <= -1/10:
            return 2
        elif network_output[0] <= 1/10:
            return 0
        elif network_output[0] <= 1:
            return 3
