import numpy as np

N = 100 # number of sampled policies at each step
M = 100 # number of games played during each round
p = 20 # top p% policy samples are used for updating the multivariate Gaussian
mu_init = np.random.rand(9**2, 1)
cov_init = np.random.rand(9**2, 9**2)

# sample N policies from a multivariate Gaussian
P = np.random.multivariate_normal(mu_init, cov_init, N)

print P.shape