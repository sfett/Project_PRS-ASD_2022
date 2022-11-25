#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 11:49:14 2022

@author: serena
"""

import numpy as np 
import pickle 


from brainspace.datasets import load_group_fc, load_parcellation, load_conte69
from brainspace.utils.parcellation import map_to_labels
from brainspace.plotting import plot_hemispheres

labeling = load_parcellation('schaefer', scale=400, join=True)
surf_lh, surf_rh = load_conte69() 


# Load ABCD gradient to see 

grads_path = '/Users/serena/Documents/MICA/Project_ASD/scripts/abcd/check_grads/'
file = open(grads_path + '/Schaefer_400/NDARINV03BDCNWM_hcp_aligned_gm_Schaefer-400_dm_na_0.9.pickle', "rb")
gm = pickle.load(file)

mask = labeling != 0

# map the gradient to the parcels
g1 = map_to_labels(gm.aligned_[:,0], labeling, mask=mask, fill=np.nan)

plot_hemispheres(surf_lh, surf_rh, array_name=g1, size=(900, 300), cmap='viridis', \
                 color_bar=True, label_text=['Grad1'], zoom=1.1, \
                 embed_nb=True,scale=2,cb__labelTextProperty={"fontSize": 33})

# Load HCP gradient to see 

file_hcp = open(grads_path + 'hcp_gm_Schaefer-400_dm_na_0.9.pickle', "rb")
gm_hcp = pickle.load(file_hcp)


# map the gradient to the parcels
g1_hcp = map_to_labels(gm_hcp.gradients_[:,0], labeling, mask=mask, fill=np.nan)

plot_hemispheres(surf_lh, surf_rh, array_name=g1_hcp, size=(900, 300), cmap='viridis', \
                 color_bar=True, label_text=['Grad1'], zoom=1.1, \
                 embed_nb=True,scale=2,cb__labelTextProperty={"fontSize": 33})






