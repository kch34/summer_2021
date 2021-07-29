# -*- coding: utf-8 -*-
"""
@author: Hostl
"""
#imports
from multiprocessing import freeze_support  #needed due to windows processing
#import sys, torch, copy, time, os, torchvision, gc   
#import torch.nn as nn
import random
#import statistics
import matplotlib.pyplot as plt
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
#agent class
class botty:
    #initialize the robot with name blocks owned and needed
    def __init__(self, name, blocks, colors_needed):
        self.name = name
        self.blocks = blocks
        self.colors_owned = blocks
        self.colors_needed = colors_needed
        self.done = False
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
#the main code to be used for looping
def pro():
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
        #initialize both agents
        robot1 = botty('taysir',start_block1,color_needed1)
        robot2 = botty('zach',start_block2,color_needed2)
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

        #setting up a general heuristic for learning
        def h_general(agent,agent2,input_msg,side):
            #get agent1's features
            agent_owned = agent.colors_owned.copy()
            agent_needed = agent.colors_needed.copy()
            #get agent2's features
            agent2_owned = agent2.colors_owned.copy()
            agent2_needed = agent2.colors_needed.copy()
            #flags for heuristic logic
            agent_needs_blocks = False
            agent_can_take_blocks = False
            #Does the agent need a block?
            for b in agent_needed:
                if (b in agent_owned) == False:
                    agent_needs_blocks = True
            #can the agent take blocks?
            if len(agent_owned) < 3:
                agent_can_take_blocks = True    
            #we look to see if the other agent asked us to move a block        
            if(input_msg != "Game Start"):
                msg_list = input_msg.split()
                action = msg_list[0]
                if action == "move":
                    #this indicates the agent was asked to move something, else
                    #it would just be a statment moved.
                    color = msg_list[1]
                    i = int(msg_list[2])
                    j = int(msg_list[3])
                    #Set the color to numerical value
                    color = key_list[val_list.index(color)]                    
                    #now that we have the desired block data, we find it and move it
                    #Does the agent have needed blocks?
                    try:
                        for ii in range(3):
                            for jj in range(3):
                                if board.board[ii][jj] == color:
                                   board.board[ii][jj] = 0.0
                                   board.board[i][j] = color
                                   raise Found
                    except Found:
                        #do nothing
                        n=5                      
                    agent_owned.remove(color)
                    agent.set_colors_owned(agent_owned)                    
                    #set color back to a string
                    color = val_list[key_list.index(color)]
                    output_msg = "moved " + color + " " + str(i) + " " + str(j)
                    agent.set_done(False)
                    return output_msg                                    
            if(agent_needs_blocks == True):#the agent is in need of blocks 
                    print("I need blocks")
                    if(agent_can_take_blocks == True):#agent has room to take blocks
                        print("I have room to take blocks")
                        #check the middle for blocks
                        if middle == [0.0,0.0,0.0]:
                            #no blocks present so we ask for one
                            #find a block that the other agent has of ours and ask them to move it
                            for b in agent2_owned:
                                if (b in agent_needed):
                                    if(board.board[0][1] == 0.0):
                                        i = 0
                                        j = 1
                                    elif(board.board[1][1] == 0.0):
                                        i = 1
                                        j = 1
                                    else:
                                        i = 2
                                        j = 1
                                    #switch the color from numeric to string
                                    b = val_list[key_list.index(b)]
                                    output_msg = "move " + b + " " + str(i) + " " + str(j)
                                    agent.set_done(False)
                                    return output_msg
                        else:
                            #the middle has blocks, but are they mine?
                            for b in middle:
                                if b in agent_needed:
                                    if side == "left": #set for the left agent
                                        j = 0
                                    else:#set for the right agent
                                        j = 2
                                    #move the block
                                    if(board.board[0][j] == 0.0):
                                        i = 0
                                    elif(board.board[1][j] == 0.0):
                                        i = 1
                                    else:
                                        i = 2
                                    #moving
                                    try:
                                        for ii in range(3):
                                            for jj in range(3):
                                                if board.board[ii][jj] == b:
                                                   board.board[ii][jj] = 0.0
                                                   board.board[i][j] = b
                                                   raise Found
                                    except Found:
                                        #do nothing
                                        n=5          
                                    agent_owned.append(b)
                                    agent.set_colors_owned(agent_owned)
                                    #switch the color from numeric to string
                                    b = val_list[key_list.index(b)]
                                    output_msg = "moved " + b + " " + str(i) + " " + str(j)
                                    agent.set_done(False)
                                    return output_msg
                            #if we make it this far then the middle blocks aren't mine
                            #find a block that the other agent has of ours and ask them to move it
                            for b in agent2_owned:
                                if (b in agent_needed):
                                    if(board.board[0][1] == 0.0):
                                        i = 0
                                        j = 1
                                    elif(board.board[1][1] == 0.0):
                                        i = 1
                                        j = 1
                                    else:
                                        i = 2
                                        j = 1
                                    #switch the color from numeric to string
                                    b = val_list[key_list.index(b)]
                                    output_msg = "move " + b + " " + str(i) + " " + str(j)
                                    agent.set_done(False)
                                    return output_msg                    
                    else:#agent does not have room to take blocks
                        print("I do not have room to take blocks")
                        #check if agent owns blocks the other agent needs
                        for b in agent_owned:
                                if (b in agent2_needed):
                                    if(board.board[0][1] == 0.0):
                                        i = 0
                                        j = 1
                                    elif(board.board[1][1] == 0.0):
                                        i = 1
                                        j = 1
                                    else:
                                        i = 2
                                        j = 1
                                    #moving
                                    try:
                                        for ii in range(3):
                                            for jj in range(3):
                                                if board.board[ii][jj] == b:
                                                   board.board[ii][jj] = 0.0
                                                   board.board[i][j] = b
                                                   raise Found
                                    except Found:
                                        #do nothing
                                        n=5   
                                    agent_owned.remove(b)
                                    agent.set_colors_owned(agent_owned)
                                    #switch the color from numeric to string
                                    b = val_list[key_list.index(b)]
                                    output_msg = "moved " + b + " " + str(i) + " " + str(j)
                                    agent.set_done(False)
                                    return output_msg   
                        #Agent doesnt own needed blocks
                        #check for not needed blocks to move
                        for b in agent_owned:
                            if (b in agent_needed) == False:
                                    if(board.board[0][1] == 0.0):
                                        i = 0
                                        j = 1
                                    elif(board.board[1][1] == 0.0):
                                        i = 1
                                        j = 1
                                    else:
                                        i = 2
                                        j = 1
                                    #moving
                                    try:
                                        for ii in range(3):
                                            for jj in range(3):
                                                if board.board[ii][jj] == b:
                                                   board.board[ii][jj] = 0.0
                                                   board.board[i][j] = b
                                                   raise Found
                                    except Found:
                                        #do nothing
                                        n=5   
                                    agent_owned.remove(b)
                                    agent.set_colors_owned(agent_owned)
                                    #switch the color from numeric to string
                                    b = val_list[key_list.index(b)]
                                    output_msg = "moved " + b + " " + str(i) + " " + str(j)
                                    agent.set_done(False)
                                    return output_msg                                                               
            else:#agent is not in need of blocks
                    print("I do not need blocks")
                    if(agent_can_take_blocks == True):#agent has room to take blocks
                        print("I have room to take blocks")
                        #see if there is an orphan block
                        if(board.board[0][1] != 0.0):
                            orphan = board.board[0][1]
                        elif(board.board[1][1] != 0.0):
                            orphan = board.board[1][1]
                        elif(board.board[2][1] != 0.0):
                            orphan = board.board[2][1]    
                        else:
                            output_msg = "I'm out of moves."
                            agent.set_done(True)
                            return output_msg
                        #check if the orphan is in agent 2's needed
                        if (orphan in agent2_needed):
                            output_msg = "I'm out of moves."
                            agent.set_done(True)
                            return output_msg
                        b = orphan
                        #if it is not in the needed then take it as an orphan
                        if side == "left": #set for the left agent
                            j = 0
                        else:#set for the right agent
                            j = 2
                        #move the block
                        if(board.board[0][j] == 0.0):
                            i = 0
                        elif(board.board[1][j] == 0.0):
                            i = 1
                        else:
                            i = 2
                        #moving
                        try:
                            for ii in range(3):
                                for jj in range(3):
                                    if board.board[ii][jj] == b:
                                        board.board[ii][jj] = 0.0
                                        board.board[i][j] = b
                                        raise Found
                        except Found:
                            #do nothing
                            n=5          
                        agent_owned.append(b)
                        agent.set_colors_owned(agent_owned)
                        #switch the color from numeric to string
                        b = val_list[key_list.index(b)]
                        output_msg = "moved " + b + " " + str(i) + " " + str(j)
                        agent.set_done(False)
                        return output_msg                                                                                
                    else:#agent does not have room to take blocks
                        print("I do not have room to take blocks")
                        output_msg = "I'm out of moves."
                        agent.set_done(True)
                        return output_msg
        print("  ")
        
        #setting up the model
        
        #training the model
        #first we set the turn timeout
        num_turns = 50
        turn_max = 50
        game_log = []
        txt = "Game Start"
        print(txt)
        print("  ")
        game_log.append(txt)
        A = True
        
        middle = [board.board[0][1],board.board[1][1],board.board[2][1]]
        
        while num_turns > 0 :
    
            if A==True:
                print(robot1.name)
                txt = h_general(robot1,robot2,game_log[-1],"left")
                A = False
            else:
                print(robot2.name)
                txt = h_general(robot2,robot1,game_log[-1],"right")            
                A = True
            print(txt)
            game_log.append(txt)
            #do the stuff
            num_turns-=1
            middle = [board.board[0][1],board.board[1][1],board.board[2][1]]
            board.print_current()
            
            #sainity check for winning
            if(robot1.done == True and robot2.done == True):
                """
                print(" ")
                print("Goal state reached")
                print("Turns taken, " + str(turn_max-num_turns))
                board.print_current()
                board.print_goal()
                """
                temp1 = len(robot1.colors_owned)+len(robot2.colors_owned)
                temp2 = turn_max-num_turns                
                return temp1, temp2            
            print(" ")

    
totalblocks = []
totalturns = []
amount = 10000
for i in tqdm(range(amount)):
    tb, tt = pro()
    totalblocks.append(tb)
    totalturns.append(tt)
    
plt.hist(totalblocks, color = 'blue', edgecolor = 'black',bins = int(5))
plt.hist(totalturns, color = 'green', edgecolor = 'black',bins = int(50))