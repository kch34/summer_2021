# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 12:28:22 2021
@author: Hostl
"""
#imports
from multiprocessing import freeze_support  #needed due to windows 
from multiprocessing.dummy import Pool as ThreadPool
import multiprocessing as mp
from joblib import Parallel, delayed
import pickle
#import sys, torch, copy, time, os, torchvision, gc   
#import torch.nn as nn
import random
import torch
import time
#import statistics
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np
import copy
from tqdm import tqdm
#set the size of the board
BOARD_ROWS = 3
BOARD_COLS = 3
#set the color dictionary
colors = {1:"black",2:"blue",3:"white",4:"red",5:"yellow",6:"pink"}
key_list = list(colors.keys())
val_list = list(colors.values())
totalblocks = []
totalturns = []
w_turns    = []
score_log = []
game_log = []
show_chat = True
epochs = 0
#the board class
class State:
    #initialize the state 
    def __init__(self):
        self.board = np.zeros((BOARD_ROWS, BOARD_COLS))
        self.goal_board = np.zeros((BOARD_ROWS, BOARD_COLS))
        self.boardHash = None
    # board reset
    def reset(self):
        self.board = np.zeros((BOARD_ROWS, BOARD_COLS))
        self.goal_board = np.zeros((BOARD_ROWS, BOARD_COLS))
        self.boardHash = None
    # get unique hash of current board state
    def getHash(self):
        self.boardHash = str(self.board.reshape(BOARD_COLS * BOARD_ROWS))
        return self.boardHash
    #update the state
    def updateState(self, position,value):
        self.board[position] = value
    #print the current board state
    def print_current(self):
        print("Current state")
        print(self.board[0])
        print(self.board[1])
        print(self.board[2])
    #print the goal board state
    def print_goal(self):
        print("Goal State")
        print(self.goal_board[0])
        print(self.goal_board[1])
        print(self.goal_board[2])        
    #initialize the state 
    def __init__(self):
        self.board = np.zeros((BOARD_ROWS, BOARD_COLS))
        self.goal_board = np.zeros((BOARD_ROWS, BOARD_COLS))
        self.boardHash = None
    # board reset
    def reset(self):
        self.board = np.zeros((BOARD_ROWS, BOARD_COLS))
        self.goal_board = np.zeros((BOARD_ROWS, BOARD_COLS))
        self.boardHash = None
    #update the state
    def updateState(self, position,value):
        self.board[position] = value
    #print the current board state
    def print_current(self):
        print("Current state")
        print(self.board[0])
        print(self.board[1])
        print(self.board[2])
    #print the goal board state
    def print_goal(self):
        print("Goal State")
        print(self.goal_board[0])
        print(self.goal_board[1])
        print(self.goal_board[2])        
#agent class
class botty:
    def reset(self,blocks, colors_needed):
        self.blocks = blocks
        self.colors_owned = blocks
        self.colors_needed = colors_needed
        self.was_asked            = False
        self.checked_for_asked    = False
        self.checked_my_needed    = False
        self.checked_their_needed = False
        self.checked_for_orphans  = False
        self.checked_zero         = False
        self.checked_middle       = False
        self.checked_self         = False
        self.reward               = 0.0
        self.motive               = 0.0
        self.ask_motive           = 0.0
        self.give_motive          = 0.0
        self.take_motive          = 0.0
        self.try_to_ask_motive    = 0.0 
        self.done                 = False
        self.has_needed           = False
        self.oprhan_logged        = False
        self.my_orphans              = []
        self.their_orphans           = []
    #initialize the robot with name blocks owned and needed
    def __init__(self, name):
        self.name = name        
        self.done                 = False
        self.has_needed           = False
        self.check_asked          = 1/2
        self.try_to_give          = 1/3
        self.try_to_take          = 1/3
        self.try_to_ask           = 1/3
        self.check_my_needed      = 1/2
        self.check_their_needed   = 1/2
        self.check_their_needed2  = 1/2
        self.motive               = 0.0
        self.ask_motive           = 0.0
        self.give_motive          = 0.0
        self.take_motive          = 0.0
        self.try_to_ask_motive    = 0.0      
        self.check_zero           = 1/2
        self.check_middle         = 1/2
        self.check_self           = 1/2
        self.check_asked_color    = 1/2
        self.check_game_complete  = 1/2
        self.forward_think        = 1/2
        self.orphan_check         = 1/2
        self.orphan_logged        = False
        self.checked_self         = False
        self.my_orphans              = []
        self.their_orphans           = []
        self.checked_middle       = False
        self.checked_zero         = False
        self.was_asked            = False
        self.checked_for_asked    = False
        self.checked_my_needed    = False
        self.checked_their_needed = False
        self.checked_for_orphans  = False
        self.reward               = 0.0
    #return the colors owned
    def get_colors_owned(self):
        return self.colors_owned
    #return the colors needed
    def get_colors_needed(self):
        return self.colors_needed
    #set the colors owned
    def set_colors_owned(self,x):
        self.colors_owned = x
    #set the colors needed
    def set_colors_needed(self,x):
        self.colors_needed = x
    #set that the agent is done and ready to quit
    def set_done(self,x):
        self.done = x
#blank exception class used for breaking double loops
class Found(Exception): pass
#create the two agents
#initialize both agents
robot1 = botty('taysir')
robot2 = botty('zach')
#the main code to be used for looping
def pro(robot1,robot2):
    #need this for multithreading
    #if __name__ == '__main__':
        #used for multithreading
        #freeze_support()        
        #the main board to be manipulated
        board = State()
        #we set the current color set to be used
        color_set = list(colors.values())
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
        #reset both agents
        robot1.reset(start_block1,color_needed1)
        robot2.reset(start_block2,color_needed2)
        #set the blocks on the board for each agent
        for i in range(len(robot1.blocks)):              
            board.updateState((i,0), key_list[val_list.index(robot1.blocks[i])])
        for i in range(len(robot2.blocks)):
            board.updateState((i,2), key_list[val_list.index(robot2.blocks[i])])            
        #set temp needed values for the goal state                    
        needed1 = robot1.colors_needed.copy()
        needed1_1 = robot1.colors_needed.copy()
        needed2 = robot2.colors_needed.copy()
        needed2_2 = robot2.colors_needed.copy()
        #make a copy of the board state for the goal.
        board.goal_board = copy.deepcopy(board.board)    
        add_left = []
        add_right =[]        
        for i in range(3):
            if val_list[int(board.goal_board[i][0]-1)] in needed2_2:
                board.goal_board[i][0] = 0.0         
        for i in range(3):
            if val_list[int(board.goal_board[i][2]-1)] in needed1_1:
                board.goal_board[i][2] = 0.0
        while (not needed1_1) == False:
            #try to add in the needed
            for i in range(3):
                if board.goal_board[i][0] == 0.0 and (not needed1_1) == False:
                    board.goal_board[i][0] = key_list[val_list.index(needed1_1.pop(0))]
            #if needed isn't empty then check for orphans
            if (not needed1_1) == False:
                for i in range(3):
                    if (val_list[int(board.goal_board[i][0]-1)] in needed1) == False:
                        add_right.append(board.goal_board[i][0])
                        board.goal_board[i][0] = 0.0
        while (not needed2_2) == False:
            #try to add in the needed
            for i in range(3):
                if board.goal_board[i][2] == 0.0 and (not needed2_2) == False:
                    board.goal_board[i][2] = key_list[val_list.index(needed2_2.pop(0))]
            #if needed isn't empty then check for orphans
            if (not needed2_2) == False:
                for i in range(3):
                    if (val_list[int(board.goal_board[i][2]-1)] in needed2) == False:
                        add_left.append(board.goal_board[i][2])
                        board.goal_board[i][2] = 0.0
                        break
        if (not add_left) == False:
            for i in range(3):
                if board.goal_board[i][0] == 0.0 and (not add_left) == False:
                    board.goal_board[i][0] = add_left.pop(0)           
        if (not add_right) == False:
            for i in range(3):
                if board.goal_board[i][2] == 0.0 and (not add_right) == False:
                    board.goal_board[i][2] = add_right.pop(0)      
        #testing
        if show_chat == True:            
            board.print_current()
            board.print_goal()
            print(robot1.colors_needed)
            print(robot2.colors_needed)
        #set the numeric values for colors owned and needed for both of them
        #Set the first agents colors needed as numerics
        temp = []
        for i in robot1.colors_needed:
            temp.append(key_list[val_list.index(i)])
        robot1.set_colors_needed(temp)
        #set the first agents colors owned as numerics
        temp = []
        for i in robot1.colors_owned:
            temp.append(key_list[val_list.index(i)])
        robot1.set_colors_owned(temp)
        #Set the second agents colors needed as numerics
        temp = []
        for i in robot2.colors_needed:
            temp.append(key_list[val_list.index(i)])
        robot2.set_colors_needed(temp)
        #set the second agents colors owned as numerics
        temp = []
        for i in robot2.colors_owned:
            temp.append(key_list[val_list.index(i)])
        robot2.set_colors_owned(temp)
        #orphan lists
        robot1_orphans = []
        robot2_orphans = []

        #set the oprhans for later checking
        if ((board.goal_board[0][0] in robot1.colors_needed) == False )and (not 0.0):
            robot1_orphans.append(board.goal_board[0][0])
        if ((board.goal_board[1][0] in robot1.colors_needed) == False )and (not 0.0):
            robot1_orphans.append(board.goal_board[1][0])
        if ((board.goal_board[2][0] in robot1.colors_needed) == False )and (not 0.0):
            robot1_orphans.append(board.goal_board[2][0])
            
        if ((board.goal_board[0][2] in robot2.colors_needed) == False )and (not 0.0):
            robot2_orphans.append(board.goal_board[0][2])
        if ((board.goal_board[1][2] in robot2.colors_needed) == False )and (not 0.0):
            robot2_orphans.append(board.goal_board[1][2])
        if ((board.goal_board[2][2] in robot2.colors_needed) == False )and (not 0.0):
            robot2_orphans.append(board.goal_board[2][2])
            
        robot1_orphans = robot1_orphans.sort()
        robot2_orphans = robot2_orphans.sort()
        
        
        if robot1_orphans != [] or robot2_orphans != []:
            orphans_exist = True
        else:
            orphans_exist = False





        #the reinforcement learning heuristic
        def rl_forward_think(agent,agent2,input_msg,side,show_chat,robot1_orphans,robot2_orphans,orphans_exist):
            #get agent1's features
            agent_owned = agent.colors_owned.copy()
            agent_needed = agent.colors_needed.copy()
            #get agent1's features
            agent2_owned = agent2.colors_owned.copy()
            agent2_needed = agent2.colors_needed.copy()
            #random actions
            #flags for  logic
            agent_needs_blocks         = False
            agent_can_take_blocks      = False       
            agent_has_agent2_blocks    = False
            #flags for  logic
            agent2_needs_blocks         = False
            agent2_can_take_blocks      = False  
            #reset the agents motives to zero
            agent.motive               = 0.0
            agent.ask_motive           = 0.0
            agent.give_motive          = 0.0
            agent.take_motive          = 0.0
            agent.try_to_ask_motive    = 0.0
            #reset the agents flags to default false
            agent.checked_middle       = False
            agent.checked_zero         = False 
            agent.was_asked            = False
            agent.checked_for_asked    = False
            agent.checked_my_needed    = False
            agent.checked_their_needed = False
            agent.checked_for_orphans  = False
            #reset the agents rewards for the current actions
            agent.reward               = 0.0                        
            #Does the agent need a block?
            for b in agent_needed:
                if (b in agent_owned) == False:
                    agent_needs_blocks = True
                    break
            if agent_needs_blocks == True:
                if show_chat == True:
                    print("I need blocks.")
            #can the agent take blocks?
            if len(agent_owned) < 3:
                agent_can_take_blocks = True 
                if show_chat == True:
                    print("I have room to take blocks.")                 
            #set the done state if the agent has needed blocks.
            if agent_needs_blocks == False:
                agent.set_done(True)                          

            #Find out which agent we have
            if side == "left":
                agent1_side = 0
                agent2_side = 2
            else:
                agent1_side = 2
                agent2_side = 0



            binary_decision = 0.50
            color_asked = " "
        
            #logic for finding out if the agent was asked a question
            
            #find out if the agent was asked to moved a block                      
            #grab the last msg
            msg_list = input_msg.split()
            #find the action verb            
            action = msg_list[0]            
            #check if the action verb implies a 
            if action == "move":
                #if the action verb was a question to move          
                #set the color that was asked
                color_asked = msg_list[1]
                #Set the color to numerical value
                color_asked = key_list[val_list.index(color_asked)]                 
            #choice to check for a question input msg                
            check_asked_choice = random.random()
            #decides to check the input msg 
            if ((check_asked_choice + agent.check_asked) >=  binary_decision):
                #flag for moving a block asked by the other agent
                agent.checked_for_asked = True  
                #we check if a question was asked
                if action == "move":
                    #if a question was asked then we want to increase the chance to happen again
                    agent.check_asked += 0.01
                    #set more motive to give
                    agent.give_motive += 0.15
                    #set the flag that agent was asked to move a block
                    agent.was_asked = True
                else:
                    #always reinforce the fact that the agent checked for a question to encourage communication
                    agent.check_asked += 0.01            
                    #set the flag that agent was asked to move a block
                    agent.was_asked = False                                     
            else:
                #flag for moving a block asked by the other agent
                agent.checked_for_asked = False 
                 #we check if a question was asked
                if action == "move":
                    #set the flag that agent was asked to move a block
                    agent.was_asked = True
                                                  


            #check if other agent needs any blocks
            choice_check_their_needed = random.random()
            if(choice_check_their_needed <= agent.check_their_needed):
                #reward
                agent.check_their_needed+= 0.01
                #check their needed
                #Does the agent need a block?
                for b in agent2_needed:
                    if (b in agent2_owned) == False:
                        agent2_needs_blocks = True
                        break            
                #check if other agent needs any blocks
                choice_check2 = random.random()
                if choice_check2 <= agent.check_their_needed2:
                    agent.check_their_needed2+= 0.01
                    for b in agent2_needed:
                        if (b in agent_owned) == True:
                            agent_has_agent2_blocks = True
                            break



            #game completion check
            choice_check_game = random.random()
            #game completion decision
            if choice_check_game <= agent.check_game_complete:
                #are the agents needs met?
                if(agent_needs_blocks==False):
                    #reward
                    agent.check_game_complete+=0.01
                    #set the agent to be done
                    agent.set_done(True)
                    #agent has it's needed
                    agent.has_needed = True
                    #
                    agent.try_to_ask_motive += 0.05
                    agent.take_motive       += 0.05  
                else:
                    #set the agent to not done
                    agent.set_done(False)
                    #agent doesnt have what it needs
                    agent.has_needed = False
                #forward thinking decision
                choice_forward_think = random.random()
                #forward think decision
                if choice_forward_think <= agent.forward_think:
                    #reward
                    agent.forward_think+=0.01
                    #forward thinking decision
                    choice_orphan_check = random.random()
                    #forward think decision
                    if choice_orphan_check <= agent.orphan_check:
                        #reward
                        agent.orphan_check+=0.01
                        #go through and log orphans
                        if agent.orphan_logged == False:                            
                            for i in range(3):
                                for j in range(3):
                                    if(board.board[i][j] != 0.0):
                                        if (board.board[i][j] in agent2_needed) == False:
                                            if (board.board[i][j] in agent_needed) == False:
                                                agent.my_orphans.append(board.board[i][j])                                                
                            agent.my_orphans = agent.my_orphans.sort()                    
                            if side == "left":
                                if agent.my_orphans == robot1_orphans:
                                    agent.orphan_logged = True
                                    #reward
                                    agent.orphan_check+=0.05
                            elif side == "right":
                                if agent.my_orphans == robot2_orphans:
                                    agent.orphan_logged = True
                            else:
                                agent.orphan_logged = False
                                agent.my_orphans = []
                            
                                        
            

            #if the agent was asked to move encourge the agent to move as first attempt
            if((agent.checked_for_asked==True)and(agent.was_asked==True)):
                agent.give_motive       += 0.15
            elif((agent_needs_blocks==True)and(agent_can_take_blocks==True)):
                agent.take_motive       += 0.15
            elif((agent_needs_blocks==False)and(agent_can_take_blocks==True)):
                agent.try_to_ask_motive += 0.15
                
            #decide to check the middle
            m_choice = random.random()
            if (m_choice <= agent.check_middle):
                agent.check_middle+=0.01
                if (0.0 in middle) == False:
                    agent.take_motive       += 0.20                
                                                
            #the decision loop
            while True:                            
                agent.motive = 0.0
                #set the choice parameters
                first = (agent.try_to_give+agent.give_motive)
                second = (agent.try_to_take+agent.take_motive)
                third = (agent.try_to_ask+agent.try_to_ask_motive)

                mylist = ['give', 'take', 'ask']                                
                choice = random.choices(mylist, weights = [first, second, third], k = 1)    
                choice = choice[0]
                
                if (choice == 'give'):
                    #set the chance to run this again to slimtonone
                    #agent.give_motive = 
                    j = agent1_side
                    #go through the current agents blocks
                    for i in range(3):
                      agent.motive = 0.0
                      z_choice = random.random()
                      m_choice = random.random()
                      c_choice = random.random()
                      c_choice2 = random.random()
                      choice_orphan_check = random.random()
                      choice2 = random.random()
                      #zero value
                      #decide to check if the block is zero
                      if (z_choice <= agent.check_zero):
                          agent.check_zero+= 0.01
                          #smack if the agent tries to take a zero
                          if(board.board[i][j] == 0.0):
                            agent.check_zero+= 0.05
                            agent.motive+= -0.35                            
                      #check if the middle is full
                      if (m_choice <= agent.check_middle):
                        agent.check_middle+=0.01
                        if (0.0 in middle) == False:
                            agent.check_middle+=0.05
                            agent.motive+= -0.35                            
                      #check if agent needs the block
                      #choice to check own blocks                      
                      if (c_choice <= agent.check_my_needed):
                          #give a reinforcemnt
                          agent.check_my_needed += 0.01
                          #do i need the block?
                          if (board.board[i][j] in agent.colors_needed) == True:
                              #the current agent does need it                              
                              #give a reinforcemnt
                              agent.check_my_needed += 0.05
                              #set the motive much lower to not move the block
                              agent.motive += -0.35  
                      #check if they need 
                      if agent_has_agent2_blocks == True:
                          c_choice2 += -0.35
                      if (c_choice2 <= agent.check_their_needed):
                          #give a reinforcemnt
                          agent.check_their_needed += 0.01
                          #do they need the block?
                          if (board.board[i][j] in agent2.colors_needed) == True:                              
                              #the other agent does need it
                              #give a reinforcemnt
                              agent.check_their_needed += 0.05
                              #set the motive much higher to move the block
                              agent.motive += 0.35
                      #asked_check
                      if((agent.checked_for_asked==True)and(agent.was_asked==True)):
                         if(board.board[i][j] == color_asked):
                              agent.motive += 0.35                             
                      #forward thinking decision                      
                      #forward think decision
                      if choice_orphan_check <= agent.orphan_check: 
                        #reward
                        agent.orphan_check+=0.01
                        #go through and check orphans
                        if agent.orphan_logged == True:
                            if side == "left":
                                l = robot2_orphans
                            else:
                                l = robot1_orphans
                            if (not l)==False:
                                if ((board.board[i][j] in l) == True):
                                    agent.motive += 0.35  
                      #decide to move or not                                                                                                  
                      #make the decision to move the block
                      if ((choice2+agent.motive)>= .50):
                          #smack if the agent tries to move a zero
                          if(board.board[i][j] == 0.0):
                              return "Tried to move zero value."                                                    
                          #attempt to move the block to an empty position in the 
                          if(board.board[0][1] == 0.0):
                              ii = 0
                              jj = 1
                          elif(board.board[1][1] == 0.0):
                              ii = 1
                              jj = 1
                          elif(board.board[2][1] == 0.0):
                              ii = 2
                              jj = 1
                          else:        
                              #smack if spots are full
                              return "Failed to move, Middle Spots Full."                                                         
                          #move color
                          color = board.board[i][j]
                          board.board[i][j] = 0.0
                          board.board[ii][jj] = color
                          ind = agent.colors_owned.index(color)                          
                          agent.colors_owned.pop(ind)
                          #switch the color from numeric to string
                          b = val_list[key_list.index(color)]
                          output_msg = "moved " + b + " " + str(i) + " " + str(j)
                          return output_msg                                
                elif (choice == 'take'):
                    #set the chance to run this again to slimtonone
                    #agent.take_motive+= -50
                    j = agent1_side
                    #go through the middle blocks
                    mj = 1
                    for mi in range(3):
                      agent.motive = 0.0
                      z_choice = random.random()
                      m_choice = random.random()
                      c_choice = random.random()
                      c_choice2 = random.random()
                      choice_orphan_check = random.random()
                      choice2 = random.random()
                      #zero value
                      #decide to check if the block is zero
                      if (z_choice <= agent.check_zero):
                          agent.check_zero+= 0.01
                          #smack if the agent tries to take a zero
                          if(board.board[mi][mj] == 0.0):
                            agent.check_zero+= 0.05
                            agent.motive+= -0.35                            
                      #check if agent needs the block
                      #choice to check own blocks
                      if (c_choice <= agent.check_my_needed):
                          #give a reinforcemnt
                          agent.check_my_needed += 0.01
                          #do i need the block?
                          if (board.board[mi][mj] in agent.colors_needed) == True:
                              #the current agent does need it                              
                              #give a reinforcemnt
                              agent.check_my_needed += 0.05
                              #set the motive much lower to not move the block
                              agent.motive += 0.35  
                      #check if they need 
                      if (c_choice2 <= agent.check_their_needed):
                          #give a reinforcemnt
                          agent.check_their_needed += 0.01
                          #do they need the block?
                          if (board.board[mi][mj] in agent2.colors_needed) == True:                              
                              #the other agent does need it
                              #give a reinforcemnt
                              agent.check_their_needed += 0.05
                              #set the motive much higher to move the block
                              agent.motive -= 0.35
                        
                      #forward thinking decision
                      #forward think decision
                      if choice_orphan_check <= agent.orphan_check: 
                        #reward
                        agent.orphan_check+=0.01
                        #go through and check orphans
                        if agent.orphan_logged == True:
                            if side == "left":
                                l = robot1_orphans
                            else:
                                l = robot2_orphans
                            if (not l)==False:
                                if ((board.board[mi][mj] in l) == True):
                                    agent.motive += 0.35

                      #decide to take or not          
                      #make the decision to move the block
                      if ((choice2+agent.motive)>= .50):
                          #smack if the agent tries to take a zero
                          if(board.board[mi][mj] == 0.0):
                            return "Tried to take zero value." 
                          #attempt to take the block to an empty position 
                          if(board.board[0][j] == 0.0):
                              ai = 0
                              aj = j
                          elif(board.board[1][j] == 0.0):
                              ai = 1
                              aj = j
                          elif(board.board[2][j] == 0.0):
                              ai = 2
                              aj = j
                          else:                              
                              #smack if spots are full
                              return "Failed to Take, Agent Spots Full."
                          #Take color
                          color = board.board[mi][mj]
                          board.board[mi][mj] = 0.0
                          board.board[ai][aj] = color                                                
                          agent.colors_owned.append(color)
                          #switch the color from numeric to string
                          b = val_list[key_list.index(color)]
                          output_msg = "moved " + b + " " + str(ai) + " " + str(aj)
                          return output_msg                                                                
                elif (choice == 'ask'):
                    #set the chance to run this again to slimtonone
                    #agent.try_to_ask_motive+= -50
                    j = agent1_side
                    j2 = agent2_side
                    #go through the current agents blocks
                    for i in range(3):
                      agent.motive = 0.0
                      z_choice = random.random()
                      m_choice = random.random()
                      c_choice = random.random()
                      c_choice2 = random.random()
                      choice_orphan_check = random.random()
                      choice2 = random.random()
                      #zero value
                      #decide to check if the block is zero
                      if (z_choice <= agent.check_zero):
                          agent.check_zero+= 0.01
                          #smack if the agent tries to take a zero
                          if(board.board[i][j2] == 0.0):
                            agent.check_zero+= 0.05
                            agent.motive+= -0.35                            
                      
                      #check if the middle is full
                      if (m_choice <= agent.check_middle):
                        agent.check_middle+=0.01
                        if (0.0 in middle) == False:
                            agent.check_middle+=0.05
                            agent.motive+= -0.35                            
                      
                      #check if agent needs the block
                      #choice to check own blocks
                      if (c_choice <= agent.check_my_needed):
                          #give a reinforcemnt
                          agent.check_my_needed += 0.01
                          #do i need the block?
                          if (board.board[i][j2] in agent.colors_needed) == True:
                              #the current agent does need it                              
                              #give a reinforcemnt
                              agent.check_my_needed += 0.05
                              #set the motive much lower to not move the block
                              agent.motive += 0.35 
                    
                      #check if they need 
                      if (c_choice2 <= agent.check_their_needed):
                          #give a reinforcemnt
                          agent.check_their_needed += 0.01
                          #do they need the block?
                          if (board.board[i][j2] in agent2.colors_needed) == True:                              
                              #the other agent does need it
                              #give a reinforcemnt
                              agent.check_their_needed += 0.05
                              #set the motive much higher to move the block
                              agent.motive += -0.35
                              
                      #forward thinking decision
                      #forward think decision
                      if choice_orphan_check <= agent.orphan_check: 
                        #reward
                        agent.orphan_check+=0.01
                        #go through and check orphans
                        if agent.orphan_logged == True:
                            if side == "left":
                                l = robot2_orphans
                                l2 = robot1_orphans
                            else:
                                l = robot1_orphans
                                l2 = robot2_orphans
                            if (not l)==False:
                                if((board.board[i][j2] in l) == True):
                                    agent.motive += -0.35
                            if (not l2)==False:  
                                if((board.board[i][j2] in l2) == True):
                                    agent.motive += 0.35                                            
                      #decide to move or not                                                                            
                      #make the decision to move the block
                      if ((choice2+agent.motive)>= .50):
                          #smack if the agent tries to move a zero
                          if(board.board[i][j2] == 0.0):
                              return "Asked to move zero value."                                                    
                          #attempt to move the block to an empty position in the 
                          if(board.board[0][1] == 0.0):
                              ii = 0
                              jj = 1
                          elif(board.board[1][1] == 0.0):
                              ii = 1
                              jj = 1
                          elif(board.board[2][1] == 0.0):
                              ii = 2
                              jj = 1
                          else:        
                              #smack if spots are full
                              return "Failed to ask, Middle Spots Full."                                                         
                          #Take color
                          color = board.board[i][j2]                          
                          #switch the color from numeric to string
                          b = val_list[key_list.index(color)]
                          output_msg = "move " + b + " " + str(ii) + " " + str(jj)
                          return output_msg                          
        #first we set the turn timeout
        num_turns = epochs
        turn_max = epochs
        game_log = []
        score = 'L'
        txt = "Game Start"
        if show_chat == True:
            print(txt)
            print("  ")
        game_log.append(txt)
        A = True
        
        middle = [board.board[0][1],board.board[1][1],board.board[2][1]]
        
        while num_turns > 0 :
    
            if A==True:
                if show_chat == True:
                    print(robot1.name)
                txt = rl_forward_think(robot1,robot2,game_log[-1],"left",show_chat,robot1_orphans,robot2_orphans,orphans_exist)
                A = False
            else:
                if show_chat == True:
                    print(robot2.name)
                txt = rl_forward_think(robot2,robot1,game_log[-1],"right",show_chat,robot1_orphans,robot2_orphans,orphans_exist)            
                A = True
            if show_chat == True:
                print(txt)                
                board.print_current()
                print(" ")
            game_log.append(txt)
            #do the stuff
            num_turns-=1
            middle = [board.board[0][1],board.board[1][1],board.board[2][1]]
            
            
            #sainity check for winning
            if(robot1.done == True and robot2.done == True):                              
                #first check if the middle is empty
                if(middle==[0.0,0.0,0.0]):
                    if(robot1.has_needed==True and robot2.has_needed==True):  
                        score = 'W'
                        if show_chat == True:
                            print(" ")
                            print("Goal state reached")
                            print("Turns taken, " + str(turn_max-num_turns))
                            board.print_current()
                            board.print_goal()                
                        temp1 = len(robot1.colors_owned)+len(robot2.colors_owned)
                        temp2 = turn_max-num_turns                
                        totalblocks.append(temp1)
                        totalturns.append(temp2)     
                        game_log.append(game_log)
                        score_log.append(score)
                        w_turns.append(temp2)
                        return    
                    
        if show_chat == True:
            print(" ")
            print("Game Time Out")
            print("Turns taken, " + str(turn_max-num_turns))
            board.print_current()
            board.print_goal()                
        temp1 = len(robot1.colors_owned)+len(robot2.colors_owned)
        temp2 = turn_max-num_turns      
        totalblocks.append(temp1)
        totalturns.append(temp2)     
        game_log.append(game_log)
        score_log.append(score)
        w_turns.append(temp2)
        return 
            
    
"""
# Reload the file
robot1 = pickle.load(open("robot1_2000_1m.pickle", "rb"))
# Reload the file
robot2 = pickle.load(open("robot2_2000_1m.pickle", "rb"))    
"""

#need this for multithreading
if __name__ == '__main__':    
   #used for multithreading
   freeze_support()   
   totalblocks = []
   totalturns = []
   score_log = []
   game_log = []
   w_turns = []
   show_chat = False
   epochs = 50
   amount  = 2000000
   start_time = time.time()
   for i in tqdm(range(amount)):       
       pro(robot1,robot2)
   print(" ")
   x = round(time.time() - start_time,3)
   y = round(x/60,3)
   print("--- %s seconds ---" % (x))
   print("--- %s minutes ---" % (y))
   
    # driver program
   x = 'L'
   y = 'W'
   d = Counter(score_log)
   print('{} has occurred {} times'.format(x, d[x]))
   print('{} has occurred {} times'.format(y, d[y]))
   print('{} Average turns taken.'.format(round(sum(totalturns)/len(totalturns))))
   print('{} Average Goal Completion turns taken.'.format(round(sum(w_turns)/len(w_turns))))
   print(robot1.colors_needed)
   print(robot2.colors_needed)
   
   
    
   #plt.hist(totalblocks, color = 'blue', edgecolor = 'black',bins = int(5))
   plt.hist(totalturns, color = 'green', edgecolor = 'black',bins = int(50))
   
   #test 1 is train 1000 then test on 50 or 100
   #test 2 is train 2000
   # Save the file
   pickle.dump(robot1, file = open("robot1_50_2m_new4.pickle", "wb"))
   #save the file
   pickle.dump(robot2, file = open("robot2_50_2m_new4.pickle", "wb"))
