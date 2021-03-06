import numpy as np
import pickle, time
from datetime import datetime
from Utils import get_reward_vector, get_single_game_reward, get_stats

start = time.time()

N = 5000  # number of sampled policies at each step
M = 100  # number of games played during each round
N_ROUNDS = 100  # number of rounds
X_init = 3000  # top X policy samples are used for updating the multivariate Gaussian
ANN_FACTOR = 30
mu_init = np.random.rand(9**2)  # vector of length 81
cov_init = np.random.rand(9**2, 9**2)  # 81x81 matrix
HUMAN_ONE_MOVE_AHEAD = True

print 'Number of sampled policies at each step N =', N
print 'Number of games played during each round M =', M
print 'Number of rounds N_ROUNDS =', N_ROUNDS
print 'Number of policies used (initially) for updating the multivariate Gaussian X =', X_init
print 'Annealing factor ANN_FACTOR =', ANN_FACTOR
print 'Human one move ahead =', HUMAN_ONE_MOVE_AHEAD

# sample N policies from a multivariate Gaussian
P = np.random.multivariate_normal(mu_init, cov_init, N)  # Nx81 matrix

# calculate total reward for each policy
R = np.array(get_reward_vector(P, M, HUMAN_ONE_MOVE_AHEAD))  # vector of length N

for i in range(N_ROUNDS):

    X = int(X_init * (1 - np.exp(np.true_divide(i - N_ROUNDS, ANN_FACTOR))))

    if i % 10 == 0:
        print 'Elapsed {:1.1f} minutes'.format(np.true_divide(time.time() - start, 60))
    print 'Round', str(i + 1), ': Sampled policies', X, ', Average reward', np.average(R), 'Best reward', np.max(R)

    Best = P[R.argsort()[-X:][::-1]]

    mu = np.mean(Best, axis=0)
    cov = np.cov(Best, rowvar=0)

    P = np.random.multivariate_normal(mu, cov, N)
    R = np.array(get_reward_vector(P, M, HUMAN_ONE_MOVE_AHEAD))

print 'Elapsed {:1.1f} minutes'.format(np.true_divide(time.time() - start, 60))
Solution = mu
timestamp = '{:%Y-%m-%d|%H-%M-%S}'.format(datetime.now())
pickle.dump(Solution, open('solutions/Solution' + timestamp + '.p', 'wb'))
print 'Dumped solution to', 'solutions/Solution' + timestamp + '.p'


for i in range(10):
    res = get_single_game_reward(Solution, debug=True, one_ahead=HUMAN_ONE_MOVE_AHEAD)

get_stats(Solution, human_one_move_ahead=HUMAN_ONE_MOVE_AHEAD, games=100)



