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
  #the entire 54 set move list, indexed 0 to 53
  moves = {0:((0,0),(0,1)),   1:((0,1),(0,0)),  2:((0,2),(0,1)),
           3:((0,0),(1,1)),   4:((1,1),(0,0)),  5:((0,2),(1,1)),
           6:((0,0),(2,1)),   7:((2,1),(0,0)),  8:((0,2),(2,1)),
           
           9:((1,0),(0,1)),  10:((0,1),(1,0)), 11:((1,2),(0,1)),
           12:((1,0),(1,1)), 13:((1,1),(1,0)), 14:((1,2),(1,1)),
           15:((1,0),(2,1)), 16:((2,1),(1,0)), 17:((1,2),(2,1)), 
           
           18:((2,0),(0,1)), 19:((0,1),(2,0)), 20:((2,2),(0,1)),
           21:((2,0),(1,1)), 22:((1,1),(2,0)), 23:((2,2),(1,1)),
           24:((2,0),(2,1)), 25:((2,1),(2,0)), 26:((2,2),(2,1)),
           
           
           
           27:((0,2),(0,1)), 28:((0,1),(0,2)), 29:((0,0),(0,1)),
           30:((0,2),(1,1)), 31:((1,1),(0,2)), 32:((0,0),(1,1)),
           33:((0,2),(2,1)), 34:((2,1),(0,2)), 35:((0,0),(2,1)),
           
           36:((1,2),(0,1)), 37:((0,1),(1,2)), 38:((1,0),(0,1)),
           39:((1,2),(1,1)), 40:((1,1),(1,2)), 41:((1,0),(1,1)),
           42:((1,2),(2,1)), 43:((2,1),(1,2)), 44:((1,0),(2,1)),
           
           45:((2,2),(0,1)), 46:((0,1),(2,2)), 47:((2,0),(0,1)),
           48:((2,2),(1,1)), 49:((1,1),(2,2)), 50:((2,0),(1,1)),
           51:((2,2),(2,1)), 52:((2,1),(2,2)), 53:((2,0),(2,1))   }


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
     print("---------- ")
     print("Current state")
     print(self.board[0])
     print(self.board[1])
     print(self.board[2])
     print(" ")
     print("Goal State")
     print(self.goal_board[0])
     print(self.goal_board[1])
     print(self.goal_board[2]) 
     print("---------- ")

  def close(self):
    pass