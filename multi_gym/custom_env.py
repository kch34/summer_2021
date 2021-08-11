# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 12:18:06 2021

@author: Hostl
"""
import numpy as np
import gym
from gym import spaces

from custom_multi_agent_env import MEnv




class block_world(MEnv):
  """
  Custom Environment that follows gym interface.
  This is a simple env where the agent must learn to go always left. 
  """
  #color list
  colors  = {0:"red",1:"white",2:"blue",3:"black",4:"pink",5:"yellow"}
  #reward variables
  reward  = 0
  penalty = 0



  def __init__(self,rows,columns):
    super(block_world, self).__init__()
    #set the the normal board
    self.board = np.zeros((rows, columns))
    #set the goal board
    self.goal_board = np.zeros((rows, columns))    
    # Size of the 1D-grid
    self.grid_size = rows*columns    
    # Define action and observation space
    # They must be gym.spaces objects
    # Example when using discrete actions, we have two: left and right
    n_actions = 54
    self.action_space = spaces.Discrete(n_actions)
    # The observation will be the coordinate of the agent
    # this can be described both by Discrete and Box space
    self.observation_space = spaces.Box(low=0, high=self.grid_size,shape=(rows,columns), dtype=np.float32)

  def reset(self):
    """
    Important: the observation must be a numpy array
    :return: (np.array) 
    """
    # Initialize the agent at the right of the grid
    self.agent_pos = self.grid_size - 1
    # here we convert to float32 to make it more general (in case we want to use continuous actions)
    return np.array([self.agent_pos]).astype(np.float32)

  def step(self, action):
    if action == self.LEFT:
      self.agent_pos -= 1
    elif action == self.RIGHT:
      self.agent_pos += 1
    else:
      raise ValueError("Received invalid action={} which is not part of the action space".format(action))

    # Account for the boundaries of the grid
    self.agent_pos = np.clip(self.agent_pos, 0, self.grid_size)

    # Are we at the left of the grid?
    done = bool(self.agent_pos == 0)

    # Null reward everywhere except when reaching the goal (left of the grid)
    reward = 1 if self.agent_pos == 0 else 0

    # Optionally we can pass additional info, we are not using that for now
    info = {}

    return np.array([self.agent_pos]).astype(np.float32), reward, done, info

  #print the current board state
  def render(self):
     print("Current state")
     print(self.board[0])
     print(self.board[1])
     print(self.board[2])

  def close(self):
    pass