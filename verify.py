from mlagents_envs.environment import UnityEnvironment
import os

from arguments import get_args
from env.underwater_env import UnderwaterEnv

print("Start verifying the environment...")
args = get_args()
unity_env = UnderwaterEnv(file_name=args.file_name, 
                    worker_id=0, 
                    base_port=None, 
                    seed=args.seed, 
                    no_graphics=True, 
                    timeout_wait=60, 
                    side_channels=[],
                    log_folder='logs/', 
                    max_steps=100, 
                    behavior_name=None,
                    reward_type=args.reward_type,
                    max_reward=args.max_reward,
                    nsubsteps=args.nsubsteps)

print("Environment is set up!")
unity_env.reset()
done = False
reward = 0
while not done:
  # Move the simulation forward
  obs, reward, done, info = unity_env.step()
  decision_steps, terminal_steps = unity_env.env.get_steps(unity_env.behavior_name)
  print("reward: ", reward, " done: ", done, " info: ", info, "terminal_steps len: ", len(terminal_steps))
print("reward: ", reward, " done: ", done, " info: ", info)