import argparse

"""
Here are the param for the training

"""

def get_args():
    parser = argparse.ArgumentParser()
    # the environment setting
    parser.add_argument('--n-epochs', type=int, default=200, help='the number of epochs to train the agent')
    parser.add_argument('--n-episodes', type=int, default=80, help='the number of episodes to collect samples')
    parser.add_argument('--n-batches', type=int, default=40, help='the times to update the network')
    parser.add_argument('--seed', type=int, default=1, help='random seed')
    parser.add_argument('--num-workers', type=int, default=1, help='the number of cpus to collect samples')
    parser.add_argument('--replay-strategy', type=str, default='future', help='the HER strategy')
    parser.add_argument('--replay-k', type=int, default=4, help='ratio to be replace')
    parser.add_argument('--clip-return', type=float, default=50, help='if clip the returns')
    parser.add_argument('--save-dir', type=str, default='saved_models/', help='the path to save the models')
    parser.add_argument('--noise-eps', type=float, default=0.2, help='noise eps')
    parser.add_argument('--random-eps', type=float, default=0.3, help='random eps')
    parser.add_argument('--buffer-size', type=int, default=int(1e6), help='the size of the buffer')
    parser.add_argument('--clip-obs', type=float, default=200, help='the clip ratio')
    parser.add_argument('--batch-size', type=int, default=256, help='the sample batch size')
    parser.add_argument('--gamma', type=float, default=0.98, help='the discount factor')
    parser.add_argument('--action-l2', type=float, default=1, help='l2 reg')
    parser.add_argument('--lr-actor', type=float, default=0.001, help='the learning rate of the actor')
    parser.add_argument('--lr-critic', type=float, default=0.001, help='the learning rate of the critic')
    parser.add_argument('--polyak', type=float, default=0.95, help='the average coefficient')
    parser.add_argument('--n-test-rollouts', type=int, default=10, help='the number of tests')
    parser.add_argument('--clip-range', type=float, default=5, help='the clip range')
    parser.add_argument('--cuda', action='store_true', help='if use gpu do the acceleration')
    parser.add_argument('--num-rollouts-per-mpi', type=int, default=2, help='the rollouts per mpi')
    parser.add_argument('--max-timesteps', type=int, default=50, help='the max timesteps')
    parser.add_argument('--reward-type', type=str, default='sparse', help='the reward type')
    parser.add_argument('--nsubsteps', type=int, default=20, help='the number of substeps')
    parser.add_argument('--file-name', type=str, default=None, help='the path to the environment')
    parser.add_argument('--max-reward', type=float, default=1, help='the max reward')
    parser.add_argument('--continue-training', action='store_true', help='if continue training')
    parser.add_argument('--load-actor-only', action='store_true', help='if continue training')
    parser.add_argument('--load-dir', type=str, default=None, help='the path to load the model')
    parser.add_argument('--continue-epoch', type=int, default=0, help='the epoch to continue training')
    parser.add_argument('--training-label', type=str, default='default', help='the label for training')
    parser.add_argument('--headless', action='store_true', help='if run the environment with headless')

    args = parser.parse_args()

    return args
