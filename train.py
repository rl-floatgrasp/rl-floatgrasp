from env.underwater_env import UnderwaterEnv
from rl_modules.ddpg_agent import ddpg_agent
from arguments import get_args
import os

if __name__ == "__main__":
    args = get_args()
    no_graphics = True if args.headless else False
    env = UnderwaterEnv(file_name=args.file_name, 
                        worker_id=0, 
                        base_port=5004, 
                        seed=args.seed, 
                        no_graphics=no_graphics, 
                        timeout_wait=60, 
                        log_folder='logs/', 
                        max_steps=args.max_timesteps, 
                        behavior_name=None,
                        reward_type=args.reward_type,
                        max_reward=args.max_reward,
                        nsubsteps=args.nsubsteps)
    obs = env.get_obs()
    env_params = {
        'obs': obs['observation'].shape[0],
        'goal': obs['desired_goal'].shape[0],
        'action': env.action_space.continuous_size,
        'action_max': env.action_max,
        'max_timesteps': args.max_timesteps
    }
    ddpg_ag = ddpg_agent(args, env, env_params)
    ddpg_ag.learn()