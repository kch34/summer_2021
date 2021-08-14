# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 12:18:06 2021

@author: Hostl
"""
import numpy as np
import gym
import random
import copy
from random import sample
from gym import Env, spaces
from gym.utils import seeding
from gym.envs.toy_text import discrete

"""
x = block_world(3,3)
x.render()
print(x.left_colors_needed)
print(x.right_colors_needed)
"""








class block_world(gym.Env):
  """
  Custom Environment that follows gym interface.
  This is a simple env where the agent must learn to go always left. 
  """
  #the board class
         
  #color list
  colors = {1:"black",2:"blue",3:"white",4:"red",5:"yellow",6:"pink"}
  #set the color list
  color_set = list(colors.keys())
  key_list = list(colors.keys())
  val_list = list(colors.values())
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
  legal_moves =  list(moves.keys())
  action_space = len(moves)

  def __init__(self,rows,columns):      
      
    self.reset()
     
        
    """
    #change left side to 1,3
    for i in range(3):
        if(int(self.goal_board[i][0])) in self.left_colors_needed:
            self.goal_board[i][0] = 1
        elif int(self.goal_board[i][0]) != 0:                        
            self.goal_board[i][0] = 3
            
    #change right side to 2,4
    for i in range(3):
        if(int(self.goal_board[i][2])) in self.right_colors_needed:
            self.goal_board[i][2] = 2
        elif int(self.goal_board[i][2]) != 0:
            self.goal_board[i][2] = 4
            
    #change left side to 1,3
    for i in range(3):
        if(int(self.board[i][2])) in self.left_colors_needed:
            self.board[i][2] = 1
        elif (int(self.board[i][2]) != 0) and ((not left_orphans_2)==False):
            if int(self.board[i][2]) in left_orphans_2:              
               self.board[i][2] = 3
    
    #change right side to 2,4
    for i in range(3):
        if(int(self.board[i][0])) in self.right_colors_needed:
            self.board[i][0] = 2
        elif (int(self.board[i][0]) != 0) and ((not right_orphans_2)==False):
            if int(self.board[i][0]) in right_orphans_2:              
               self.board[i][0] = 4
    """   
     
  def reset(self):
    """
    Important: the observation must be a numpy array
    :return: (np.array) 
    """
    rows     = 3
    columns  = 3
    #set the the normal board
    self.board = np.zeros((rows, columns)).astype(np.float32)
    #set the goal board
    self.goal_board = np.zeros((rows, columns)).astype(np.float32)   
    self.current_agent = 'left'

    current_colors = self.color_set.copy()
    random.shuffle(current_colors)
            
    self.left_colors_owned     = sample(current_colors,random.randint(1, 3))    
    for i in self.left_colors_owned:    
        current_colors.pop(current_colors.index(i))
    self.right_colors_owned    = sample(current_colors,random.randint(1, 3))  
    
    self.left_colors_needed    = sample(self.right_colors_owned,random.randint(1, len(self.right_colors_owned)))    
    self.right_colors_needed   = sample(self.left_colors_owned,random.randint(1, len(self.left_colors_owned)))

    self.left_colors_owned.sort()
    self.right_colors_owned.sort()
    self.left_colors_needed.sort()
    self.right_colors_needed.sort()

    for i in range(len(self.left_colors_owned)):
        self.board[i][0] = self.left_colors_owned[i]
        
    for i in range(len(self.right_colors_owned)):
        self.board[i][2] = self.right_colors_owned[i]

    self.goal_board = self.board.copy()

    add_left     = self.left_colors_needed.copy()
    add_right    = self.right_colors_needed.copy()
    left_orphans = []
    right_orphans = []
    #add left needed
    for i in range(3):
        if(((int(self.board[i][0])in self.right_colors_needed)==True)or(int(self.board[i][0])==0))and((not add_left)==False):
            self.goal_board[i][0] = add_left.pop(0)
    #add right needed
    for i in range(3):
        if(((int(self.board[i][2])in self.left_colors_needed)==True)or(int(self.board[i][2])==0))and((not add_right)==False):
            self.goal_board[i][2] = add_right.pop(0)
    #remove left dupliactes
    for i in range(3):
        if(int(self.goal_board[i][0])) in self.right_colors_needed:
            self.goal_board[i][0] = 0.0
    #remove right duplicates 
    for i in range(3):
        if(int(self.goal_board[i][2])) in self.left_colors_needed:
            self.goal_board[i][2] = 0.0
    
    #right needs to move orphans left
    if (not add_right)==False:
        #take out right orphans
        for i in range(3):
            if((int(self.board[i][2])in self.right_colors_needed)==False) and ((not add_right)==False):
                left_orphans.append(self.goal_board[i][2])
                self.goal_board[i][2] = add_right.pop(0)
        #add to left side
        for i in range(3):
            if (int(self.board[i][0]) == 0)and((not left_orphans)==False):
                self.goal_board[i][0] = left_orphans.pop(0)
    
    #left needs to move orphans left
    if (not add_left)==False:
        #take out left orphans
        for i in range(3):
            if((int(self.board[i][0])in self.left_colors_needed)==False) and ((not add_left)==False):
                right_orphans.append(self.goal_board[i][0])
                self.goal_board[i][0] = add_right.pop(0)
        #add to right side
        for i in range(3):
            if (int(self.board[i][2]) == 0)and((not right_orphans)==False):
                self.goal_board[i][2] = right_orphans.pop(0)    
    
    #change left side to 1,3
    for i in range(3):
        if(int(self.goal_board[i][0])) in self.left_colors_needed:
            self.goal_board[i][0] = 1
        elif int(self.goal_board[i][0]) != 0:
            self.goal_board[i][0] = 3
            
    #change right side to 2,4
    for i in range(3):
        if(int(self.goal_board[i][2])) in self.right_colors_needed:
            self.goal_board[i][2] = 2
        elif int(self.goal_board[i][2]) != 0:
            self.goal_board[i][2] = 4
        
    # here we convert to float32 to make it more general (in case we want to use continuous actions)    
    return self.board.flatten().copy()

  def step(self, action):
    reward = 0
      
    if (action in self.legal_moves):               
         decision = self.moves[action]           
         b_i = decision[0][0]
         b_j = decision[0][1]         
         l_i = decision[1][0]
         l_j = decision[1][1]
    else:
        raise ValueError("Received invalid action={} which is not part of the action space".format(action))        
     #move the block
    if self.board[l_i][l_j]==0.0 and self.board[b_i][b_j]!=0.0:
         #check for rewards         
         #moving a 1 or 3
         if ((self.board[b_i][b_j] == 1.0) or (self.board[b_i][b_j] == 3.0)):         
             if  ((b_j==2 and l_j==1) or (b_j==1 and l_j==0)):
                 reward +=  1
             elif((b_j==0 and l_j==1) or (b_j==1 and l_j==2)):
                 reward += -1
         #moving a 2 or 4
         if ((self.board[b_i][b_j] == 2.0) or (self.board[b_i][b_j] == 4.0)):         
             if  ((b_j==0 and l_j==1) or (b_j==1 and l_j==2)):
                 reward +=  1
             elif((b_j==2 and l_j==1) or (b_j==1 and l_j==0)):
                 reward += -1         
         temp                 = self.board[b_i][b_j].copy()
         self.board[b_i][b_j] = 0.0
         self.board[l_i][l_j] = temp.copy()
    else:
        reward+= -1
         
    temp = (self.board == self.goal_board)
        
    done = False
    if (False in temp)==False:
        done = True    
    # Null reward everywhere except when reaching the goal (left of the grid)
    reward += 20 if done == True else 0
    # Optionally we can pass additional info, we are not using that for now
    info = {}
    return self.board.flatten().copy(), reward, done, info

  #print the current board state
  def render(self, mode='console'):
     if mode != 'console':
        raise NotImplementedError()
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