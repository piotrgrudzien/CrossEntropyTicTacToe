import numpy as np
from Game import Game


def get_stats(solution, human_one_move_ahead, games):
    w, d, l = 0, 0, 0
    for i in range(games):
        res = get_single_game_reward(solution, debug=False, one_ahead=human_one_move_ahead)
        if res == 1: w += 1
        if res == 0: d += 1
        if res == -1: l += 1
    print '*** Solution stats ***'
    print 'Wins', w
    print 'Draws', d
    print 'Losses', l


def get_single_game_reward(p, debug, one_ahead):
    game = Game(p, debug=debug, one_ahead=one_ahead)
    while not game.finished():
        game.move()
    return game.result()


def get_total_reward(p, m, human_one_move_ahead):
    # argument is a vector of length 81 (sample policy)
    r = 0
    for i in range(0, m):
        r += get_single_game_reward(p, debug=False, one_ahead=human_one_move_ahead)
    return r


def get_reward_vector(p, m, human_one_move_ahead):
    # argument is an Nx81 matrix (policy population)
    r = np.apply_along_axis(get_total_reward, 1, p, m, human_one_move_ahead)
    return r
