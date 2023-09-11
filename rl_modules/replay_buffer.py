import threading
import numpy as np
import csv

"""
the replay buffer here is basically from the openai baselines code

"""
class replay_buffer:
    def __init__(self, env_params, buffer_size, sample_func, multiplier=1):
        self.env_params = env_params
        self.T = env_params['max_timesteps']
        self.multiplier = multiplier
        self.size = buffer_size // (self.T*multiplier)
        # memory management
        self.current_size = 0
        self.n_transitions_stored = 0
        self.sample_func = sample_func
        # create the buffer to store info
        self.buffers = {'obs': np.empty([self.size, (self.T + 1)*multiplier, self.env_params['obs']]),
                        'ag': np.empty([self.size, (self.T + 1)*multiplier, self.env_params['goal']]),
                        'g': np.empty([self.size, (self.T + 1)*multiplier, self.env_params['goal']]),
                        'actions': np.empty([self.size, self.T*multiplier, self.env_params['action']]),
                        'r': np.empty([self.size, self.T*multiplier, 1])
                        }
        # thread lock
        self.lock = threading.Lock()
    
    # store the episode
    def store_episode(self, episode_batch):
        mb_obs, mb_ag, mb_g, mb_actions, mb_rewards = episode_batch

        batch_size = mb_obs.shape[0]
        with self.lock:
            idxs = self._get_storage_idx(inc=batch_size)
            self.buffers['obs'][idxs] = mb_obs
            self.buffers['ag'][idxs] = mb_ag
            self.buffers['g'][idxs] = mb_g
            self.buffers['actions'][idxs] = mb_actions
            self.buffers['r'][idxs] = mb_rewards
            self.n_transitions_stored += self.T * batch_size
    
    def write_to_file(self, filename, max_timesteps):
        temp_buffers = {}
        with self.lock:
            for key in self.buffers.keys():
                temp_buffers[key] = self.buffers[key][:self.current_size]
        temp_buffers['obs_next'] = temp_buffers['obs'][:, self.multiplier:, :]
        temp_buffers['ag_next'] = temp_buffers['ag'][:, self.multiplier:, :]
        temp_buffers['g_next'] = temp_buffers['g'][:, self.multiplier:, :]
        # save the temp_buffers to csv file each time rewrite the file
        with open(filename, 'w') as f:
            writer = csv.writer(f)
            for i in range(self.current_size):
                for j in range(max_timesteps):
                    writer.writerow(np.concatenate([temp_buffers['obs'][i][j], temp_buffers['ag'][i][j], temp_buffers['g'][i][j], temp_buffers['actions'][i][j], temp_buffers['r'][i][j], temp_buffers['obs_next'][i][j], temp_buffers['ag_next'][i][j], temp_buffers['g_next'][i][j]], axis=0))
    
    # sample the data from the replay buffer
    def sample(self, batch_size):
        temp_buffers = {}
        with self.lock:
            for key in self.buffers.keys():
                temp_buffers[key] = self.buffers[key][:self.current_size]
        temp_buffers['obs_next'] = temp_buffers['obs'][:, self.multiplier:, :]
        temp_buffers['ag_next'] = temp_buffers['ag'][:, self.multiplier:, :]
        temp_buffers['g_next'] = temp_buffers['g'][:, self.multiplier:, :]
        # sample transitions
        transitions = self.sample_func(temp_buffers, batch_size)
        return transitions

    def _get_storage_idx(self, inc=None):
        inc = inc or 1
        if self.current_size+inc <= self.size:
            idx = np.arange(self.current_size, self.current_size+inc)
        elif self.current_size < self.size:
            overflow = inc - (self.size - self.current_size)
            idx_a = np.arange(self.current_size, self.size)
            idx_b = np.random.randint(0, self.current_size, overflow)
            idx = np.concatenate([idx_a, idx_b])
        else:
            idx = np.random.randint(0, self.size, inc)
        self.current_size = min(self.size, self.current_size+inc)
        if inc == 1:
            idx = idx[0]
        return idx
