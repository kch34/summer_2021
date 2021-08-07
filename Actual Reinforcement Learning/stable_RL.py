# -*- coding: utf-8 -*-
"""
Created on Mon Aug  2 19:50:02 2021
@author: Kevin Charles Hostler 
"""
import gym

from stable_baselines3 import A2C


from stable_env import SimpleMultiObsEnv
from stable_baselines.common.env_checker import check_env

#create the new environment

#create the model from DQN

#train the model

#save the model


#test the model
env = SimpleMultiObsEnv()

#check_env(env)

# Parallel environments

model = A2C("MultiInputPolicy", env, verbose=1)
model.learn(total_timesteps=25000)
model.save("test")


obs = env.reset()
for i in range(50):
    action, _states = model.predict(obs)
    obs, rewards, dones, info = env.step(action)
    env.render()


"""
obs = env.reset()
n_steps = 10
for _ in range(n_steps):
    # Random action
    action = env.action_space.sample()
    obs, reward, done, info = env.step(action)
"""




