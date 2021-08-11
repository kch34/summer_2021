# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 12:12:45 2021

@author: Hostl
"""
import numpy as np
import gym
from gym import spaces
from stable_baselines.common.env_checker import check_env
from stable_baselines import DQN, PPO2, A2C, ACKTR
from stable_baselines.common.cmd_util import make_vec_env
#import mgym

from custom_env import block_world
from custom_goleft import GoLeftEnv

# Instantiate the env
env = GoLeftEnv(grid_size=10)






# wrap it
env = make_vec_env(lambda: env, n_envs=1)

# Train the agent
# robot_1 = A2C('MlpPolicy', env, verbose=1).learn(5000)

robot_1 = A2C('MlpPolicy', env, verbose=1).learn(2000)

# Test the trained agent
obs = env.reset()
n_steps = 20
for step in range(n_steps):
  action, _ = robot_1.predict(obs, deterministic=True)
  print("Step {}".format(step + 1))
  print("Action: ", action)
  obs, reward, done, info = env.step(action)
  print('obs=', obs, 'reward=', reward, 'done=', done)
  env.render(mode='console')
  if done:
    # Note that the VecEnv resets automatically
    # when a done signal is encountered
    print("Goal reached!", "reward=", reward)
    break
