import numpy as np
import pickle
from Game import Game


def get_single_game_reward(p, debug, one_ahead):
    game = Game(p, debug=debug, one_ahead=one_ahead)
    while not game.finished():
        game.move()
    return game.result()


def get_total_reward(p):
    # argument is a vector of length 81 (sample policy)
    r = 0
    for i in range(0, M):
        r += get_single_game_reward(p, debug=False, one_ahead=HUMAN_ONE_MOVE_AHEAD)
    return r


def get_reward_vector(p):
    # argument is an Nx81 matrix (policy population)
    r = np.apply_along_axis(get_total_reward, 1, p)
    return r

N = 500  # number of sampled policies at each step
M = 100  # number of games played during each round
N_ROUNDS = 10  # number of rounds
X = 100  # top X policy samples are used for updating the multivariate Gaussian
mu_init = np.random.rand(9**2)  # vector of length 81
cov_init = np.random.rand(9**2, 9**2)  # 81x81 matrix
HUMAN_ONE_MOVE_AHEAD = True

# sample N policies from a multivariate Gaussian
P = np.random.multivariate_normal(mu_init, cov_init, N)  # Nx81 matrix

# calculate total reward for each policy
R = np.array(get_reward_vector(P))  # vector of length N

for i in range(N_ROUNDS):
    print 'Round', str(i + 1), ': Average reward', np.average(R), 'Best reward', np.max(R)

    Best = P[R.argsort()[-X:][::-1]]

    mu = np.mean(Best, axis=0)
    cov = np.cov(Best, rowvar=0)

    P = np.random.multivariate_normal(mu, cov, N)
    R = np.array(get_reward_vector(P))

Solution = np.random.multivariate_normal(mu, cov, 1)
pickle.dump(Solution, open('Solution.p', 'wb'))

for i in range(5):
    get_single_game_reward(Solution, debug=True, one_ahead=HUMAN_ONE_MOVE_AHEAD)

