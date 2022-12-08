#!/usr/bin/env python
# coding: utf-8

""" Compute functional connectivity matrices

This script allows the user to compute individual matrices of
functional connectivity from timeseries data. 

Inputs: 
Timeseries inputs are loaded in gifti format 

Outputs: 
Produces 400 x 400 correlation matrices
In Schaefer 400 parcellation space

File contains the following functions:
    * fill_empty_ts - fills timeseries values so none are empty 
    * get_con - computes pearson correlation
    * build_con - fisher z transfroms and saves output matrices 
  

This script includes portions of code written by Oualid Benkarim and Valeria Kebets.

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
ts_file = sys.argv[1]  #_s6_atlasroi_5k_fs_LR.func.gii
input_dir = sys.argv[2] #/data/mica2/ABIDE/Outputs/RSFC/timecourses_5k
output_dir = sys.argv[3] # /data/mica2/ABIDE/Outputs/RSFC/Schaefer_400 
fc_file = sys.argv[4] # name of output file for fc
subjects_file = sys.argv[5] #df of subjects 
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


def get_con(sid, input_dir, ts_file, parc, mask, fc_file, dist_ring,smooth=3):
    
    """ Pulls timeseries data and performs Pearson's correlation 
    across all vertices
    """

     # Load cortical timeseries
    pth_ctx = input_dir + sid + ts_file
    
    # load gifti timeseries
    try:
        ts_ctx = np.load(pth_ctx)
        print ("shape of timeseries" + str(ts_ctx.shape))
        #ts_ctx = ts_sub.agg_data()
    except:
        return None, None, None

    # Remove midline
    ts_ctx = ts_ctx[:mask.size]
    ts_ctx = ts_ctx[mask]

    if dist_ring is not None:
    # Fill remaining timeseries if zero (happens with small number of subjects)
        ts_ctx = fill_empty_ts(ts_ctx, dist_ring)
    
    # Average timeseries per cortical parcel
    ts_ctx = reduce_by_labels(ts_ctx, parc[mask], red_op='mean', axis=1, dtype=np.float32)
    
    # Compute Pearson's corr
    c = np.corrcoef(ts_ctx).astype(np.float32) # cortico-cortical FC
    
    return c


def build_con(df, dist_ring, input_dir, output_dir):

    """ Computes func connectivty across all subjects and 
    fisher Z tranforms using one of two methods. 
    
    Both methods aim to normalize pearson correlation values 
    but have  different approaches to treating the diagonal. 
    
    Method 1: replaces diagonal with highest relative value 
    of correlation. ("the Oualid method")
    
    Method 2: replaces diagonal with values of zero. 
    ("the Boris method")
    
    """
    for index, rw in df.iterrows():
        
        sid = str(rw.Subjects)
    
        print(sid) 
    
        FC = get_con(sid, input_dir, ts_file, parc, mask, fc_file) 
        
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
        print("gradient successfully computed for subject #" + sid)


#  Load surface files
surf = read_surface(surf_vtp) 
surf_file = sio.loadmat(surf_mat)
mask = surf_file['mask'].flatten()
dist_ring = get_immediate_distance(surf, metric='euclidean', mask=mask)


#  Choose parcellation surface 
parc = surf.PointData['schaefer400_yeo7']
n_ctx = np.unique(parc[mask]).size
print('Using Schaefer parcellation with 400 parcels')


# Load dataframe wit sIDs of cohort
df = pd.read_csv(subjects_file, header=None)
df = df.rename(columns={0: 'Subjects'})


# Build average connectivity matrices for all subjects
build_con(df, dist_ring, input_dir, output_dir)

