import numpy as np
import random

human = 'human'
ai = 'ai'


class Game:

    def __init__(self, policy):
        self._policy = policy
        self._state = np.zeros(9)
        self._moved_last = random.choice([human, ai])
        self._result = None

    def finished(self):
        if self.human_won():
            self._result = -1
        if self.ai_won():
            self._result = 1
        if self.draw():
            self._result = 0
        if self.human_illegal():
            self._result = 1
        if self.ai_illegal():
            self._result = -1
        return self._result is not None

    def result(self):
        return self._result

    def move(self):
        self.ai_move() if self._moved_last is human else self.human_move()

    def ai_move(self):
        # TODO implement
        self.state = None

    def human_move(self):
        # TODO implement
        self.state = None

    def human_won(self):
        # TODO implement
        return False

    def ai_won(self):
        # TODO implement
        return False

    def draw(self):
        # TODO implement
        return False

    def human_illegal(self):
        # TODO implement
        return False

    def ai_illegal(self):
        # TODO implement
        return False