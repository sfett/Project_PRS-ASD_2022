#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

Oct 28, 2022. @author: serenafett 


This script computes individual gradients from functional connectivity
in Schaefer 400 parcellations. Option is provided for gradients to be aligned
to a reference gradient. 

Inputs: 
    
    * List of subjects ID (.txt)
    * Individual functional connectivity matrices (.npz)
    
Outputs:
    
    * The 10 first gradients in 400 x 400 parcellation space (.pickle)
    
    
This script requires that `BrainSpace`--and all its necessary packages--be
installed within the Python environment. 
(See: https://brainspace.readthedocs.io/en/latest/)


This scripted is to be called from a bash script (.sh) where all dataset
specific paths and inputs are to be already defined. 


"""

import os
import numpy as np
import pandas as pd
import pickle
import scipy.io as sio
import sys
import time


from brainspace.mesh.mesh_io import read_surface
from brainspace.gradient import GradientMaps
import matplotlib.pyplot as plt


from brainspace.datasets import load_group_fc, load_parcellation 

# Call input variables from bash script

sID_file = sys.argv[1]

# fc (inputs)
fc_pth = sys.argv[2]
fc_fname = sys.argv[3]
fc_label = sys.argv[4]

# gradients (outputs)
grad_path = sys.argv[5]
grad_fname = sys.argv[6]

# template (optional input)
template = sys.argv[7]
template_grad_pth = sys.argv[8]


def fisher_z1(FC):
    
    ''' Replaces diagonal with value of 0s '''
    
    print("using Fisher z method that replaces with 0s")
    FCz = np.arctanh(FC)
    FCz[~np.isfinite(FCz)] = 0 
    
    return FCz


def fisher_z2(FC):

    ''' Replaces diagonal with relative highest value of correlation '''
    
    print("using Fisher z method of highest value of corr")
    FCz = np.arctanh(FC)
    FCz = np.clip(FCz, np.arctanh(-1+np.spacing(1)), np.arctanh(1-np.spacing(1)))
    
    return FCz


def compute_gradient(FCz,gm_template):
    
    # Perform Procrustes alignment
    if gm_template == None:
        
        # note can use kernel and approach with different inputs 
        gm = GradientMaps(n_components=10, sparsity=0.9, kernel='normalized_angle', \
                          approach='dm', random_state=0)
        gm = gm.fit(FCz)
        
    else: 
        
        gm = GradientMaps(n_components=10, sparsity=0.9, approach ='dm', \
                          kernel='normalized_angle', random_state=0, \
                          alignment='procrustes')
            
        gm = gm.fit(FCz, sparsity=0.9, reference=gm_template.gradients_)
        
    return gm


def create_template_grad(template):

    global alignment
    
    if template == 'hcp': # use BrainSpace preloaded data
        
        alignment = '_hcp_aligned'
        print("You are aligning gradients to HCP template")
        
        # load FC 
        FC_hcp = load_group_fc('schaefer', scale=400)

        # fisher Z transform 
        FCz_hcp = fisher_z1(FC_hcp)

        # compute gradient
        gm_temp = compute_gradient(FCz_hcp, None)
    
        print("Dimensions of HCP template: " + gm_temp.gradients_[:,1].shape)
    
    else:
        # using other dataset template data
        # for now set to None
        
        alignment = '_no_alignment'
        print("Gradients will not be aligned to template")
     
        gm_temp == None 
        
    return gm_temp


# Compute template gradient and save
gm_template = create_template_grad(template)
file_template = open(template_grad_pth + template + grad_fname, 'wb') 
pickle.dump(gm_template, file_template)
file_template.close()
print("Template gradient successfully produced and saved")


# Load list of subjects 
df = pd.read_csv(sID_file, sep=" ", header=None, names=['sid'])

# test first three subjects 
# remove after
n_test = 2
print("running for first " + n_test + "subjects")
df = df.head(n_test)


# Compute individual gradients
for index,rw in df.iterrows():

    sid = str(rw.sid)
    
    # to calculate time taken 
    st = time.time()

    sub_path = fc_pth + sid + fc_fname 
    
    # loading mat file 
    data = sio.loadmat(sub_path)
    fc = data[fc_label]
    
    # remove subcortical parcels
    fc = fc[:400, :400]
    
    print("Dimension of FC: " + fc.shape)
    
    # Fisher z transform using one of two methods
    fc_z = fisher_z1(fc)
    
    # compute gradient 
    grad = compute_gradient(fc_z,gm_template)
    
    print("Gradient successfully computed for sID: " + sid)
    print("Dimension of subject grad: " + grad.aligned_[:,1].shape)
                                                        
    # save gradient for each subject 
    file = open(grad_path + sid + alignment + grad_fname, 'wb') 
    pickle.dump(grad, file)
    file.close()

    et = time.time()
    
    elapsed_time = et - st
    print('Execution time to produce grad:', elapsed_time, 'seconds')

