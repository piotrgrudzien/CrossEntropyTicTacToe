import numpy as np
import random

human = 'human'
ai = 'ai'

def is_legal(move, state):
    return state[move] == 0

class Game:

    def __init__(self, policy, debug):
        self._debug = debug
        if self._debug:
            print '*** Initializing new game ***'
        self._policy = policy
        if self._debug:
            print 'Policy:[', self._policy[0], ', ... ,', self._policy[-1], ']'
        self._state = np.zeros(9)
        if self._debug:
            print 'State:', self._state
        self._moved_last = random.choice([human, ai])
        if self._debug:
            print 'Moved last:', self._moved_last
        self._result = None
        self._ai_illegal = False

    def finished(self):
        if self.human_won():
            self._result = -1
        if self.ai_won():
            self._result = 1
        if self.draw():
            self._result = 0
        if self._debug:
            print 'Checking result:', self._result
        return self._result is not None

    def result(self):
        return self._result

    def move(self):
        if self._moved_last is human:
            move = self.ai_move()
            if not is_legal(move, self._state):
                self._ai_illegal = True
                return
            self._state[move] = 1
            self._moved_last = ai
        else:
            self._state[self.human_move()] = -1
            self._moved_last = human
        if self._debug:
            print 'State:', self._state


    def ai_move(self):
        p_matrix = self._policy.reshape(9, 9)
        probs = p_matrix.dot(self._state)
        move = np.argmax(probs)
        if self._debug:
            print 'AI move:', move
        return move

    def human_move(self):
        move = random.choice(np.where(self._state == 0)[0])
        if self._debug:
            print 'Human move:', move
        return move

    # merge the two functions below into one
    def human_won(self):
        # TODO implement
        # implement 8 checks
        # get the order right to make it as fast as possible
        if self._ai_illegal: return True
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
