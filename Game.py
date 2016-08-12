import numpy as np
import random

human = 'human'
ai = 'ai'
# Markers
human_circle = -1  # human circle
empty = 0.1  # empty
ai_cross = 1  # ai cross
triples = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]


def inv_get_move(move):
    return move + 1


def is_legal(move, state):
    return state[move] == empty


def check_one_ahead(state, marker, this_triples):
    move = None
    for triple in this_triples:
        if state[triple[0]] == marker:
            if (state[triple[1]] == marker) & (state[triple[2]] == empty):
                move = triple[2]
                break
            elif (state[triple[2]] == marker) & (state[triple[1]] == empty):
                move = triple[1]
                break
        elif (state[triple[1]] == marker) & (state[triple[2]] == marker) & (state[triple[0]] == empty):
            move = triple[0]
            break
    return move


def check_two_ahead(state, marker, this_triples):
    move = None
    for triple in this_triples:
        if state[triple[0]] == marker:
            if (state[triple[1]] == empty) & (state[triple[2]] == empty):
                move = triple[2]
                break
        elif (state[triple[0]] == empty) & (((state[triple[1]] == marker) & (state[triple[2]] == empty)) | ((state[triple[1]] == empty) & (state[triple[2]] == marker))):
            move = triple[0]
            break
    return move

class Game:

    def __init__(self, policy, debug, one_ahead):
        self._debug = debug
        self._one_ahead = one_ahead
        self._triples = triples
        random.shuffle(self._triples)
        if self._debug:
            print '*** Initializing new game ***'
        self._policy = policy
        self._state = np.zeros(9)
        self._state.fill(empty)
        if self._debug:
            print str(self._state.astype(int).reshape(3, 3)).replace('0.1', '0')
        self._moved_last = random.choice([human, ai])
        if self._debug:
            print 'Moved last:', self._moved_last
        self._result = None
        self._ai_illegal = False

    def finished(self):
        if self.human_won():
            self._result = -1
        elif self.ai_won():
            self._result = 1
        elif self.draw():
            self._result = 0
        if self._debug:
            if self._result == 1:
                print 'AI won!'
            elif self._result == -1:
                print 'Human won!'
            elif self._result == 0:
                print 'Draw!'
        return self._result is not None

    def result(self):
        return self._result

    def move(self):
        if self._moved_last is human:
            move = self.ai_move()
            if not is_legal(move, self._state):
                self._ai_illegal = True
                return
            self._state[move] = ai_cross
            self._moved_last = ai
        else:
            self._state[self.human_move()] = human_circle
            self._moved_last = human
        if self._debug:
            print str(self._state.astype(int).reshape(3, 3)).replace('0.1', '0')

    def ai_move(self):
        p_matrix = self._policy.reshape(9, 9)
        probs = p_matrix.dot(self._state)
        move = np.argmax(probs)
        if self._debug:
            print 'AI move:', inv_get_move(move)
        return move

    def human_move(self):
        move = None
        if self._one_ahead:
            # check if can win in one move
            move = check_one_ahead(self._state, human_circle, self._triples)
            if move is None:
                # check if might loose in one move
                move = check_one_ahead(self._state, ai_cross, self._triples)
                if move is None:
                # choose a move where a win is two steps away
                    move = check_two_ahead(self._state, human_circle, self._triples)
        if move is None:
            move = random.choice(np.where(self._state == empty)[0])
        if self._debug:
            print 'Human move:', inv_get_move(move)
        return move

    def human_won(self):
        if self._ai_illegal: return True
        for triple in triples:
            if (self._state[triple[0]] == human_circle) & (self._state[triple[1]] == human_circle) & (self._state[triple[2]] == human_circle):
                return True
        return False

    def ai_won(self):
        for triple in triples:
            if (self._state[triple[0]] == ai_cross) & (self._state[triple[1]] == ai_cross) & (self._state[triple[2]] == ai_cross):
                return True
        return False

    def draw(self):
        return empty not in self._state
