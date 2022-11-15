#!/usr/bin/env python
# coding: utf-8



""" Compute gradient from group mean functional connectivity

This script computes a gradient from mean functional connectivity 
to be used as a template for Procrustes alignment in future 
analyses. 

Inputs: 
    Mean functional connectivty matric (npz file)


Outputs:
    The 10 first gradients in 10,000 x 10,000
    In conte 69 space (5k)
    Output is a pickle object
 
""" 

import os
import numpy as np
import pandas as pd
import pickle
import mat73 
import scipy.io as sio
import seaborn as sns
import matplotlib.pyplot as plt
import sys

from brainspace.mesh.mesh_io import read_surface
from brainspace.gradient import GradientMaps


# Load average connectivity matrix 

fc_file = sys.argv[1] 
surf_mat = sys.argv[2] 
kernel = sys.argv[3]
output_dir = sys.argv[4] 
output_name = sys.argv[5] 


# Load mean func connectivity

fc_file = np.load(fc_file)
mean_FC = fc_file['c_all']


# Load surface mask in 5k

mask_file = sio.loadmat(surf_mat)
mask = mask_file['mask']
mask_bin = (mask==1) # creates boolean mask
new_mask = np.where(mask_bin==True) # creates the index of where mask==1
new_mask = new_mask[1] 

# Mask the mean FC 

fc_masked = mean_FC[new_mask,:] 
fc_masked = fc_masked[:,new_mask]


# Compute gradient

gm = GradientMaps(n_components=10,approach ='dm', kernel=kernel, alignment=None, random_state=0)
gm.fit(fc_masked, sparsity=0.9)


# Save gradient as object 

object = gm
filehandler = open('output_dir' + 'output_name' + '.pickle', 'wb') 
pickle.dump(object, filehandler)

filehandler.close()



