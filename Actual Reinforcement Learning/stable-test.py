# -*- coding: utf-8 -*-
"""
Created on Sun Aug  1 07:19:14 2021

@author: Hostl
"""
import numpy as np
import gym
from gym import spaces
from stable_baselines.common.env_checker import check_env
from stable_baselines import DQN, PPO2, A2C, ACKTR
from stable_baselines.common.cmd_util import make_vec_env
from stable_env import GoLeftEnv



print("Test 2")


env = GoLeftEnv()
# If the environment don't follow the interface, an error will be thrown
check_env(env, warn=True)

print(" ")
print("Testing none stable baselines")
env = GoLeftEnv(grid_size=10)

obs = env.reset()
env.render()

print(env.observation_space)
print(env.action_space)
print(env.action_space.sample())

GO_LEFT = 0
# Hardcoded best agent: always go left!
n_steps = 20
for step in range(n_steps):
  print("Step {}".format(step + 1))
  obs, reward, done, info = env.step(GO_LEFT)
  print('obs=', obs, 'reward=', reward, 'done=', done)
  env.render()
  if done:
    print("Goal reached!", "reward=", reward)
    break


print(" ")
print("Testing stable baselines")


# Instantiate the env
env = GoLeftEnv(grid_size=10)
# wrap it
env = make_vec_env(lambda: env, n_envs=1)

# Train the agent
model = ACKTR('MlpPolicy', env, verbose=1).learn(5000)

# Test the trained agent
obs = env.reset()
n_steps = 20
for step in range(n_steps):
  action, _ = model.predict(obs, deterministic=True)
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

https://www.reddit.com/r/reinforcementlearning/comments/mcmrna/how_can_i_use_stablebaselines_to_train_multiple/