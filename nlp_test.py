# -*- coding: utf-8 -*-
"""
@author: Hostl
"""
from multiprocessing import Process, freeze_support
import sys, torch, copy, time, os, torchvision, gc
import torch.nn as nn
import random
import statistics
import matplotlib.pyplot as plt

def pro():

    #need this for multithreading
    if __name__ == '__main__':
        freeze_support()
        
        
        def print_current():
            print("Current state")
            print(c_grid[0])
            print(c_grid[1])
            print(c_grid[2])
            
        def print_goal():
            print("Goal State")
            print(g_grid[0])
            print(g_grid[1])
            print(g_grid[2])
            
        class botty:
            def __init__(self, name, blocks, colors_needed):
                self.name = name
                self.blocks = blocks
                self.colors_owned = blocks
                self.colors_needed = colors_needed
                self.done = False
            def get_colors_owned(self):
                return self.colors_owned
            def get_colors_needed(self):
                return self.colors_needed
            def set_colors_owned(self,x):
                self.colors_owned = x
            def set_colors_needed(self,x):
                self.colors_needed = x
            def set_done(self,x):
                self.done = x
                
        class Found(Exception): pass
        
        
        #data encodings
        color_ix = {"Black":0,"Blue":1,"White":2,
                    "Red":3,"Yellow":4,"Pink":5}
        location_ix = {"one":6,   "two":7,   "three":8,
                       "four":9,  "five":10, "six":11,
                       "seven":12,"eight":13,"nine":14}
        
        
        
        
        #for i in range(100):
        
        d1_grid = [[0,0,0],
                   [0,0,0],
                   [0,0,0]]
        c_grid  = [[0,0,0],
                   [0,0,0],
                   [0,0,0]]
        g_grid  = [[0,0,0],
                   [0,0,0],
                   [0,0,0]]
        d1_colors = ['Black','Blue','White','Red','Yellow','Pink']
            
        start_color1 = random.randint(1, 3)
        start_block1 = {}
        for i in range(start_color1):
            random.shuffle(d1_colors)
            start_block1[i] = d1_colors.pop()
        
        start_color2 = random.randint(1, 3)
        start_block2 = {}
        for i in range(start_color2):
            random.shuffle(d1_colors)
            start_block2[i] = d1_colors.pop()
        
        d1_colors = [1,2,3,4,5,6]
        
        color1 = random.randint(1, len(start_block2))
        color_needed1 = {}
        color2 = random.randint(1, len(start_block1))
        color_needed2 = {}
    
        temp = list(start_block2.values())
        random.shuffle(temp)
        for i in range(color1):
            color_needed1[i] = temp.pop()
        temp = list(start_block1.values())
        random.shuffle(temp)
        for i in range(color2):
            color_needed2[i] = temp.pop()
        
        robot1 = botty('taysir',start_block1,color_needed1)
        robot2 = botty('zach',start_block2,color_needed2)
       
        for i in range(len(robot1.blocks)):
            c_grid[i][0] = robot1.blocks[i]
        for i in range(len(robot2.blocks)):
            c_grid[i][2] = robot2.blocks[i]
    
        
        needed1 = list(robot1.colors_needed.values())
        needed2 = list(robot2.colors_needed.values())
        
        for i in range(3):
            for j in range(3):
                g_grid[i][j] = c_grid[i][j]
        
        #go through the left side first   
        #take out the ones that robot2 needs
        for i in range(3):
            if g_grid[i][0] in needed2:
                g_grid[i][0] = 0;
        #add in what robot1 needs to it's side
        for i in range(3):
            if g_grid[i][0]==0 and (not needed1) == False:
                g_grid[i][0] = needed1.pop()
        #this is if robot1 needs to move a block thats extra
        temp = list(robot1.colors_needed.values())
        orphan = []
        if (not needed1) == False:
            for i in range(3):
                if (g_grid[i][0] in temp) == False and (g_grid[i][0] in needed2) == False:
                    orphan.append(g_grid[i][0])
                    g_grid[i][0] = needed1.pop()
                if (not needed1) == True:
                    break    
        needed1 = list(robot1.colors_needed.values())
        #go through the right side now   
        #take out the ones that robot1 needs
        for i in range(3):
            if g_grid[i][2] in needed1:
                g_grid[i][2] = 0;
        #add in what robot2 needs to it's side
        for i in range(3):
            if g_grid[i][2]==0 and (not needed2) == False:
                g_grid[i][2] = needed2.pop()
        #this is if robot1 needs to move a block thats extra
        temp = list(robot2.colors_needed.values())
        if (not needed2) == False:
            for i in range(3):
                if (g_grid[i][2] in temp) == False and (g_grid[i][2] in needed1) == False:
                    orphan.append(g_grid[i][2])
                    g_grid[i][2] = needed2.pop()
                if (not needed2) == True:
                    break
    
        if (not orphan == False):
            for i in range(3):
                if g_grid[i][0] == 0:
                    g_grid[i][0] = orphan.pop()
                if (not orphan) ==True:
                    break
        if (not orphan == False):
            for i in range(3):
                if g_grid[i][2] == 0:
                    g_grid[i][2] = orphan.pop()
                if (not orphan) ==True:
                    break    
        
        print_current()
        print_goal()
        
        robot1.set_colors_owned(list(robot1.get_colors_owned().values()))
        robot2.set_colors_owned(list(robot2.get_colors_owned().values()))
        
        robot1.set_colors_needed(list(robot1.get_colors_needed().values()))
        robot2.set_colors_needed(list(robot2.get_colors_needed().values()))
        
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
            
        
            #Does the agent have orphaned blocks?
            
            
            
        
        
        
        
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