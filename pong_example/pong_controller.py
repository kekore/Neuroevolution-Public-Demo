from neuroevolution.controllers import ProblemController
import gym
from time import sleep


class PongGame:
    def __init__(self, demo):
        self.score = 0
        self.do_render = demo
        self.env = gym.make("Pong-ramDeterministic-v4")
        self.time = 0

    def receive_action(self, action):
        if self.do_render:
            self.env.render()
            sleep(0.03)
        state, reward, done, info = self.env.step(action)
        self.score += reward
        if done or self.time > 25000:
            return self.score  # if end of episode - return score
        self.time += 1
        return state


class PongController(ProblemController):
    def __init__(self, network_controller, demo):
        super().__init__(network_controller, demo)
        self.game = PongGame(demo)

    def run_test(self):
        state = self.game.env.reset()
        # play until receives score
        while not isinstance(state, float):
            input_vector = self.state_to_input_vector(state)
            output_vector = self.network_controller.process_input(input_vector)
            action = self.output_vector_to_action(output_vector)
            state = self.game.receive_action(action)
        self.score = state
        self.game.env.close()

    def state_to_input_vector(self, state):
        # get ball's and racket's position and normalize them
        return [(state[49]-103)/103, (state[50]-130)/76, (state[51]-121)/83]

    def output_vector_to_action(self, output_vector):
        return 5 if output_vector[0] == 0 else 2
