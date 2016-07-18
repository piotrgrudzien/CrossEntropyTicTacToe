import numpy as np


def get_reward(p):

    return R

N = 100  # number of sampled policies at each step
M = 100  # number of games played during each round
X = 20  # top X% policy samples are used for updating the multivariate Gaussian
mu_init = np.random.rand(9**2, None)  # vector of length 81
cov_init = np.random.rand(9**2, 9**2)  # 81x81 matrix

# sample N policies from a multivariate Gaussian
P = np.random.multivariate_normal(mu_init, cov_init, N)  # Nx81 matrix

# calculate total reward for each policy
R = get_reward(P)  # vector of length N

