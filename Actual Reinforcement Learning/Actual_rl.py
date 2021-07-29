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











#the main function
def main():
    print('main')



#need this for multithreading
if __name__ == '__main__': 
    #needed for multithreading
    freeze_support()  
    main()
    