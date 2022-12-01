#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dec 1, 2022. @author: sfett


This script computes the average gradient of a dataset by calculating the mean 
across individual funcitonal connectivity. In Schaefer 400 parcellations.
Option is provided to align gradient to reference gradient. 

Inputs: 
    
    * List of subjects ID (.csv)
    * Individual functional connectivity matrices (.mat)
    
Outputs:
    
    * The 10 first average gradients in 400 x 400 parcellation space (.pickle)
    
    
This script requires that `BrainSpace`--and all its necessary packages--be
installed within the Python environment. 
(See: https://brainspace.readthedocs.io/en/latest/)

"""

import numpy as np
import pandas as pd
import pickle
import scipy.io as sio


from brainspace.gradient import GradientMaps

# Define inputs 
root_path = '/data/mica2/ABCD/imaging/'
fc_path = root_path + 'RSFC/'
fc_label = 'corr_mat'
fc_fname = '_rest_mc_skip_residc_interp_FDRMS0.3_DVARS50_bp_0.009_0.08_fs6_sm6_all2all.mat'
template_grad = '/data/mica1/03_projects/serena/HCP/Schaefer_400/hcp_gm_Schaefer-400_dm_na_0.9.pickle'
grad_path = root_path + '/RSFC_gradients/Schaefer_400/'
grad_fname="_gm_Schaefer-400_dm_na_0.9"
average = 'ABCD_average_gradient_n2518_hcp_aligned'

# Open dataset dataframe
df = pd.read_csv(root_path + 'abcd_final_cohort_PRS_demog.csv')

# Calculate mean FC
c_all = None 
n_all = 0

for index,rw in df.iterrows():
    
    sid = str(rw.subjectkey)
    print(sid)
    
    # loading subject fc file
    sub_path = fc_path + sid + fc_fname 
    data = sio.loadmat(sub_path)
    c = data[fc_label]
   
    # remove subcortical parcels
    c = c[:400, :400]
   
    print("Dimension of FC is " + str(c.shape) +"parcels")
   
    # Fisher z transform, also replaces diagonal with value of 0s 
    c_z = np.arctanh(c)
    c_z[~np.isfinite(c_z)] = 0

    c_all = c_all + c_z if c_all is not None else c_z
    n_all += 1
   
# ddivide by total number of subjects to get mean connectivity matrix of all subjects
c_all /= n_all

print(c_all.shape)
print(n_all)

# save matrix within fc directory
np.savez_compressed(fc_path, FC_all=c_all)   

# if aligning, load template gradient
file_to_read = open(template_grad, "rb")
gm_template = pickle.load(file_to_read)

# create gradient from mean connectivity 
gm = GradientMaps(n_components=10,approach ='dm', kernel='normalized_angle', alignment='procrustes', random_state=0)
gm.fit(c_all, sparsity=0.9, reference=gm_template.gradients_)
    
# save gradient for each subject 
file_gm = open(grad_path + average + grad_fname, 'wb') 
pickle.dump(gm, file_gm)
file_gm.close()

