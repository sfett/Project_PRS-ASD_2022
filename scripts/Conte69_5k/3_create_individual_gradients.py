#!/usr/bin/env python
# coding: utf-8

"""
Oct 6, 2022. @author: serenafett 

This script computes individual gradients from functional connectivity matrices of 10k x 10k resolution. 
Option is provided for gradients to be aligned to a reference gradient. 

Inputs: 
    
    * List of subjects ID (.csv)
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
import pickle
import numpy as np
import pandas as pd
import sys

from brainspace.mesh.mesh_io import read_surface
from brainspace.gradient import GradientMaps


# Call variables from bash script
subjects_file = sys.argv[1]
template_grad = sys.argv[2]
input_dir = sys.argv[3]
output_dir = sys.argv[4]
ts_file = sys.argv[5]
kernel = sys.argv[6]
grad_fname = sys.argv[7]


# load subjects list
df = pd.read_csv(subjects_file, header=None)
df = df.rename(columns={0: 'Subjects'})


# load template gradient
file_to_read = open(template_grad + ".pickle", "rb")
gm_temp = pickle.load(file_to_read)


for index,rw in df.iterrows():

    sid = str(rw.Subjects)
    print(sid)
    
    sub_path = input_dir + sid + ts_file
    
    data = np.load(sub_path)
    FCz = data['FCz'] # load Fisher-Z data
    
    # compute gradient
    gm = GradientMaps(n_components=10,approach ='dm', kernel=kernel, alignment='procrustes', random_state=0)
    gm.fit(FCz, sparsity=0.9, reference=gm_temp.gradients_)
    
    # save gradient for each subject 
    file = open(output_dir + "sub-" + sid + grad_fname + ".pickle", 'wb') 
    pickle.dump(gm, file)
    file.close()

    
    
