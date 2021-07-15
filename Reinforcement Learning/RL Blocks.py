# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 12:28:22 2021
@author: Hostl
"""
#imports
from multiprocessing import freeze_support  #needed due to windows processing
#import sys, torch, copy, time, os, torchvision, gc   
#import torch.nn as nn
import random
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
        self.reward               = 0.0
        self.motive               = 0.0
        self.ask_motive           = 0.0
        self.give_motive          = 0.0
        self.take_motive          = 0.0
        self.try_to_ask_motive    = 0.0 
        self.done                 = False
        self.has_needed           = False
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
        self.motive               = 0.0
        self.ask_motive           = 0.0
        self.give_motive          = 0.0
        self.take_motive          = 0.0
        self.try_to_ask_motive    = 0.0            
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
    if __name__ == '__main__':
        #used for multithreading
        freeze_support()        
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

        #the reinforcement learning heuristic
        def rl_random(agent,agent2,input_msg,side):
            #get agent1's features
            agent_owned = agent.colors_owned.copy()
            agent_needed = agent.colors_needed.copy()
            #random actions
            #flags for  logic
            agent_needs_blocks         = False
            agent_can_take_blocks      = False            
            #reset the agents motives to zero
            agent.motive               = 0.0
            agent.ask_motive           = 0.0
            agent.give_motive          = 0.0
            agent.take_motive          = 0.0
            agent.try_to_ask_motive    = 0.0
            #reset the agents flags to default false
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
                print("I need blocks.")
            #can the agent take blocks?
            if len(agent_owned) < 3:
                agent_can_take_blocks = True 
                print("I have room to take blocks.")                 
            #set the done state if the agent has needed blocks.
            if agent_needs_blocks == False:
                agent.set_done(True)                                            
            #The agent makes the decision to check if it was asked to move a block                        
            #grab the last msg
            msg_list = input_msg.split()
            #find the action verb            
            action = msg_list[0]            
            #check if the action verb implies a 
            if action == "move":
                #if the action verb was a question to move
                #set the motive for checking for a question
                agent.ask_motive += 0.01           
                #set the color that was asked
                color_asked = msg_list[1]
                #Set the color to numerical value
                color_asked = key_list[val_list.index(color_asked)] 
            #choice to check for a question input msg                
            choice = random.random()
            #decides to check the input msg 
            if choice <= (agent.check_asked + agent.ask_motive):
                #we check if a question was asked
                if action == "move":
                    #if a question was asked then we want to increase the chance to happen again
                    agent.check_asked += 0.10
                    #set the flag that agent was asked to move a block
                    agent.was_asked = True
                    #set a high reward
                    agent.reward += 5
                else:
                    #always reinforce the fact that the agent checked for a question to encourage communication
                    agent.check_asked += 0.01
                    #set a moderate reward
                    agent.reward += 1                    
                #flag for moving a block asked by the other agent
                agent.checked_for_asked = True                
            else:
                 #we check if a question was asked
                if action == "move":
                    #set the flag that agent was asked to move a block
                    agent.was_asked = True
                    #set a high penalty
                    agent.reward -= 5
                else:
                    #set a moderate penalty
                    agent.reward -= 1
                #flag for moving a block asked by the other agent
                agent.checked_for_asked = False          
                                
            #set the move motive based on the above information
            if((agent.checked_for_asked==True)and(agent.was_asked==True)):
                #set the give motive
                agent.give_motive       = 0.05
            
            #set the ask motive and take motive
            if((agent_needs_blocks==True)and(agent_can_take_blocks==True)):
                agent.try_to_ask_motive = 0.05
                agent.take_motive       = 0.05        
            
            if(agent_needs_blocks==False):
                agent.set_done(True)
                agent.has_needed = True
            else:
                agent.set_done(False)
                agent.has_needed = False
            
            #the decision loop
            while True:            
                #reset parameters
                agent.checked_my_needed  = False
                agent.check_their_needed = False
                agent.motive = 0.0
                #set the choice parameters
                floor = 0.000
                first = (agent.try_to_give+agent.give_motive)
                second = (agent.try_to_take+agent.take_motive)
                third = (agent.try_to_ask+agent.try_to_ask_motive)
                roof = first + second + third
                #find the choice number                
                choice = random.uniform(floor,roof)                
                #go through the current agents column
                if side == "left":
                    j = 0
                    j2 = 2
                else:
                    j = 2
                    j2 =0
                #find out if the choice is to attempt to give a block
                if (choice <= first):                
                    #go through the current agents blocks
                    for i in range(3):
                      #check if i need it
                      #choice to check own blocks
                      choice = random.random()
                      if (choice <= agent.check_my_needed):
                          #set the bool
                          agent.checked_my_needed = True
                          #give a reinforcemnt
                          agent.check_my_needed += 0.01
                          #do i need the block?
                          if (board.board[i][j] in agent.colors_needed) == True:
                              #the current agent does need it                              
                              #give a reinforcemnt
                              agent.check_my_needed += 0.05
                              #set the motive much lower to not move the block
                              agent.motive += -0.20                              
                      #check if they need 
                      choice = random.random()
                      if (choice <= agent.check_their_needed):
                          #set the bool
                          agent.check_their_needed = True
                          #give a reinforcemnt
                          agent.check_their_needed += 0.01
                          #do they need the block?
                          if (board.board[i][j] in agent2.colors_needed) == True:                              
                              #the other agent does need it
                              #give a reinforcemnt
                              agent.check_their_needed += 0.05
                              #set the motive much higher to move the block
                              agent.motive += 0.20
                              
                      if((agent.checked_for_asked==True)and(agent.was_asked==True)):
                         if(board.board[i][j] == color_asked):
                              agent.motive += 0.20
                      
                      if(board.board[i][j] == 0.0):
                         agent.motive += -0.20
                      
                                                       
                      #orphan motive, neither need but space is needed
                      
                              
                      #decide to move or not          
                      choice = random.random()
                      #make the decision to move the block
                      if ((choice+agent.motive)>= .50):
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
                          
                        
                #find out if the choice is to attempt to take a block
                elif((choice>first)and(choice<=second)):
                    #go through the middle blocks
                    jj = 1
                    for ii in range(3):                        
                      #non-zero value
                      #check if i need it
                      #choice to check own blocks
                      choice = random.random()
                      if (choice <= agent.check_my_needed):
                          #set the bool
                          agent.checked_my_needed = True
                          #give a reinforcemnt
                          agent.check_my_needed += 0.01
                          #do i need the block?
                          if (board.board[ii][jj] in agent.colors_needed) == True:
                              #the current agent does need it                              
                              #give a reinforcemnt
                              agent.check_my_needed += 0.05
                              #set the motive much lower to not move the block
                              agent.motive += 0.20     
                      #check if they need 
                      choice = random.random()
                      if (choice <= agent.check_their_needed):
                          #set the bool
                          agent.check_their_needed = True
                          #give a reinforcemnt
                          agent.check_their_needed += 0.01
                          #do they need the block?
                          if (board.board[ii][jj] in agent2.colors_needed) == True:                              
                              #the other agent does need it
                              #give a reinforcemnt
                              agent.check_their_needed += 0.05
                              #set the motive much higher to move the block
                              agent.motive += -0.20
                      
                      #decide to take or not          
                      choice = random.random()
                      #make the decision to move the block
                      if ((choice+agent.motive)>= .50):
                          #smack if the agent tries to take a zero
                          if(board.board[ii][jj] == 0.0):
                              return "Tried to take zero value."      
                          #attempt to take the block to an empty position 
                          if(board.board[0][j] == 0.0):
                              iii = 0
                              jjj = j
                          elif(board.board[1][j] == 0.0):
                              iii = 1
                              jjj = j
                          elif(board.board[2][j] == 0.0):
                              iii = 2
                              jjj = j
                          else:                              
                              #smack if spots are full
                              return "Failed to Take, Agent Spots Full."
                          #Take color
                          color = board.board[ii][jj]
                          board.board[ii][jj] = 0.0
                          board.board[iii][jjj] = color                                                
                          agent.colors_owned.append(color)
                          #switch the color from numeric to string
                          b = val_list[key_list.index(color)]
                          output_msg = "moved " + b + " " + str(iii) + " " + str(jjj)
                          return output_msg                    
                #attempt to ask for a block
                elif((choice>second+first)and(choice<=roof)):
                    #go through the current agents blocks
                    for i in range(3):
                    #check if i need it
                      #choice to check own blocks
                      choice = random.random()
                      if (choice <= agent.check_my_needed):
                          #set the bool
                          agent.checked_my_needed = True
                          #give a reinforcemnt
                          agent.check_my_needed += 0.01
                          #do i need the block?
                          if (board.board[i][j] in agent.colors_needed) == True:
                              #the current agent does need it                              
                              #give a reinforcemnt
                              agent.check_my_needed += 0.05
                              #set the motive much lower to not move the block
                              agent.motive += 0.20                              
                      #check if they need 
                      choice = random.random()
                      if (choice <= agent.check_their_needed):
                          #set the bool
                          agent.check_their_needed = True
                          #give a reinforcemnt
                          agent.check_their_needed += 0.01
                          #do they need the block?
                          if (board.board[i][j] in agent2.colors_needed) == True:                              
                              #the other agent does need it
                              #give a reinforcemnt
                              agent.check_their_needed += 0.05
                              #set the motive much higher to move the block
                              agent.motive += -0.20
                      #decide to take or not          
                      choice = random.random()
                      #make the decision to move the block
                      if ((choice+agent.motive)>= .50):
                          #smack if the agent tries to take a zero
                          if(board.board[i][j2] == 0.0):
                              return "Asked to move zero value."
                          #attempt to take the block to an empty position 
                          y=1
                          if(board.board[0][1] == 0.0):
                              x=0
                          elif(board.board[1][1] == 0.0):
                              x=1
                          elif(board.board[2][1] == 0.0):
                              x=2
                          else:                              
                              #smack if spots are full
                              return "Middle Spots full"
                          #Take color
                          color = board.board[i][j2]
                          #switch the color from numeric to string
                          b = val_list[key_list.index(color)]
                          output_msg = "move " + b + " " + str(x) + " " + str(y)
                          return output_msg                                        

        #first we set the turn timeout
        num_turns = 50
        turn_max = 50
        game_log = []
        score = 'L'
        txt = "Game Start"
        print(txt)
        print("  ")
        game_log.append(txt)
        A = True
        
        middle = [board.board[0][1],board.board[1][1],board.board[2][1]]
        
        while num_turns > 0 :
    
            if A==True:
                print(robot1.name)
                txt = rl_random(robot1,robot2,game_log[-1],"left")
                A = False
            else:
                print(robot2.name)
                txt = rl_random(robot2,robot1,game_log[-1],"right")            
                A = True
            print(txt)
            game_log.append(txt)
            #do the stuff
            num_turns-=1
            middle = [board.board[0][1],board.board[1][1],board.board[2][1]]
            board.print_current()
            
            #sainity check for winning
            if(robot1.done == True and robot2.done == True):                              
                #first check if the middle is empty
                if(middle==[0.0,0.0,0.0]):
                    if(robot1.has_needed==True and robot2.has_needed==True):  
                        score = 'W'
                        print(" ")
                        print("Goal state reached")
                        print("Turns taken, " + str(turn_max-num_turns))
                        board.print_current()
                        board.print_goal()                
                        temp1 = len(robot1.colors_owned)+len(robot2.colors_owned)
                        temp2 = turn_max-num_turns                
                        return temp1, temp2, game_log, score
            print(" ")
        
        print(" ")
        print("Game Time Out")
        print("Turns taken, " + str(turn_max-num_turns))
        board.print_current()
        board.print_goal()                
        temp1 = len(robot1.colors_owned)+len(robot2.colors_owned)
        temp2 = turn_max-num_turns                
        return temp1, temp2, game_log, score
            

totalblocks = []
totalturns = []
score_log = []
amount = 1
for i in tqdm(range(amount)):
    tb, tt, g_log, score = pro(robot1,robot2)
    totalblocks.append(tb)
    totalturns.append(tt)
    score_log.append(score)

# driver program
x = 'L'
y = 'W'
d = Counter(score_log)
print('{} has occurred {} times'.format(x, d[x]))
print('{} has occurred {} times'.format(y, d[y]))
    
plt.hist(totalblocks, color = 'blue', edgecolor = 'black',bins = int(5))
plt.hist(totalturns, color = 'green', edgecolor = 'black',bins = int(50))