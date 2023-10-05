from typing import Dict, List
from mlagents_envs.base_env import ActionTuple
from mlagents_envs.side_channel.side_channel import SideChannel
from mlagents_envs.environment import UnityEnvironment
from scipy.spatial.transform import Rotation as R
import numpy as np
import time 
from rl_modules.float_log_channel import FloatLogChannel

REWARD_SCALE = 10.0

class UnderwaterEnv:
    def __init__(
        self,
        file_name: str,
        worker_id: int,
        base_port: int,
        seed: int,
        no_graphics: bool,
        timeout_wait: int,
        log_folder: str,
        max_steps: int,
        reward_type: str,
        max_reward: float,
        nsubsteps: int = 50,
        behavior_name: str = None,
    ):
        print("Start the environment with worker_id: ", worker_id, " and base_port: ", base_port)
        self.float_log = FloatLogChannel()
        self.env = UnityEnvironment(file_name=file_name, 
                                    worker_id=worker_id,
                                    base_port=base_port,
                                    seed=seed,
                                    no_graphics=no_graphics,
                                    timeout_wait=timeout_wait,
                                    side_channels=[self.float_log])
        self.env.reset()
        if behavior_name is None:
            behavior_name = list(self.env.behavior_specs)[0]
        else:
            if behavior_name not in self.env.behavior_specs:
                raise RuntimeError(f"Unknown behavior name {behavior_name}")
        self.behavior_name = behavior_name
        self.action_space = self.env.behavior_specs[behavior_name].action_spec
        self.observation_space = self.env.behavior_specs[behavior_name].observation_specs[0]
        self.max_steps = max_steps
        self.action_max = 1
        self.reward_type = reward_type
        self.max_reward = max_reward
        self.nsubsteps = nsubsteps
        self.th_dense_reward = -0.8 # threshold for the dense reward to reset the environment
        self.th_sparse_reward = 0.001 # threshold for the sparse reward to turn positive

    # we need to reset multiple times to avoid the bug in the environment
    def reset(self, nsubsteps=15, times=3):
        print("====================Reset the environment====================")
        for _ in range(times-1):
            print("Reset the environment for ", _+1, " times")
            self.env.reset()
            self.step(nsubsteps=nsubsteps)
        print("Reset the environment for ", times, " times")
        self.env.reset()
        return self.step(nsubsteps=nsubsteps)[0]
    
    def step(self, action=None, nsubsteps=None):
        if action is not None:
            self.env.set_actions(self.behavior_name, self._process_action(action))
        if nsubsteps is None:
            nsubsteps = self.nsubsteps
        for _ in range(nsubsteps):
            if self._is_terminal():
                break
            self.env.step()
        get_obs = self.get_obs()
        obs = {
            'observation': get_obs['observation'],
            'achieved_goal': get_obs['achieved_goal'],
            'desired_goal': get_obs['desired_goal']
        }
        reward = get_obs['reward']
        is_done = self._is_terminal() and reward > -0.001 # hard code the threshold for sparse reward for now
        info = {
            'is_success': is_done,
        }
        if (self.reward_type == "dense" and reward < self.th_dense_reward): # reset simulation in case of glitch
            self.env.reset()
        return obs, reward, is_done, info
    
    def _is_terminal(self):
        decision_steps, terminal_steps = self.env.get_steps(self.behavior_name)
        return len(terminal_steps) != 0
    
    def close(self):
        self.env.close()

    def get_obs(self):
        decision_steps, _ = self.env.get_steps(self.behavior_name)
        obs = decision_steps.obs[0]
        achieved_goal = obs[0][0:3] 
        desired_goal = obs[0][3:6]
        reward = self._get_single_reward(achieved_goal, desired_goal)
        return {
            'observation': obs[0],
            'achieved_goal': achieved_goal,
            'desired_goal': desired_goal,
            'reward': reward
        }
    
    def _goal_distance(self, goal_a, goal_b):
        assert goal_a.shape == goal_b.shape
        return np.linalg.norm(goal_a - goal_b, axis=-1)
    
    def _get_single_reward(self, achieved_goal, desired_goal):
        return self.compute_reward(np.array([achieved_goal]), np.array([desired_goal]))[0]
    
    def compute_reward(self, achieved_goal, desired_goal, info=None):
        distance = self._goal_distance(achieved_goal, desired_goal)
        if self.reward_type == "sparse":
            reward = (distance < self.th_sparse_reward).astype(np.float32) * self.max_reward
            return reward
        else:
            reward = -distance.astype(np.float32)/REWARD_SCALE
            return reward
        
    def send_float(self, value):
        self.float_log.send_float32(value)
            
    def _process_action(self, action):
        action_tuple = ActionTuple(
            continuous=np.reshape(action[0:self.action_space.continuous_size], (1, self.action_space.continuous_size))
        )
        return action_tuple

