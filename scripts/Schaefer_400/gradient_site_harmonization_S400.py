#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""

Nov 15, 2022. @author: serenafett 


This script performs the harmonization of multi-site imaging data 
with neuroComBat. 


Inputs: 
    
    * dataframe containing demographic information (.csv)
    * Individual functional gradients (.pickle)
    
Outputs:
    
    * The nth  gradient for every subject after harmonization (.pickle)
        (gradient dimension, n subjects)
     
    
This script requires that `neuroCombat`--and all its necessary packages--be
installed within the Python environment. 
(See: https://github.com/Jfortin1/neuroCombat)


This script is to be called from an external bash script (.sh) where all 
dataset specific paths and inputs are to be already defined. 

"""



# coding: utf-8

from neuroCombat import neuroCombat
import pandas as pd
import numpy as np
import pickle
import seaborn as sns
import matplotlib.pyplot as plt


# load dataframe of subjects
df = pd.read_csv("/data/mica1/03_projects/serena/scripts/ABIDE/abide_func_fn_abideI.csv")
df = df.loc[df['Func_MeanFD'] < 0.3]
df = df[["ID", "Group", "Site", "Age"]]
df.reset_index(inplace=True, drop=True)

# create empty array 
sub = len(df.index)
data1 = np.zeros((9116,sub))
data2 = np.zeros((9116,sub))
data3 = np.zeros((9116,sub))


root_path = '/data/mica2/ABIDE/Outputs/RSFC_gradients/Conte69_5k/cosine/'

for index,rw in df.iterrows():

    sid = str(rw.ID)
    
    sub_path = root_path + 'sub-' + sid + "_gm_aligned_hcp_cosine.pickle"
    
    # load gradient
    file_to_read = open(sub_path, "rb")
    gm_ASD = pickle.load(file_to_read)
    
    # extract specific gradients
    first_g = (gm_ASD.aligned_[:,0])
    second_g = (gm_ASD.aligned_[:,1])
    third_g = (gm_ASD.aligned_[:,2])
    
    # add to array
    data1[:,index]= first_g
    data2[:,index]= second_g
    data3[:,index]= third_g


print(data1.shape)
print(data2.shape)
print(data3.shape)


## NEUROCOMBAT SITE HARMONIZATION

# Specifying all the covariates
covars = df[['Age','Site', "Group"]]

# To specify names of the variables that are categorical:
categorical_cols = ["Group"]

# To specify continuous variables 
continuous_cols = ['Age']

# To specify the name of the variable that encodes for the scanner/batch covariate:
batch_col = 'Site'

covars
covars.to_csv('/data/mica1/03_projects/serena/ABIDE1/ABIDE_n211.csv')


# Harmonize FIRST gradient
data = data1 
data_combat = neuroCombat(dat=data,
    covars=covars,
    batch_col=batch_col,
    categorical_cols=categorical_cols, continuous_cols=continuous_cols)["data"]
# save harmonized first gradient
np.savez_compressed(root_path + "harmonized_first_cosine_gradient_ABIDE_n211.npz", data_combat=data_combat) 



# Harmonize SECOND gradinet
data = data2
data_combat = neuroCombat(dat=data,
    covars=covars,
    batch_col=batch_col,
    categorical_cols=categorical_cols, continuous_cols=continuous_cols)["data"]
# save harmonized second gradinet
np.savez_compressed(root_path + "harmonized_second_cosine_gradient_ABIDE_n211.npz", data_combat=data_combat) 



# Harmonize THIRD gradinet
data = data3
data_combat = neuroCombat(dat=data3,
    covars=covars,
    batch_col=batch_col,
    categorical_cols=categorical_cols, continuous_cols=continuous_cols)["data"]
# save harmonized third gradinet
np.savez_compressed(root_path + "harmonized_third_cosine_gradient_ABIDE_n211.npz", data_combat=data_combat) 


## to visualize data 
#(before harmonization)

print(np.min(data))
print(np.min(data_combat))

plt.figure()

plt.subplot(121)
heat_map = sns.heatmap(data, vmin=-0.2, vmax=0.2)

plt.subplot(122)
heat_map2 = sns.heatmap(data_combat, vmin=-0.2, vmax=0.2)

plt.show()

