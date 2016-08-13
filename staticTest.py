import pickle
from Utils import get_stats, get_single_game_reward

Solution = pickle.load(open('solutions/Solution2016-08-13|08-15-53.p')) # -14 average reached

w, d, l = 0, 0, 0
for i in range(10):
    res = get_single_game_reward(Solution, debug=True, one_ahead=True)
    if res == 1: w += 1
    if res == 0: d += 1
    if res == -1: l += 1
print '*** Solution stats ***'
print 'Wins', w
print 'Draws', d
print 'Losses', l

get_stats(Solution, human_one_move_ahead=True, games=100)