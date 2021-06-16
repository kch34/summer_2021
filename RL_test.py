# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 12:28:22 2021

@author: Hostl
"""
from multiprocessing import Process, freeze_support
import sys, torch, copy, time, os, torchvision, gc
import torch.nn as nn
import random
import statistics
import matplotlib.pyplot as plt
import numpy as np

#initialize the board rows
b_rows = 3
#initialize the board columns
b_cols = 3



def __init__(self, p1, p2):
   self.board = np.zeros((b_rows, b_cols))
   self.p1 = p1
   self.p2 = p2
   self.isEnd = False
   self.boardHash = None
   # init p1 plays first
   self.playerSymbol = 1



def main():
    #need this for multithreading
    if __name__ == '__main__':
        freeze_support()