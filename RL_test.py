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






def main():
    #need this for multithreading
    if __name__ == '__main__':
        freeze_support()