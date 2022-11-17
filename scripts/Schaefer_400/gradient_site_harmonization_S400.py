#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""

Nov 15, 2022. @author: sfett 


This script performs the harmonization of multi-site imaging data 
using neuroComBat. 


Inputs: 
    
    * dataframe containing demographic information (.csv)
    * Individual functional gradients (.pickle)
    
Outputs:
    
    * The nth  gradient for all subjects after harmonization (.pickle)
        (gradient dimension, n subjects)
     
    
This script requires that `neuroCombat`--and all its necessary packages--be
installed within the Python environment. 
(See: https://github.com/Jfortin1/neuroCombat)

Note: This script is to be called from an external bash script (.sh) where all 
dataset specific paths and inputs are to be already defined. 

"""

from neuroCombat import neuroCombat
import pandas as pd
import numpy as np
import pickle
import seaborn as sns
import matplotlib.pyplot as plt
import sys 


# Call input variables from bash script

# Gradient specifics
df = sys.argv[1] 
d_grad = sys.argv[2]
grad_path = sys.argv[3]
alignment = sys.argv[4]
grad_fname = sys.argv[5] 


# for neuroCombat
# for continuous based variables
continuous_covar1 = sys.argv[6]
continuous_covar2 = sys.argv[7]

# for categorical variables
categorical_covar3 = sys.argv[8]

# the variable representing site to harmonize
batch_covar4 = sys.argv[9]

# output details
kernel = sys.argv[10]
dataset = sys.argv[11]


# create empty arrays
sub = len(df.index) # number of subjects in the file
# for our analyses, only care about first three gradients 
gradient1 = np.zeros((int(d_grad), sub))
gradient2 = np.zeros((int(d_grad), sub))
gradient3 = np.zeros((int(d_grad), sub))


for index,rw in df.iterrows():

    sid = str(rw.ID)
    
    
    sub_path = grad_path + sid + alignment + grad_fname + ".pickle"
    
    # load gradient
    file_to_read = open(sub_path, "rb")
    gm = pickle.load(file_to_read)
    
    if alignment is not None: 
        
        key = "aligned_"
    
    else:
        key = "gradients_"
        
    # extract specific gradients
    first_g = (("gm." + key)[:,1])
    second_g = (("gm." + key)[:,2])
    third_g = (("gm." + key)[:,3])
    
    # add to array
    gradient1[:,index]= first_g
    gradient2[:,index]= second_g
    gradient3[:,index]= third_g


print(gradient1.shape)
print(gradient2.shape)
print(gradient3.shape)


## NEUROCOMBAT SITE HARMONIZATION

# Specifying all the covariates
covars = df[[continuous_covar1, continuous_covar2, categorical_covar3, batch_covar4]]

# specify the variables that are categorical:
categorical_cols = [categorical_covar3]

# specify continuous variables 
continuous_cols = [continuous_covar1,continuous_covar2]

# specify the variable that encodes for the scanner/batch covariate:
batch_col = [batch_covar4]


# Harmonize FIRST gradient
data = gradient1 
data_combat = neuroCombat(dat=data,
    covars=covars,
    batch_col=batch_col,
    categorical_cols=categorical_cols, continuous_cols=continuous_cols)["data"]
# save harmonized first gradient
np.savez_compressed(grad_path + \
                    "harmonized_first" + kernel + "_gradient_" + dataset + "n" + sub + ".npz", \
                    data_combat=data_combat)
                  
    
# Harmonize SECOND gradient
data = gradient2
data_combat = neuroCombat(dat=data,
    covars=covars,
    batch_col=batch_col,
    categorical_cols=categorical_cols, continuous_cols=continuous_cols)["data"]
# save harmonized second gradinet
np.savez_compressed(grad_path + \
                    "harmonized_second" + kernel + "_gradient_" + dataset + "n" + sub + ".npz", \
                    data_combat=data_combat)
                    
    
# Harmonize THIRD gradient
data = gradient3
data_combat = neuroCombat(dat=data,
    covars=covars,
    batch_col=batch_col,
    categorical_cols=categorical_cols, continuous_cols=continuous_cols)["data"]
# save harmonized third gradinet
np.savez_compressed(grad_path + \
                    "harmonized_first" + kernel + "_gradient_" + dataset + "n" + sub + ".npz", \
                    data_combat=data_combat)
       

data_testing = "checking if update worked" 
    
## to visualize data 
##before harmonization and after harmonization

# plt.figure()
# plt.subplot(121)
# heat_map = sns.heatmap(data, vmin=-0.2, vmax=0.2)
# plt.subplot(122)
# heat_map2 = sns.heatmap(data_combat, vmin=-0.2, vmax=0.2)
# plt.show()

