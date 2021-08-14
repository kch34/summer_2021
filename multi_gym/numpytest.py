# -*- coding: utf-8 -*-
"""
Created on Fri Aug 13 16:24:16 2021

@author: Hostl
"""
import numpy as np




def cartesian(*arrays):
    mesh = np.meshgrid(*arrays)  # standard numpy meshgrid
    dim = len(mesh)  # number of dimensions
    elements = mesh[0].size  # number of elements, any index will do
    flat = np.concatenate(mesh).ravel()  # flatten the whole meshgrid
    reshape = np.reshape(flat, (dim, elements)).T  # reshape and transpose
    return reshape



x = np.arange(4)
a = cartesian(x,x,x, x,x,x, x,x,x)
print(a)

grid = []
for i in a:
    if (np.count_nonzero(i) <= 6) and (np.count_nonzero(i) >= 2):
        if(1 in i) and (2 in i):    
         i = i.astype('float32')
         grid.append(i)
