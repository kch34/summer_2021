# -*- coding: utf-8 -*-
"""
Created on Fri Aug 13 10:40:10 2021

@author: Kevin Hostler
"""
#from custom_goleft import GoLeftEnv
#from custom_env    import block_world

import numpy as np
import random
import time
import tqdm
import sys
from custom_env import block_world

def cartesian(*arrays):
    mesh = np.meshgrid(*arrays)  # standard numpy meshgrid
    dim = len(mesh)  # number of dimensions
    elements = mesh[0].size  # number of elements, any index will do
    flat = np.concatenate(mesh).ravel()  # flatten the whole meshgrid
    reshape = np.reshape(flat, (dim, elements)).T  # reshape and transpose
    return reshape


x = np.arange(5)
a = cartesian(x,x,x, x,x,x, x,x,x)

grid = []
for i in tqdm.tqdm(a):    
    if (np.count_nonzero(i) <= 6) and (np.count_nonzero(i) >= 2):
        if(1 in i) and (2 in i):    
         i = i.astype('float32')
         grid.append(i)
def Convert(lst):
    res_dct = {repr(lst[i]): i for i in tqdm.trange(len(lst))}
    return res_dct
         
grid_dict = Convert(grid)


num_episodes = 1000
max_steps_per_episode = 50      #change to 50

learning_rate = 0.1
discount_rate = 0.99

exploration_rate = 1
max_exploration_rate = 1
min_exploration_rate = 0.01
exploration_decay_rate = 0.01

env = block_world(3,3)

q_table = np.zeros((len(grid), env.action_space))

rewards_all_episodes = []

print("raw {}".format(len(a)))
print("grid {}".format(len(grid)))
print("grid dict {}".format(len(grid_dict)))


start_time2 = time.time()
# Q-learning algorithm
for episode in tqdm.trange(num_episodes):

    # initialize new episode params
    state = env.reset()
    state_num = grid_dict[repr(state)]
    done = False
    rewards_current_episode = 0
    for step in range(max_steps_per_episode):
        # Exploration-exploitation trade-off
        exploration_rate_threshold = random.uniform(0, 1)
        if exploration_rate_threshold > exploration_rate:
            action = np.argmax(q_table[state_num,:])
        else:
            action = random.randint(0,53)
        new_state, reward, done, info = env.step(action)
        new_state_num = grid_dict[repr(new_state)]
        #q_table[state_num, action] = q_table[state_num, action] * (1 - learning_rate) + \
        #                         learning_rate * (reward + discount_rate * np.max(q_table[new_state_num]))
        state = new_state
        state_num = state_num = grid_dict[repr(state)]  
        rewards_current_episode += reward 
        if done == True: 
            break
    # Exploration rate decay   
    exploration_rate = min_exploration_rate + \
    (max_exploration_rate - min_exploration_rate) * np.exp(-exploration_decay_rate*episode)
    # Add current episode reward to total rewards list
    rewards_all_episodes.append(rewards_current_episode)
    
print(" ")   
x = round(time.time() - start_time2,3)
y = round(x/60,3)
print("--- %s seconds ---" % (x))
print("--- %s minutes ---" % (y))
print(" ")





# Calculate and print the average reward per thousand episodes
rewards_per_thousand_episodes = np.split(np.array(rewards_all_episodes),num_episodes/1000)
count = 1000

print("********Average reward per thousand episodes********\n")
for r in rewards_per_thousand_episodes:
    print(count, ": ", str(sum(r/1000)))
    count += 1000
# Print updated Q-table
print("\n\n********Q-table********\n")
print(q_table)


#test the newly trained agent
"""
# initialize new episode params
state = env.reset()
done = False
rewards_current_episode = 0
for step in range(max_steps_per_episode):
    # Exploration-exploitation trade-off
    exploration_rate_threshold = random.uniform(0, 1)
    if exploration_rate_threshold > exploration_rate:
        action = np.argmax(q_table[state,:]) 
    else:
        action = env.action_space.sample()    
    new_state, reward, done, info = env.step(action)
    state = new_state
    rewards_current_episode += reward 
    env.render()
    if done == True: 
        break
"""