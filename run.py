import numpy as np
from Game import Game


def get_single_game_reward(p):
    init = np.zeros(9)
    game = Game(p)
    while not game.finished():
        game.move()
    return game.result()


def get_total_reward(p):
    # argument is a vector of length 81 (sample policy)
    r = 0
    for i in range(0, M):
        r += get_single_game_reward(p)
    return r


def get_reward_vector(p):
    # argument is an Nx81 matrix (policy population)
    r = np.apply_along_axis(get_total_reward, 1, p)
    return r

N = 100  # number of sampled policies at each step
M = 100  # number of games played during each round
X = 20  # top X% policy samples are used for updating the multivariate Gaussian
mu_init = np.random.rand(9**2)  # vector of length 81
print 'mu_init shape', mu_init.shape
cov_init = np.random.rand(9**2, 9**2)  # 81x81 matrix
print 'cov_init shape', cov_init.shape

# sample N policies from a multivariate Gaussian
P = np.random.multivariate_normal(mu_init, cov_init, N)  # Nx81 matrix
print 'P shape', P.shape

# calculate total reward for each policy
R = get_reward_vector(P)  # vector of length N

