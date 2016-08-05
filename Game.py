import numpy as np
import random

human = 'human'
ai = 'ai'

def is_legal(move, state):
    return state[move] == 0

class Game:

    def __init__(self, policy):
        self._policy = policy
        self._state = np.zeros(9)
        self._moved_last = random.choice([human, ai])
        self._result = None
        self._ai_illegal = False

    def finished(self):
        if self.human_won():
            self._result = -1
        if self.ai_won():
            self._result = 1
        if self.draw():
            self._result = 0
        return self._result is not None

    def result(self):
        return self._result

    def move(self):
        self.ai_move() if self._moved_last is human else self.human_move()
        if self._moved_last is human:
            move = self.ai_move()
            if not is_legal(move, self._state):
                self._ai_illegal = True
                return
            self._state[move] = 1
        else:
            self._state[self.human_move()] = -1



    def ai_move(self):
        # TODO implement
        # turn vector p into a 9x9 matrix
        # the next move is argmax of self.state multiplied by the matrix
        # return move
        p_matrix = self._policy.reshape(3, 3)
        probs = p_matrix.dot(self._state)
        return np.argmax(probs)

    def human_move(self):
        # TODO implement
        # implement a random legal move
        # sample a random index from where self.state is 0
        # move
        return random.choice(np.where(self._state == 0)[0])

    # merge the two functions below into one
    def human_won(self):
        # TODO implement
        # implement 8 checks
        # get the order right to make it as fast as possible
        if (self._state[0] == -1) & (self._state[1] == -1) & (self._state[2] == -1): return True
        if (self._state[3] == -1) & (self._state[4] == -1) & (self._state[5] == -1): return True
        if (self._state[6] == -1) & (self._state[7] == -1) & (self._state[8] == -1): return True
        if (self._state[0] == -1) & (self._state[3] == -1) & (self._state[6] == -1): return True
        if (self._state[1] == -1) & (self._state[4] == -1) & (self._state[7] == -1): return True
        if (self._state[2] == -1) & (self._state[5] == -1) & (self._state[8] == -1): return True
        if (self._state[0] == -1) & (self._state[4] == -1) & (self._state[8] == -1): return True
        if (self._state[2] == -1) & (self._state[4] == -1) & (self._state[6] == -1): return True
        return False

    def ai_won(self):
        # TODO implement
        # implement 8 checks
        # get the order right to make it as fast as possible
        if (self._state[0] == 1) & (self._state[1] == 1) & (self._state[2] == 1): return True
        if (self._state[3] == 1) & (self._state[4] == 1) & (self._state[5] == 1): return True
        if (self._state[6] == 1) & (self._state[7] == 1) & (self._state[8] == 1): return True
        if (self._state[0] == 1) & (self._state[3] == 1) & (self._state[6] == 1): return True
        if (self._state[1] == 1) & (self._state[4] == 1) & (self._state[7] == 1): return True
        if (self._state[2] == 1) & (self._state[5] == 1) & (self._state[8] == 1): return True
        if (self._state[0] == 1) & (self._state[4] == 1) & (self._state[8] == 1): return True
        if (self._state[2] == 1) & (self._state[4] == 1) & (self._state[6] == 1): return True
        return False

    def draw(self):
        return 0 not in self._state
