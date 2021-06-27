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
        #orphan list
        orphans = []
        #go through the left side first   
        #take out the ones that robot2 needs
        for i in range(3):
            if val_list[int(board.goal_board[i][0]-1)] in needed2_2:
                board.goal_board[i][0] = 0.0                
        #add in the ones that robot1 needs
        for i in range(3):
            if board.goal_board[i][0] == 0.0 and (not needed1)==False:
                board.goal_board[i][0] = key_list[val_list.index(needed1.pop())]
        #oprhan check
        if (not needed1) == False: 
            while (not needed1) == False:
                #check for needed orphans
                for i in range(3):
                    if val_list[int(board.goal_board[i][0]-1)] in needed1_1 == False:
                        orphans.append(board.goal_board[i][0])
                        board.goal_board[i][0] = 0.0
                        break                                
                #add in the ones that robot1 needs
                for i in range(3):
                    if board.goal_board[i][0] == 0.0:
                        board.goal_board[i][0] = key_list[val_list.index(needed1.pop())]
                        break                                
        #Go through the right side now
        #take out the ones that robot1 needs
        for i in range(3):
            if val_list[int(board.goal_board[i][2]-1)] in needed1_1:
                board.goal_board[i][2] = 0.0    
        #add in the ones that robot2 needs
        for i in range(3):
            if board.goal_board[i][2] == 0.0 and (not needed2)==False:
                board.goal_board[i][2] = key_list[val_list.index(needed2.pop())]      
        #check if oprhans is empty or not 
        if (not orphans)==False:
            #add in the orphans
            for i in range(3):
                if board.goal_board[i][2] == 0.0 and (not orphans)==False:
                    board.goal_board[i][2] = key_list[val_list.index(orphans.pop())]  
        #orphans is empty but check if robot2 has orphans that robot1 needs to take
        else:    
            #oprhan check
            if (not needed2) == False: 
                while (not needed2) == False:
                    #check for needed orphans
                    for i in range(3):
                        if val_list[int(board.goal_board[i][2]-1)] in needed2_2 == False:
                            orphans.append(board.goal_board[i][2])
                            board.goal_board[i][2] = 0.0
                            break                                
                    #add in the ones that robot2 needs
                    for i in range(3):
                        if board.goal_board[i][2] == 0.0:
                            board.goal_board[i][2] = key_list[val_list.index(needed2.pop())]
                            break
            #check if robot2 nee
            if (not orphans)==False:
                #add in the orphans
                for i in range(3):
                    if board.goal_board[i][0] == 0.0 and (not orphans)==False:
                        board.goal_board[i][0] = key_list[val_list.index(orphans.pop())]              
        #testing
        board.print_current()
        board.print_goal()
        robot1.colors_needed
        robot2.colors_needed
                
        #robot1.set_colors_owned(list(robot1.get_colors_owned().values()))
        #robot2.set_colors_owned(list(robot2.get_colors_owned().values()))        
        #robot1.set_colors_needed(list(robot1.get_colors_needed().values()))
        #robot2.set_colors_needed(list(robot2.get_colors_needed().values()))
        
        #setting up a general heuristic for learning
        def h_general(agent,agent2,input_msg,side):
            #get agent1's features
            agent_owned = agent.get_colors_owned()
            agent_needed = agent.get_colors_needed()
            #get agent2's features
            agent2_owned = agent2.get_colors_owned()
            agent2_needed = agent2.get_colors_needed()
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
                    #now that we have the desired block data, we find it and move it
                    #Does the agent have needed blocks?
                    try:
                        for ii in range(3):
                            for jj in range(3):
                                if c_grid[ii][jj] == color:
                                   c_grid[ii][jj] = 0
                                   c_grid[i][j] = color
                                   raise Found
                    except Found:
                        #do nothing
                        n=5                      
                    agent_owned.remove(color)
                    agent.set_colors_owned(agent_owned)
                    output_msg = "moved " + color + " " + str(i) + " " + str(j)
                    agent.set_done(False)
                    return output_msg                                    
            if(agent_needs_blocks == True):#the agent is in need of blocks 
                    print("I need blocks")
                    if(agent_can_take_blocks == True):#agent has room to take blocks
                        print("I have room to take blocks")
                        #check the middle for blocks
                        if middle == [0,0,0]:
                            #no blocks present so we ask for one
                            #find a block that the other agent has of ours and ask them to move it
                            for b in agent2_owned:
                                if (b in agent_needed):
                                    if(c_grid[0][1] == 0):
                                        i = 0
                                        j = 1
                                    elif(c_grid[1][1] == 0):
                                        i = 1
                                        j = 1
                                    else:
                                        i = 2
                                        j = 1
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
                                    if(c_grid[0][j] == 0):
                                        i = 0
                                    elif(c_grid[1][j] == 0):
                                        i = 1
                                    else:
                                        i = 2
                                    #moving
                                    try:
                                        for ii in range(3):
                                            for jj in range(3):
                                                if c_grid[ii][jj] == b:
                                                   c_grid[ii][jj] = 0
                                                   c_grid[i][j] = b
                                                   raise Found
                                    except Found:
                                        #do nothing
                                        n=5          
                                    agent_owned.append(b)
                                    agent.set_colors_owned(agent_owned)
                                    output_msg = "moved " + b + " " + str(i) + " " + str(j)
                                    agent.set_done(False)
                                    return output_msg
                            #if we make it this far then the middle blocks aren't mine
                            #find a block that the other agent has of ours and ask them to move it
                            for b in agent2_owned:
                                if (b in agent_needed):
                                    if(c_grid[0][1] == 0):
                                        i = 0
                                        j = 1
                                    elif(c_grid[1][1] == 0):
                                        i = 1
                                        j = 1
                                    else:
                                        i = 2
                                        j = 1
                                    output_msg = "move " + b + " " + str(i) + " " + str(j)
                                    agent.set_done(False)
                                    return output_msg                    
                    else:#agent does not have room to take blocks
                        print("I do not have room to take blocks")
                        #check if agent owns blocks the other agent needs
                        for b in agent_owned:
                                if (b in agent2_needed):
                                    if(c_grid[0][1] == 0):
                                        i = 0
                                        j = 1
                                    elif(c_grid[1][1] == 0):
                                        i = 1
                                        j = 1
                                    else:
                                        i = 2
                                        j = 1
                                    #moving
                                    try:
                                        for ii in range(3):
                                            for jj in range(3):
                                                if c_grid[ii][jj] == b:
                                                   c_grid[ii][jj] = 0
                                                   c_grid[i][j] = b
                                                   raise Found
                                    except Found:
                                        #do nothing
                                        n=5   
                                    agent_owned.remove(b)
                                    agent.set_colors_owned(agent_owned)
                                    output_msg = "moved " + b + " " + str(i) + " " + str(j)
                                    agent.set_done(False)
                                    return output_msg   
                        #Agent doesnt own needed blocks
                        #check for not needed blocks to move
                        for b in agent_owned:
                            if (b in agent_needed) == False:
                                    if(c_grid[0][1] == 0):
                                        i = 0
                                        j = 1
                                    elif(c_grid[1][1] == 0):
                                        i = 1
                                        j = 1
                                    else:
                                        i = 2
                                        j = 1
                                    #moving
                                    try:
                                        for ii in range(3):
                                            for jj in range(3):
                                                if c_grid[ii][jj] == b:
                                                   c_grid[ii][jj] = 0
                                                   c_grid[i][j] = b
                                                   raise Found
                                    except Found:
                                        #do nothing
                                        n=5   
                                    agent_owned.remove(b)
                                    agent.set_colors_owned(agent_owned)
                                    output_msg = "moved " + b + " " + str(i) + " " + str(j)
                                    agent.set_done(False)
                                    return output_msg                                                               
            else:#agent is not in need of blocks
                    print("I do not need blocks")
                    if(agent_can_take_blocks == True):#agent has room to take blocks
                        print("I have room to take blocks")
                        #see if there is an orphan block
                        if(c_grid[0][1] != 0):
                            orphan = c_grid[0][1]
                        elif(c_grid[1][1] != 0):
                            orphan = c_grid[1][1]
                        elif(c_grid[2][1] != 0):
                            orphan = c_grid[2][1]    
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
                        if(c_grid[0][j] == 0):
                            i = 0
                        elif(c_grid[1][j] == 0):
                            i = 1
                        else:
                            i = 2
                        #moving
                        try:
                            for ii in range(3):
                                for jj in range(3):
                                    if c_grid[ii][jj] == b:
                                        c_grid[ii][jj] = 0
                                        c_grid[i][j] = b
                                        raise Found
                        except Found:
                            #do nothing
                            n=5          
                        agent_owned.append(b)
                        agent.set_colors_owned(agent_owned)
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
        
        middle = [c_grid[0][1],c_grid[1][1],c_grid[2][1]]
        
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
            middle = [c_grid[0][1],c_grid[1][1],c_grid[2][1]]
            print_current()
            
            #sainity check for winning
            if(robot1.done == True and robot2.done == True):
                print(" ")
                print("Goal state reached")
                print("Turns taken, " + str(turn_max-num_turns))
                print_current()
                print_goal()
                temp1 = len(robot1.colors_owned)+len(robot2.colors_owned)
                temp2 = turn_max-num_turns
                
                return temp1, temp2
            
            print(" ")

    
totalblocks = []
totalturns = []
for i in range(1):
    tb, tt = pro()
    totalblocks.append(tb)
    totalturns.append(tt)
    
plt.hist(totalblocks, color = 'blue', edgecolor = 'black',bins = int(5))
plt.hist(totalturns, color = 'green', edgecolor = 'black',bins = int(50))