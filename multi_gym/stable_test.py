# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 12:12:45 2021
@author: Kevin Charles Hostler
"""
"""
import numpy as np
import gym
from gym import spaces
"""
from stable_baselines3.common.env_checker import check_env
from stable_baselines3 import A2C
from stable_baselines3.common.env_util import make_vec_env

from custom_env import block_world
from custom_goleft import GoLeftEnv
from custom_SimpleMultiObsEnv import SimpleMultiObsEnv

# Instantiate the env
env = block_world(3,3)
env = SimpleMultiObsEnv()
#env = GoLeftEnv(grid_size=10)

# wrap it
env = make_vec_env(lambda: env, n_envs=1)

# Train the agent
# robot_1 = A2C('MlpPolicy', env, verbose=1).learn(5000)

steps = 50000
n     = 50

robot_1 = A2C('MlpPolicy', env, n_steps=n, verbose=1).learn(steps)

"""
robot_1.save("a2c_blocks{}_{}".format(steps,n))

del robot_1 # remove to demonstrate saving and loading

robot_1 = A2C.load("a2c_blocks{}_{}".format(steps,n))
"""


# Test the trained agent
obs = env.reset()
n_steps = 50
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
