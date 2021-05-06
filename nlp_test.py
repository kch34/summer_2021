# -*- coding: utf-8 -*-
"""
@author: Hostl
"""
from multiprocessing import Process, freeze_support
import sys, torch, copy, time, os, torchvision, gc
import torch.nn as nn
import random
#current plan
"""
World:
1. I have a random set of between 1-3 blocks
2. You have a random set of between 1-3 blocks
3. I need a random set of 1-3 colors
4. You need a random set of 1-3 colors
"""
"""
Input:
1. Grid of the current world state
2. Goal configuration
3. Message (or null message) from other agent

Output: 
1. Color + "send" or "location"

Logic:
while True:
   if turn A:
      optimal action for A
  else
      optimal action for B

Simple initial model:
Inputs are linearized representations of the three inputs above which are then embedded.  These are passed to two fully-connected layers and then outs are.
1. fully connected layer over the space of colors (with a softmax)
2. fully connected layer over the space of locations and the send command.
This means the model makes two choices: What color and what to do with it.

Simple initial training paradigm:
By rolling out a bunch of the logic (above) we can produce input-output pairs of the form:  Given that I'm in the following situation (current state, message) I should predict the following color+loc/send.  This is trained via supervised training.

Simple evaluation setting:
Given two agents which have converged to near perfect performance on the training setup above, run them on random world configurations and see how many turns it takes for them to complete the task on average with a max-timeout of N turns (set N large but not too large, e.g. 50).

Once all of this is in place, we can now ask questions about smarter training and/or modeling decisions.
"""

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
    
    #setting up the model
    
    #training the model
    
        
    
    
    
    
    