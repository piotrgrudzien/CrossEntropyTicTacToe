import unittest, pickle, random
import numpy as np
from Game import Game, is_legal, check_one_ahead, check_two_ahead, human_circle, ai_cross, empty, triples


# get state by specifying human circles [ 1 2 3 ]
# and ai crosses as in:                 [ 4 5 6 ]
# same for get move:                    [ 7 8 9 ]
def get_state(human_circles, ai_crosses):
    if len(human_circles) > len(set(human_circles)):
        raise KeyError('Duplicate human circles:', human_circles)
    if len(ai_crosses) > len(set(ai_crosses)):
        raise KeyError('Duplicate ai crosses:', ai_crosses)
    if len([val for val in human_circles if val in ai_crosses]) != 0:
        raise KeyError('Repeated indexes in human circles', human_circles, 'and ai crosses', ai_crosses)
    state = np.zeros(9)
    state.fill(empty)
    for i in human_circles:
        state[i - 1] = human_circle
    for i in ai_crosses:
        state[i - 1] = ai_cross
    return state


def get_move(move):
    return move - 1


class GameMethods(unittest.TestCase):

    def test_is_legal(self):
        self.assertTrue(is_legal(get_move(1), get_state(human_circles=[2, 3, 4], ai_crosses=[6, 5])))
        self.assertFalse(is_legal(get_move(5), get_state(human_circles=[2, 3, 4], ai_crosses=[6, 5])))

    def test_check_one_ahead(self):
        self.assertEqual(check_one_ahead(get_state(human_circles=[1, 2], ai_crosses=[5, 6]), human_circle, triples), get_move(3))
        self.assertEqual(check_one_ahead(get_state(human_circles=[1, 5], ai_crosses=[3, 6]), human_circle, triples), get_move(9))
        self.assertEqual(check_one_ahead(get_state(human_circles=[1, 6], ai_crosses=[2, 5]), ai_cross, triples), get_move(8))
        self.assertEqual(check_one_ahead(get_state(human_circles=[1, 5], ai_crosses=[3, 6]), ai_cross, triples), get_move(9))

    def test_check_two_ahead(self):
        self.assertIn(check_two_ahead(get_state(human_circles=[1], ai_crosses=[5, 7]), human_circle, triples), [get_move(x) for x in [2, 3, 4]])
        self.assertIn(check_two_ahead(get_state(human_circles=[5], ai_crosses=[3, 4, 6, 7]), human_circle, triples),
                  [get_move(x) for x in [1, 2, 8]])
        self.assertIn(check_two_ahead(get_state(human_circles=[1, 6], ai_crosses=[2, 5, 9]), human_circle, triples),
                  [get_move(x) for x in [4, 7]])

    def test_finished(self):
        g = Game(s, debug=False, one_ahead=True)
        g._state = get_state(human_circles=[1, 2, 3], ai_crosses=[5, 6])
        self.assertTrue(g.finished())
        self.assertEqual(g.result(), -1)
        g = Game(s, debug=False, one_ahead=True)
        g._state = get_state(human_circles=[1, 3], ai_crosses=[5, 6])
        self.assertFalse(g.finished())
        g = Game(s, debug=False, one_ahead=True)
        g._state = get_state(human_circles=[1, 2, 4, 5, 9], ai_crosses=[3, 6, 7, 8])
        self.assertTrue(g.finished())
        self.assertEqual(g.result(), -1)
        g = Game(s, debug=False, one_ahead=True)
        g._state = get_state(human_circles=[1, 2, 4, 5], ai_crosses=[3, 6, 7, 8, 9])
        self.assertTrue(g.finished())
        self.assertEqual(g.result(), 1)
        g = Game(s, debug=False, one_ahead=True)
        g._state = get_state(human_circles=[1, 2, 4, 5], ai_crosses=[3, 6, 7, 8])
        self.assertFalse(g.finished())
        g = Game(s, debug=False, one_ahead=True)
        g._state = get_state(human_circles=[1, 2, 4, 5], ai_crosses=[3, 6, 7, 9])
        self.assertTrue(g.finished())
        self.assertEqual(g.result(), 1)
        g = Game(s, debug=False, one_ahead=True)
        g._state = get_state(human_circles=[1, 3, 4, 8, 9], ai_crosses=[2, 5, 6, 7])
        self.assertTrue(g.finished())
        self.assertEqual(g.result(), 0)

    def test_human_move(self):
        g = Game(s, debug=False, one_ahead=True)
        g._state = get_state(human_circles=[], ai_crosses=[])
        self.assertIn(g.human_move(), [get_move(x) for x in range(1, 10)])
        g = Game(s, debug=False, one_ahead=True)
        g._state = get_state(human_circles=[1, 2, 5, 9], ai_crosses=[3, 4, 7])
        self.assertIn(g.human_move(), [get_move(x) for x in [6, 8]])
        g = Game(s, debug=False, one_ahead=True)
        g._state = get_state(human_circles=[1, 2], ai_crosses=[5])
        self.assertEqual(g.human_move(), get_move(3))
        g = Game(s, debug=False, one_ahead=True)
        g._state = get_state(human_circles=[1, 2, 5], ai_crosses=[6, 4, 9])
        self.assertIn(g.human_move(), [get_move(x) for x in [3, 8]])
        g = Game(s, debug=False, one_ahead=True)
        g._state = get_state(human_circles=[7, 8], ai_crosses=[4, 5])
        self.assertEqual(g.human_move(), get_move(9))
        g = Game(s, debug=False, one_ahead=True)
        g._state = get_state(human_circles=[7, 2], ai_crosses=[4, 5])
        self.assertEqual(g.human_move(), get_move(6))
        g = Game(s, debug=False, one_ahead=True)
        g._state = get_state(human_circles=[1, 2, 8], ai_crosses=[3, 7])
        self.assertEqual(g.human_move(), get_move(5))
        g = Game(s, debug=False, one_ahead=True)
        g._state = get_state(human_circles=[4, 8], ai_crosses=[1, 2, 5])
        self.assertIn(g.human_move(), [get_move(x) for x in [3, 9]])
        g = Game(s, debug=False, one_ahead=True)
        g._state = get_state(human_circles=[4, 8], ai_crosses=[2, 6])
        self.assertIn(g.human_move(), [get_move(x) for x in [1, 7, 9]])
        g = Game(s, debug=False, one_ahead=True)
        g._state = get_state(human_circles=[4, 9], ai_crosses=[1, 6])
        self.assertIn(g.human_move(), [get_move(x) for x in [7, 8]])
        g = Game(s, debug=False, one_ahead=True)
        g._state = get_state(human_circles=[3], ai_crosses=[4, 9])
        self.assertIn(g.human_move(), [get_move(x) for x in [1, 2, 5, 7]])

    def test_human_won(self):
        g = Game(s, debug=False, one_ahead=True)
        g._state = get_state(human_circles=[1, 4, 6, 7, 8], ai_crosses=[2, 3, 5, 9])
        self.assertTrue(g.human_won())
        g = Game(s, debug=False, one_ahead=True)
        g._state = get_state(human_circles=[1, 4, 6, 8], ai_crosses=[2, 3, 5, 9])
        self.assertFalse(g.human_won())
        g = Game(s, debug=False, one_ahead=True)
        g._state = get_state(human_circles=[1, 3, 4, 6, 8], ai_crosses=[2, 5, 7, 9])
        self.assertFalse(g.human_won())

    def test_ai_won(self):
        g = Game(s, debug=False, one_ahead=True)
        g._state = get_state(human_circles=[1, 2, 4, 8], ai_crosses=[3, 5, 6, 7, 9])
        self.assertTrue(g.ai_won())
        g = Game(s, debug=False, one_ahead=True)
        g._state = get_state(human_circles=[1, 4, 6, 8], ai_crosses=[2, 3, 5, 9])
        self.assertFalse(g.ai_won())
        g = Game(s, debug=False, one_ahead=True)
        g._state = get_state(human_circles=[1, 3, 4, 6, 8], ai_crosses=[2, 5, 7, 9])
        self.assertFalse(g.ai_won())

    def test_draw(self):
        g = Game(s, debug=False, one_ahead=True)
        g._state = get_state(human_circles=[1, 4, 6, 8], ai_crosses=[2, 3, 5, 9])
        self.assertFalse(g.draw())
        g = Game(s, debug=False, one_ahead=True)
        g._state = get_state(human_circles=[1, 4, 6, 8], ai_crosses=[2, 3, 5, 9])
        self.assertFalse(g.ai_won())
        g = Game(s, debug=False, one_ahead=True)
        g._state = get_state(human_circles=[1, 3, 4, 6, 8], ai_crosses=[2, 5, 7, 9])
        self.assertTrue(g.draw())

s = pickle.load(open('Solution.p', 'rb'))
random.shuffle(triples)

suite = unittest.TestLoader().loadTestsFromTestCase(GameMethods)
unittest.TextTestRunner(verbosity=2).run(suite)