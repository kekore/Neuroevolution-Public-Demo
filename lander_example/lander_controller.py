from neuroevolution.controllers import ProblemController
import gym
from time import sleep
from statistics import mean


class LanderGame:
    def __init__(self, demo):
        self.score = 0
        self.do_render = demo
        self.env = gym.make("LunarLanderContinuous-v2")
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
        if done or self.time >= 250:
            return self.score
        self.time += 1
        return state


class LanderController(ProblemController):
    def __init__(self, network_controller, demo):
        super().__init__(network_controller, demo)
        self.game = LanderGame(demo)
        self.scores = []

    def run_test(self):
        for episode in range(10):
            state = self.game.reset(episode*10+14)
            while not isinstance(state, float):
                network_output = self.network_controller.process_input(state)
                state = self.game.receive_action(network_output)
            self.scores.append(state)
        self.score = mean(self.scores)
        self.game.env.close()
