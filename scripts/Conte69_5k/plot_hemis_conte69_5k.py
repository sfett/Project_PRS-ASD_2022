#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 11:54:45 2022

@author: serena

Plot gradients script 

"""
#%% Plot hcp gradient in S400

from brainspace.utils.parcellation import map_to_labels
from brainspace.plotting import plot_hemispheres
from brainspace.datasets import load_group_fc, load_parcellation, load_conte69

# and load the conte69 surfaces
surf_lh, surf_rh = load_conte69()

mask = labeling != 0

grad = [None] * 3

for i in range(3):
    # map the gradient to the parcels
    grad[i] = map_to_labels(gm_hcp.gradients_[:, i], labeling, mask=mask, fill=np.nan)

plot_hemispheres(surf_lh, surf_rh, array_name=grad, size=(1200, 400), cmap='viridis_r',
                 color_bar=True, label_text=['Grad1', 'Grad2', 'Grad3'], scale=2, embed_nb=True, zoom=1.55)



#%% Plot Explained Variance

expl_var = gm_hcp.lambdas_/sum(gm_hcp.lambdas_)

plt.figure(figsize=(5,4))
plt.scatter(range(expl_var.size), expl_var*100, alpha=0.7, color='#00063F') 
plt.xlabel('Gradient', fontsize=14, fontname='Avenir')
plt.ylabel('Explained variance (%)', fontsize=14, fontname='Avenir')
plt.xticks(np.arange(len(expl_var)), np.arange(1, len(expl_var)+1)) # axis ticks start at 1 not 0
plt.show()
