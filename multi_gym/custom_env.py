# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 12:18:06 2021

@author: Hostl
"""
import numpy as np
import gym
from gym import spaces
import random
import copy
from custom_multi_agent_env import MEnv


"""
x = block_world(3,3)
x.render()
print(x.left_blocks_needed)
print(x.right_blocks_needed)
"""


class block_world(MEnv):
  """
  Custom Environment that follows gym interface.
  This is a simple env where the agent must learn to go always left. 
  """
  #the board class
         
  #color list
  colors = {1:"black",2:"blue",3:"white",4:"red",5:"yellow",6:"pink"}
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
  


  def __init__(self,rows,columns):
    super(block_world, self).__init__()
    #set the the normal board
    self.board = np.zeros((rows, columns)).astype(np.float32)
    #set the goal board
    self.goal_board = np.zeros((rows, columns)).astype(np.float32)   
    # Size of the 1D-grid
    self.grid_size = rows*columns    
    self.current_agent = 'left'
    # Define action and observation space
    # They must be gym.spaces objects
    # Example when using discrete actions, we have two: left and right
    n_actions = 54
    self.action_space = spaces.Discrete(n_actions)
    # The observation will be the coordinate of the agent
    # this can be described both by Discrete and Box space
    self.observation_space = spaces.Box(low=0, high=self.grid_size,shape=(rows,columns), dtype=np.float32)

    
    #now we set the actual grid blocks with randomization
    #we set the current color set to be used
    color_set = list(self.colors.values())
    #We make sure we shuffle the list each time
    random.shuffle(color_set)
    #set the amount of starting colors for both agents
    start_color1 = random.randint(1, 3)
    start_color2 = random.randint(1, 3)
    #set the starting colors
    start_block1 = []
    start_block2 = []
    #set the starting colors for the first agent
    for i in range(start_color1):            
        start_block1.append(color_set.pop(0))
    start_block1.sort()
    #set the starting colors for the second agent
    for i in range(start_color2):            
        start_block2.append(color_set.pop(0))
    start_block2.sort()
    #set the amount of colors needed for both agents
    color1 = random.randint(1, len(start_block2))
    color2 = random.randint(1, len(start_block1))
    #set what the colors needed are for the first agent
    color_needed1 = []        
    temp = start_block2.copy()
    random.shuffle(temp)
    for i in range(color1):
        color_needed1.append(temp.pop(0))
    #set what the colors needed are for the second agent
    color_needed2 = []        
    temp = start_block1.copy()
    random.shuffle(temp)
    for i in range(color2):
        color_needed2.append(temp.pop(0))
        
    self.left_blocks_start  =  start_block1.copy()
    self.left_blocks_needed =  color_needed1.copy()
    
    self.right_blocks_start = start_block2.copy()
    self.right_blocks_needed =  color_needed2.copy()
    
    #set the blocks on the board for each agent
    for i in range(len(self.left_blocks_start)):             
        value    = self.key_list[self.val_list.index(self.left_blocks_start[i])]
        position = (i,0)
        self.board[position] = value

    for i in range(len(self.right_blocks_start)):
        value    = self.key_list[self.val_list.index(self.right_blocks_start[i])]
        position = (i,2)
        self.board[position] = value
        
         
    #set temp needed values for the goal state                    
    needed1   = self.left_blocks_needed.copy()
    needed1_1 = self.left_blocks_needed.copy()
    needed2   = self.right_blocks_needed.copy()
    needed2_2 = self.right_blocks_needed.copy()
    #make a copy of the board state for the goal.
    self.goal_board = copy.deepcopy(self.board)    
    add_left = []
    add_right =[]        
    for i in range(3):
        if self.val_list[int(self.goal_board[i][0]-1)] in needed2_2:
            self.goal_board[i][0] = 0.0         
    for i in range(3):
        if self.val_list[int(self.goal_board[i][2]-1)] in needed1_1:
            self.goal_board[i][2] = 0.0
    while (not needed1_1) == False:
        #try to add in the needed
        for i in range(3):
            if self.goal_board[i][0] == 0.0 and (not needed1_1) == False:
                self.goal_board[i][0] = self.key_list[self.val_list.index(needed1_1.pop(0))]
        #if needed isn't empty then check for orphans
        if (not needed1_1) == False:
            for i in range(3):
                if (self.val_list[int(self.goal_board[i][0]-1)] in needed1) == False:
                    add_right.append(self.goal_board[i][0])
                    self.goal_board[i][0] = 0.0
    while (not needed2_2) == False:
        #try to add in the needed
        for i in range(3):
            if self.goal_board[i][2] == 0.0 and (not needed2_2) == False:
                self.goal_board[i][2] = self.key_list[self.val_list.index(needed2_2.pop(0))]
        #if needed isn't empty then check for orphans
        if (not needed2_2) == False:
            for i in range(3):
                if (self.val_list[int(self.goal_board[i][2]-1)] in needed2) == False:
                    add_left.append(self.goal_board[i][2])
                    self.goal_board[i][2] = 0.0
                    break
    if (not add_left) == False:
        for i in range(3):
            if self.goal_board[i][0] == 0.0 and (not add_left) == False:
                self.goal_board[i][0] = add_left.pop(0)           
    if (not add_right) == False:
        for i in range(3):
            if self.goal_board[i][2] == 0.0 and (not add_right) == False:
                self.goal_board[i][2] = add_right.pop(0)      
    #set the numeric values for colors owned and needed for both of them
    #Set the first agents colors needed as numerics
    temp = []
    for i in self.left_blocks_needed:
        temp.append(self.key_list[self.val_list.index(i)])
    self.left_blocks_needed = temp.copy()
    #set the first agents colors owned as numerics
    temp = []
    for i in self.left_blocks_start:
        temp.append(self.key_list[self.val_list.index(i)])
    self.left_blocks_start = temp.copy()
    #Set the second agents colors needed as numerics
    temp = []
    for i in self.right_blocks_needed:
        temp.append(self.key_list[self.val_list.index(i)])
    self.right_blocks_needed = temp.copy()
    #set the second agents colors owned as numerics
    temp = []
    for i in self.right_blocks_start:
        temp.append(self.key_list[self.val_list.index(i)])
    self.left_blocks_start = temp.copy()
    
    self.left_blocks_owned = self.left_blocks_start.copy()
    self.right_blocks_owned = self.right_blocks_start.copy()
    
    
    
    #orphan lists
    self.left_orphans   = []
    self.right_orphans  = []

    #set the oprhans for later checking
    if ((self.goal_board[0][0] in self.left_blocks_needed)== False  )and (self.goal_board[0][0] != 0.0):
        self.left_orphans.append(self.goal_board[0][0])
    if ((self.goal_board[1][0] in self.left_blocks_needed) == False )and (self.goal_board[1][0] != 0.0):
        self.left_orphans.append(self.goal_board[1][0])
    if ((self.goal_board[2][0] in self.left_blocks_needed) == False )and (self.goal_board[2][0] != 0.0):
        self.left_orphans.append(self.goal_board[2][0])
        
    if ((self.goal_board[0][2] in self.right_blocks_owned) == False )and (self.goal_board[0][2] != 0.0):
        self.right_orphans.append(self.goal_board[0][2])
    if ((self.goal_board[1][2] in self.right_blocks_owned) == False )and (self.goal_board[1][2] != 0.0):
        self.right_orphans.append(self.goal_board[1][2])
    if ((self.goal_board[2][2] in self.right_blocks_owned) == False )and (self.goal_board[2][2] != 0.0):
        self.right_orphans.append(self.goal_board[2][2])
        
    
    for i in range(3):
        x = self.goal_board[i][0]        
        if   (int(x) in self.left_blocks_needed) == True:
                self.goal_board[i][0] = 1.0
        elif (float(x) in self.left_orphans) == True:
                self.goal_board[i][0] = 3.0
    
    for i in range(3):
        x = self.goal_board[i][2]        
        if   (int(x) in self.right_blocks_needed) == True:
                self.goal_board[i][2] = 2.0
        elif (float(x) in self.right_orphans) == True:
                self.goal_board[i][2] = 4.0
    
    
    for i in range(3):
        for j in range(3):
            x = self.board[i][j]        
            if   (int(x) in self.left_blocks_needed) == True:
                self.board[i][j] = 1.0
            elif (float(x) in self.left_orphans) == True:
                self.board[i][j] = 3.0
            elif (int(x) in self.right_blocks_needed) == True:
                self.board[i][j] = 2.0
            elif (float(x) in self.right_orphans) == True:
                self.board[i][j] = 4.0
     
    
    
    
    
 
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
    # Size of the 1D-grid
    self.grid_size = rows*columns    
    self.current_agent = 'left'
    # Define action and observation space
    # They must be gym.spaces objects
    # Example when using discrete actions, we have two: left and right
    n_actions = 54
    self.action_space = spaces.Discrete(n_actions)
    # The observation will be the coordinate of the agent
    # this can be described both by Discrete and Box space
    self.observation_space = spaces.Box(low=0, high=self.grid_size,shape=(rows,columns), dtype=np.float32)

    
    #now we set the actual grid blocks with randomization
    #we set the current color set to be used
    color_set = list(self.colors.values())
    #We make sure we shuffle the list each time
    random.shuffle(color_set)
    #set the amount of starting colors for both agents
    start_color1 = random.randint(1, 3)
    start_color2 = random.randint(1, 3)
    #set the starting colors
    start_block1 = []
    start_block2 = []
    #set the starting colors for the first agent
    for i in range(start_color1):            
        start_block1.append(color_set.pop(0))
    start_block1.sort()
    #set the starting colors for the second agent
    for i in range(start_color2):            
        start_block2.append(color_set.pop(0))
    start_block2.sort()
    #set the amount of colors needed for both agents
    color1 = random.randint(1, len(start_block2))
    color2 = random.randint(1, len(start_block1))
    #set what the colors needed are for the first agent
    color_needed1 = []        
    temp = start_block2.copy()
    random.shuffle(temp)
    for i in range(color1):
        color_needed1.append(temp.pop(0))
    #set what the colors needed are for the second agent
    color_needed2 = []        
    temp = start_block1.copy()
    random.shuffle(temp)
    for i in range(color2):
        color_needed2.append(temp.pop(0))
        
    self.left_blocks_start  =  start_block1.copy()
    self.left_blocks_needed =  color_needed1.copy()
    
    self.right_blocks_start = start_block2.copy()
    self.right_blocks_needed =  color_needed2.copy()
    
    #set the blocks on the board for each agent
    for i in range(len(self.left_blocks_start)):             
        value    = self.key_list[self.val_list.index(self.left_blocks_start[i])]
        position = (i,0)
        self.board[position] = value

    for i in range(len(self.right_blocks_start)):
        value    = self.key_list[self.val_list.index(self.right_blocks_start[i])]
        position = (i,2)
        self.board[position] = value
        
         
    #set temp needed values for the goal state                    
    needed1   = self.left_blocks_needed.copy()
    needed1_1 = self.left_blocks_needed.copy()
    needed2   = self.right_blocks_needed.copy()
    needed2_2 = self.right_blocks_needed.copy()
    #make a copy of the board state for the goal.
    self.goal_board = copy.deepcopy(self.board)    
    add_left = []
    add_right =[]        
    for i in range(3):
        if self.val_list[int(self.goal_board[i][0]-1)] in needed2_2:
            self.goal_board[i][0] = 0.0         
    for i in range(3):
        if self.val_list[int(self.goal_board[i][2]-1)] in needed1_1:
            self.goal_board[i][2] = 0.0
    while (not needed1_1) == False:
        #try to add in the needed
        for i in range(3):
            if self.goal_board[i][0] == 0.0 and (not needed1_1) == False:
                self.goal_board[i][0] = self.key_list[self.val_list.index(needed1_1.pop(0))]
        #if needed isn't empty then check for orphans
        if (not needed1_1) == False:
            for i in range(3):
                if (self.val_list[int(self.goal_board[i][0]-1)] in needed1) == False:
                    add_right.append(self.goal_board[i][0])
                    self.goal_board[i][0] = 0.0
    while (not needed2_2) == False:
        #try to add in the needed
        for i in range(3):
            if self.goal_board[i][2] == 0.0 and (not needed2_2) == False:
                self.goal_board[i][2] = self.key_list[self.val_list.index(needed2_2.pop(0))]
        #if needed isn't empty then check for orphans
        if (not needed2_2) == False:
            for i in range(3):
                if (self.val_list[int(self.goal_board[i][2]-1)] in needed2) == False:
                    add_left.append(self.goal_board[i][2])
                    self.goal_board[i][2] = 0.0
                    break
    if (not add_left) == False:
        for i in range(3):
            if self.goal_board[i][0] == 0.0 and (not add_left) == False:
                self.goal_board[i][0] = add_left.pop(0)           
    if (not add_right) == False:
        for i in range(3):
            if self.goal_board[i][2] == 0.0 and (not add_right) == False:
                self.goal_board[i][2] = add_right.pop(0)      
    #set the numeric values for colors owned and needed for both of them
    #Set the first agents colors needed as numerics
    temp = []
    for i in self.left_blocks_needed:
        temp.append(self.key_list[self.val_list.index(i)])
    self.left_blocks_needed = temp.copy()
    #set the first agents colors owned as numerics
    temp = []
    for i in self.left_blocks_start:
        temp.append(self.key_list[self.val_list.index(i)])
    self.left_blocks_start = temp.copy()
    #Set the second agents colors needed as numerics
    temp = []
    for i in self.right_blocks_needed:
        temp.append(self.key_list[self.val_list.index(i)])
    self.right_blocks_needed = temp.copy()
    #set the second agents colors owned as numerics
    temp = []
    for i in self.right_blocks_start:
        temp.append(self.key_list[self.val_list.index(i)])
    self.left_blocks_start = temp.copy()
    
    self.left_blocks_owned = self.left_blocks_start.copy()
    self.right_blocks_owned = self.right_blocks_start.copy()
    
    #orphan lists
    self.left_orphans   = []
    self.right_orphans  = []

    #set the oprhans for later checking
    if ((self.goal_board[0][0] in self.left_blocks_needed)== False  )and (self.goal_board[0][0] != 0.0):
        self.left_orphans.append(self.goal_board[0][0])
    if ((self.goal_board[1][0] in self.left_blocks_needed) == False )and (self.goal_board[1][0] != 0.0):
        self.left_orphans.append(self.goal_board[1][0])
    if ((self.goal_board[2][0] in self.left_blocks_needed) == False )and (self.goal_board[2][0] != 0.0):
        self.left_orphans.append(self.goal_board[2][0])
        
    if ((self.goal_board[0][2] in self.right_blocks_owned) == False )and (self.goal_board[0][2] != 0.0):
        self.right_orphans.append(self.goal_board[0][2])
    if ((self.goal_board[1][2] in self.right_blocks_owned) == False )and (self.goal_board[1][2] != 0.0):
        self.right_orphans.append(self.goal_board[1][2])
    if ((self.goal_board[2][2] in self.right_blocks_owned) == False )and (self.goal_board[2][2] != 0.0):
        self.right_orphans.append(self.goal_board[2][2])
        
    
    for i in range(3):
        x = self.goal_board[i][0]        
        if   (int(x) in self.left_blocks_needed) == True:
                self.goal_board[i][0] = 1.0
        elif (float(x) in self.left_orphans) == True:
                self.goal_board[i][0] = 3.0
    
    for i in range(3):
        x = self.goal_board[i][2]        
        if   (int(x) in self.right_blocks_needed) == True:
                self.goal_board[i][2] = 2.0
        elif (float(x) in self.right_orphans) == True:
                self.goal_board[i][2] = 4.0
    
    
    for i in range(3):
        for j in range(3):
            x = self.board[i][j]        
            if   (int(x) in self.left_blocks_needed) == True:
                self.board[i][j] = 1.0
            elif (float(x) in self.left_orphans) == True:
                self.board[i][j] = 3.0
            elif (int(x) in self.right_blocks_needed) == True:
                self.board[i][j] = 2.0
            elif (float(x) in self.right_orphans) == True:
                self.board[i][j] = 4.0
        
    # here we convert to float32 to make it more general (in case we want to use continuous actions)    
    return np.array([self.board]).astype(np.float32)

  def step(self, action):
      
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
         temp                 = self.board[b_i][b_j]
         self.board[b_i][b_j] = 0.0
         self.board[l_i][l_j] = temp
         
    temp = (self.board == self.goal_board)
    
    
    done = False
    if (False in temp)==False:
        done = True
    
    # Null reward everywhere except when reaching the goal (left of the grid)
    reward = 1 if done == True else 0

    # Optionally we can pass additional info, we are not using that for now
    info = {}

    return np.array([self.board]).astype(np.float32), reward, done, info

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