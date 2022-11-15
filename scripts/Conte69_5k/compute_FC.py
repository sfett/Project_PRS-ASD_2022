#!/usr/bin/env python
# coding: utf-8

""" Compute functional connectivity matrices

This script allows the user to compute individual matrices of
functional connectivity from timeseries data. 

Inputs: 
Timeseries inputs are loaded in gifti format 
Outputs

Outputs: 
Produces 10,000 x 10,000 correlation matrices
In Conte69 surface space (5k)

File contains the following functions:
    * fill_empty_ts - fills timeseries values so none are empty 
    * get_con - computes pearson correlation
    * build_con - fisher z transfroms and saves output matrices 
    
""" 

import os
import argparse
import numpy as np
import pandas as pd
import nibabel as nib
import scipy.io as sio
import sys

from brainspace.mesh.mesh_io import read_surface
from brainspace.mesh import mesh_elements as me
from brainspace.utils.parcellation import reduce_by_labels
from brainspace.mesh.mesh_elements import get_immediate_distance 


# call inputs in bash script
# can alternatively use argparse to define arguments
ts_file = sys.argv[1] 
input_dir = sys.argv[2]
output_dir = sys.argv[3]
fc_file = sys.argv[4]
subjects_file = sys.argv[5]
surf_vtp = sys.argv[6]
surf_mat = sys.argv[7]


def fill_empty_ts(ts, dist_ring):
    """Fill zero timeseries (if any) with average timeseries of
    immediate neighbors.
    """

    mk = np.all(ts == 0, axis=1)
    while mk.sum() > 0:
        idx_miss = np.where(mk)[0]
        x2 = [[idx, mk[dist_ring[idx].tocoo().col].sum(),
               dist_ring[idx].tocoo().col] for idx in idx_miss]

        idx = np.argmin(idx_miss)
        tidx, tn, tneigh = x2[idx]

        tneigh = tneigh[~mk[tneigh]]
        ts[tidx] = ts[tneigh].mean(0)
        mk[tidx] = False
    return ts


def get_con(sid, input_dir, ts_file, dist_ring, fc_file):
    
    """ Pulls timeseries data and performs Pearson's correlation 
    across all vertices
    """
    
    # Get timeseries -- cortex
    pth_ctx = input_dir + sid + ts_file
    
    # load gifti 
    ts_sub = nib.load(pth_ctx)
    ts = ts_sub.agg_data()
    
    # Fill remaining timeseries if zero (happens with small number of subjects)
   
    ts_ctx = fill_empty_ts(ts, dist_ring)
    
    # Pearson's corr
    c = np.corrcoef(ts_ctx).astype(np.float32) # cortico-cortical FC
    
    return c


def build_con(df, dist_ring, input_dir, output_dir):

    """ Computes func connectivty across all subjects and 
    fisher Z tranforms using one of two methods. 
    
    Both methods aim to normalize pearson correlation values 
    but have  different approaches to treating the diagonal. 
    
    Method 1: replaces diagonal with highest relative value 
    of correlation. (the Oualid method)
    
    Method 2: replaces diagonal with values of zero. 
    (the Boris method)
    
    """
    for index, rw in df.iterrows():
        
        sid = str(rw.Subjects)
        
        print(sid) 
    
        FC = get_con(sid, input_dir, ts_file, dist_ring)
        
        if FC is None:
            print(f'Discarding: {sid}')
            continue
            
        # Fisher z transform method 1
        #FCz = np.arctanh(FC)
        #FCz = np.clip(FCz, np.arctanh(-1+np.spacing(1)), np.arctanh(1-np.spacing(1)))
        
    	# Fisher Z transform method 2
        FCz = np.arctanh(FC)
        FCz[~np.isfinite(FCz)] = 0
        
        # save both matrices within subject directory
        np.savez_compressed(output_dir + sid + fc_file, FC=FC, FCz=FCz)        
    
    
# load dataframe with sIDs of final cohort
df = pd.read_csv(subjects_file, header=None)
df = df.rename(columns={0: 'Subjects'})


# Load surface files
surf = read_surface(surf_vtp)
surf_file = sio.loadmat(surf_mat)
mask = surf_file['mask'].flatten()
dist_ring = get_immediate_distance(surf, metric='euclidean', mask=mask)


# Build average connectivity matrices for ASD and TD
build_con(df, dist_ring, input_dir, output_dir)




