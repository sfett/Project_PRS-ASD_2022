#!/usr/bin/env python
# coding: utf-8

""" Script for plotting gradients with BrainSpace"""

# In[1]:

import numpy as np
import scipy.io as sio
import pickle
import pandas as pd

from brainspace.mesh import mesh_io as mio, array_operations as aop, mesh_operations as mop
from brainspace.plotting import plot_hemispheres
from brainspace.mesh.mesh_io import read_surface, write_surface
from brainspace.mesh.mesh_creation import build_polydata

#%% Load surfaces
gen_path = '/Users/serena/Documents/MICA/Project_ASD/data/general/'

s5 = read_surface(gen_path + '/conte69_5k_new.vtp')
s10 = read_surface(gen_path + '/conte_10k_fixed.vtp')

# Mad arrays from s10 to s5
for array_name in s10.PointData.keys():
    aop.resample_pointdata(s10, s5, array_name, red_func='mode', k=3, key=array_name, append=True)

#%% Load mask in 5k

mask_file = sio.loadmat(gen_path + '/conte69_10k.mat')
mask = mask_file['mask']

mask_bin = (mask==1) # creates boolean mask

new_mask = np.where(mask_bin==True) # creates the index of where mask==1

new_mask = new_mask[1] # not sure why it becomes 2D
print('Values in new_mask:', np.unique(new_mask))
print('Dimensions of new_mask:', new_mask.shape)

#%% Build left and right surface
cells = s5.GetCells2D()

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
    

#%% Plot mean HCP gradient

hcp_path = '/Users/serena/Documents/MICA/Project_ASD/data/hcp/cosine/'
file_hcp = open(hcp_path + 'HCP_N217_4ses_mean_gradient_cosine.pickle', "rb")
gm_hcp = pickle.load(file_hcp)

# Select first hcp gradient 
g1_hcp = gm_hcp.gradients_[:,0]
print('Dimensions of HCP G1 scores :', g1_hcp.shape)
g1_hcp_masked = np.zeros([1,10000]).T
g1_hcp_masked = g1_hcp_masked.flatten()
g1_hcp_masked[:] = np.NaN 
g1_hcp_masked[new_mask]= -g1_hcp

# Select second hcp gradient 
g2_hcp = gm_hcp.gradients_[:,1]
print('Dimensions of HCP G2 scores :', g2_hcp.shape)
# put back into 10k to plot 
g2_hcp_masked = np.zeros([1,10000]).T
g2_hcp_masked = g2_hcp_masked.flatten()
g2_hcp_masked[:] = np.NaN 
g2_hcp_masked[new_mask]= -g2_hcp

# Visualize hcp gradients 
hcp_grads = []
hcp_grads.append(g1_hcp_masked)
hcp_grads.append(g2_hcp_masked)

label_hcp =  ["HCP Gradient 1", "HCP Gradient 2"]

plot_hemispheres(s5_lh, s5_rh, array_name=hcp_grads, #color_range=(-.05,0.05),
                 nan_color=(0, 0, 0, 1),
                 cmap='viridis_r', 
                 color_bar=True, zoom=1.2,label_text=label_hcp,
                 layout_style='row', embed_nb=True, scale=2, cb__labelTextProperty={"fontSize": 33})

#%% Plot ABIDE ASD gradient

grads_ASD = []

abide_path = '/Users/serena/Documents/MICA/Project_ASD/data/abide'

file_ASD = open(abide_path + '/cosine/ABIDE_ASD_mean_gradient_cosine.pickle', "rb")
gm_ASD = pickle.load(file_ASD)

# Gradient 1
# taking negative such that DMN is pos, SMN is neg
g1_ASD = -gm_ASD.aligned_[:,0]
g1_ASD_masked = np.zeros([1,10000]).T
g1_ASD_masked = g1_ASD_masked.flatten()
g1_ASD_masked[:] = np.NaN 
g1_ASD_masked[new_mask]= -g1_ASD 

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

#%%
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



#%% Plot TD ABIDE gradient 

abide_path = '/Users/serena/Documents/MICA/Project_ASD/data/abide'

#file_TD = open(abide_path + '/cosine/ABIDE_TD_mean_gradient_cosine.pickle', "rb")
file_TD = open(abide_path + '/fisher_new/test/scripts/ABIDE_mean_gradient_9116-vertices_n211_na.pickle', "rb")
gm_TD = pickle.load(file_TD)


#%%
# Gradient 1
g1_TD = -gm_TD.gradients_[:,0]
g2_TD = -gm_TD.gradients_[:,1] 
g3_TD = -gm_TD.gradients_[:,2]

print(g1_TD.shape)

#%%

# Gradient 1 
g1_TD_masked = np.zeros([1,10000]).T
g1_TD_masked = g1_TD_masked.flatten()
g1_TD_masked[:] = np.NaN 
g1_TD_masked[new_mask]= -g1_TD

# Gradient 2
g2_TD_masked = np.zeros([1,10000]).T
g2_TD_masked = g2_TD_masked.flatten()
g2_TD_masked[:] = np.NaN 
g2_TD_masked[new_mask]= -g2_TD


# Gradient 3
g3_TD_masked = np.zeros([1,10000]).T
g3_TD_masked = g3_TD_masked.flatten()
g3_TD_masked[:] = np.NaN 
g3_TD_masked[new_mask]= -g3_TD

#%%
# visualize first 3 TD gradients
maps_TD = []
maps_TD.append(g1_TD_masked)
maps_TD.append(g2_TD_masked)
maps_TD.append(g3_TD_masked)

label_td =  ["Gradient 1", "Gradient 2", "Gradient 3"]

plot_hemispheres(s5_lh, s5_rh, array_name=maps_TD, #color_range=(-3,3), 
                 nan_color=(0, 0, 0, 1), label_text=label_td,
                 size=(800, 400), cmap='viridis_r', 
                 color_bar=True, zoom=1.2,
                 layout_style='row',embed_nb=True,scale=2,cb__labelTextProperty={"fontSize": 33})

#%% Plot ASD v. TD gradient 

maps_g1 = []
maps_g1.append(g1_ASD_masked)
maps_g1.append(g1_TD_masked)

label_g1 =  ["ASD", "TD"]


plot_hemispheres(s5_lh, s5_rh, array_name=maps_g1, color_range=(-3,3), 
                 nan_color=(0, 0, 0, 1), label_text=label_g1,
                 size=(800, 400), cmap='viridis_r', 
                 color_bar=True, zoom=1.2,
                 layout_style='row',embed_nb=True,scale=2,cb__labelTextProperty={"fontSize": 33})

#%%

ping_df = pd.read_csv("/Users/serena/Documents/MICA/Project_ASD/data/ping/PING_120_cohort.csv")


#%% Plot PING gradients 

ping_path = "/Users/serena/Documents/MICA/Project_ASD/data/ping/cosine"

file_ping = open(ping_path + '/PING_conte69-5k_n120_dm_cosine_0.9.pickle', "rb")
gm_ping = pickle.load(file_ping)

g1_ping = -gm_ping.aligned_[:,0]
print(g1_ping.shape)
g1_ping_masked = np.zeros([1,10000]).T
g1_ping_masked = g1_ping_masked.flatten()
g1_ping_masked[:] = np.NaN 
g1_ping_masked[new_mask]= -g1_ping

# Gradient 2
g2_ping = -gm_ping.aligned_[:,1] 
g2_ping_masked = np.zeros([1,10000]).T
g2_ping_masked = g2_ping_masked.flatten()
g2_ping_masked[:] = np.NaN 
g2_ping_masked[new_mask]= -g2_ping


# Gradient 3
g3_ping = -gm_ping.aligned_[:,2]
g3_ping_masked = np.zeros([1,10000]).T
g3_ping_masked = g3_ping_masked.flatten()
g3_ping_masked[:] = np.NaN 
g3_ping_masked[new_mask]= -g3_ping


#%%
# visualize first 3 ping gradients

maps_ping = []
maps_ping.append(g1_ping_masked)
maps_ping.append(g2_ping_masked)
maps_ping.append(g3_ping_masked)


label_ping =  ["Gradient 1", "Gradient 2", "Gradient 3"]

plot_hemispheres(s5_lh, s5_rh, array_name=maps_ping, color_range=(-.05,0.05), 
                 nan_color=(0, 0, 0, 1), label_text=label_ping,
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

