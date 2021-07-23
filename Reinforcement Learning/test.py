# -*- coding: utf-8 -*-
"""
Created on Thu Jul 22 20:31:49 2021

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

lul = []
for i in tqdm(range(1000000)):
    r= random.random()
    if r < 0.50:
        lul.append(0)
    else:
        lul.append(1)

j = 1
w = 0
l = 0
t_w = []
t_l = []
for i in range(1000000):
    if lul[i] == 1:
        w+=1
    else:
        l+=1

    if j == 10000:
        t_w.append(w)
        t_l.append(l)
        w = 0
        l = 0
        j=1
    j+=1
    
    
    
import matplotlib.pyplot as plt
# line 1 points
x1 = range(len(t_w))
y1 = t_w
# plotting the line 1 points 
plt.plot(x1, y1, label = "line 1")
# line 2 points
x2 = range(len(t_l))
y2 = t_l
# plotting the line 2 points 
plt.plot(x2, y2, label = "line 2")
plt.xlabel('x - axis')
# Set the y axis label of the current axis.
plt.ylabel('y - axis')
# Set a title of the current axes.
plt.title('Two or more lines on same plot with suitable legends ')
# show a legend on the plot
plt.legend()
# Display a figure.
plt.show()
    
    
x = range(len(t_w))
    
# plot lines
plt.plot(x, t_l, label = "losses")
plt.plot(t_w, x, label = "wins")
plt.legend()
plt.show()
    
    
plt.plot(t_w,t_l)
plt.ylabel('some numbers')
plt.show()
    
plt.hist(t_w, color = 'green', edgecolor = 'black',bins = int(100))



#!/usr/bin/env python
import numpy

npts=20000000
filename='bigdata.bin'

def main():
    data = (numpy.random.uniform(0,1,(npts,3))).astype(numpy.float32)
    data[:,2] = 0.1*data[:,2]+numpy.exp(-((data[:,1]-0.5)**2.)/(0.25**2))
    fd = open(filename,'wb')
    
    
    scipy.io.numpyio.fwrite(fd,data.size,data)
    fd.close()

if __name__ == "__main__":
    main()