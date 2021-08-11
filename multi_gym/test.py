# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 11:31:40 2021

@author: Hostl
"""
import gym
import mgym
import random




env = gym.make('TicTacToe-v0')
fullobs = env.reset()
turns = 0
while True:
    turns +=1
    print('Player O ') if fullobs[0] else print('Player X')
    a = random.choice(env.get_available_actions())
    fullobs,rewards,done,_ = env.step(a)
    env.render()
    if done:
        break
    
    
    

    
print("{} Turns taken".format(turns))
    
"""
env = gym.make('MatchingPennies-v0')
env.reset(3)
while True:
    a = env.action_space.sample()
    _,r,done,_ = env.step(a)
    env.render()
    if done:
        break
"""