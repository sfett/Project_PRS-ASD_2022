#!/usr/bin/env python
# coding: utf-8

""" 

This script plots gradients onto hemispheres for visualization purposes. 
Also calculates the percentage of variance explained within the connectome by each gradient. 

Inputs: 
* Conte69-5k surface data is not built into BrainSpace
* Requires surface data to be uploaded independently
    * surface space (.vtp)  
    * mask (.mat) 

Outputs: 
* Python file of visualized hemispheres. 

Dependencies: 
This script requires that `BrainSpace`--and all its necessary packages--be
installed within the Python environment. 
(See: https://brainspace.readthedocs.io/en/latest/)

""" 

import numpy as np
import scipy.io as sio
import pickle
import pandas as pd

from brainspace.mesh import mesh_io as mio, array_operations as aop, mesh_operations as mop
from brainspace.plotting import plot_hemispheres
from brainspace.mesh.mesh_io import read_surface, write_surface
from brainspace.mesh.mesh_creation import build_polydata

# Load surfaces
gen_path = '/Users/serena/Documents/MICA/Project_ASD/data/general/'
s5 = read_surface(gen_path + '/conte69_5k_new.vtp')
s10 = read_surface(gen_path + '/conte_10k_fixed.vtp')


# Resample arrays from 10k to 5k 
for array_name in s10.PointData.keys():
    aop.resample_pointdata(s10, s5, array_name, red_func='mode', k=3, key=array_name, append=True)

    
# Load mask in 5k resolution
# Indicates which vertices should be mapped

mask_file = sio.loadmat(gen_path + '/conte69_10k.mat')
mask = mask_file['mask']
mask_bin = (mask==1) # creates boolean mask
new_mask = np.where(mask_bin==True) # creates the index of where mask==1
new_mask = new_mask[1] # not sure why it becomes 2D
print('Values in new_mask:', np.unique(new_mask))
print('Dimensions of new_mask:', new_mask.shape)


# Must first build left and right surface
cells = s5.GetCells2D()

# 5k per hemisphere 
s5_lh_points = s5.Points[:5000]
s5_lh_cells = cells[(cells<5000).any(1)]

s5_rh_points = s5.Points[5000:]
s5_rh_cells = cells[(cells>=5000).any(1)]

s5_lh = build_polydata(s5_lh_points, cells=s5_lh_cells)
s5_rh = build_polydata(s5_rh_points-5000, cells=s5_rh_cells-5000)

# Copy data to surfaces
for array_name in s5.PointData.keys():
    x = s5.get_array(array_name)
    s5_lh.append_array(x[:5000], name=array_name, at='p')
    s5_rh.append_array(x[5000:], name=array_name, at='p')
    

# Plot ABIDE ASD gradient

grads_ASD = []

abide_path = '/Users/serena/Documents/MICA/Project_ASD/data/abide'

file_ASD = open(abide_path + '/cosine/ABIDE_ASD_mean_gradient_cosine.pickle', "rb")
gm_ASD = pickle.load(file_ASD)

# Gradient 1
g1_ASD = -gm_ASD.aligned_[:,0]
g1_ASD_masked = np.zeros([1,10000]).T
g1_ASD_masked = g1_ASD_masked.flatten()
g1_ASD_masked[:] = np.NaN 
g1_ASD_masked[new_mask]= -g1_ASD # taking negative such that DMN is pos, SMN is neg

# Gradient 2
g2_ASD = -gm_ASD.aligned_[:,1]
g2_ASD_masked = np.zeros([1,10000]).T
g2_ASD_masked = g2_ASD_masked.flatten()
g2_ASD_masked[:] = np.NaN 
g2_ASD_masked[new_mask]= -g2_ASD 

# Gradient 3
g3_ASD = -gm_ASD.aligned_[:,2]
g3_ASD_masked = np.zeros([1,10000]).T
g3_ASD_masked = g3_ASD_masked.flatten()
g3_ASD_masked[:] = np.NaN 
g3_ASD_masked[new_mask]= -g3_ASD 

# visualize first 3 TD gradients
maps_ASD = []
maps_ASD.append(g1_ASD_masked)
maps_ASD.append(g2_ASD_masked)
maps_ASD.append(g3_ASD_masked)

label_asd =  ["Gradient 1", "Gradient 2", "Gradient 3"]

plot_hemispheres(s5_lh, s5_rh, array_name=maps_ASD, color_range=(-3,3), 
                 nan_color=(0, 0, 0, 1), label_text=label_asd,
                 size=(800, 400), cmap='viridis_r', 
                 color_bar=True, zoom=1.2,
                 layout_style='row',embed_nb=True,scale=2,cb__labelTextProperty={"fontSize": 33})


#%% Plot Explained Variance

import matplotlib.pyplot as plt

expl_var = gm_TD.lambdas_/sum(gm_TD.lambdas_)

plt.figure(figsize=(5,4))
plt.scatter(range(expl_var.size), expl_var*100, alpha=0.7, color='#00063F') 
plt.xlabel('Gradient', fontsize=14, fontname='Avenir')
plt.ylabel('Explained variance (%)', fontsize=14, fontname='Avenir')
plt.xticks(np.arange(len(expl_var)), np.arange(1, len(expl_var)+1)) # axis ticks start at 1 not 0
plt.show()

