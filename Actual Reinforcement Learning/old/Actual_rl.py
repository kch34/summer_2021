# -*- coding: utf-8 -*-
"""
Created on Thu Jul 29 17:55:51 2021
@author: Kevin Charles Hostler
"""
#package imports
#needed for windows multiprocessing
from multiprocessing import freeze_support
#to be used to save and load saved models
import pickle
#used for the actual models
import torch as t
import torchvision as tv
#used for time keeping
import time
#used for plotting
import matplotlib.pyplot as plt
#used for arrays and tensors
import numpy as np
#used to copy the tensors
import copy
#used to track progress in loops
from tqdm import tqdm
#set the color dictionary
colors = {1.0:"black",2.0:"blue",3.0:"white",4.0:"red",5.0:"yellow",6.0:"pink"}

#set the color key list
key_list = list(colors.keys())
#set the color value list
val_list = list(colors.values())
#set the rows and columns for the size of the board
rows    = 3
columns = 3
#set the amount of turns for the agents to play out
game_turns = 50

robot1 = x
robot2 = y

#the board class
class State:
    #initialize the state 
    def __init__(self):
        self.board = np.zeros((rows, columns))
        self.goal_board = np.zeros((rows, columns))
        self.boardHash = None
    # board reset
    def reset(self):
        self.board = np.zerosnp.zeros((rows, columns))
        self.goal_board = np.zeros((rows, columns))
        self.boardHash = None
    # get unique hash of current board state
    def getHash(self):
        self.boardHash = str(self.board.reshape(columns * rows))
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



#the main function
def main():
    #initialize both agents
    robot1 = botty('taysir')
    robot2 = botty('zach')
    print('main')



#need this for multithreading
if __name__ == '__main__': 
    #needed for multithreading
    freeze_support()  
    main()
    