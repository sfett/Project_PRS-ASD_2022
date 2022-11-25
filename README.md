# PRS-ASD Project 2022

This project aims to examine the effects of genetic risk for autism (via proxy of polygenic risk score) on functional connectivity. Computational methods were used to probe the brain on multiple scales inlcuding: fMRI timeseries, functional connectomes and gradients. 

## Description

Scripts in this repository include building functional connectomes and gradients, harmonizing site data and plotting onto hemispheres. 
Scripts are divided into two categories based on your chosen surface space resolution. 

* **Conte69_5k:** Data in vertex-wise space. Surface derived from FreeSurfer segmentation. For the sake of this project, working in 5k resolution per hemisphere. 

* **Schaefer_400:** Data in parcellation space. Reduced dimensionality of high-resolution neuroimaging data by merging voxels into 400 parcels. 

## Specifics

### Dependencies

* The scripts utilize MICA's in-house toolboxes BrainSpace and BrainStat, as well as neuroCombat.
* All their subsequent required packages must be installed in the python environment before analyses. 
* See installation guides here: [BrainSpace](https://brainspace.readthedocs.io/en/latest/pages/install.html#python-installation), [BrainStat]( https://brainstat.readthedocs.io/en/master/generic/install.html#python-installation), [neuroCombat](https://github.com/Jfortin1/neuroCombat)

### Code format

* All python scripts are designed to be called from a BASH script `master_call_analyses.sh`, where dataset specific inputs (i.e., demographic files and paths) are to be defined. 


## Authors

Serena Fett   
[serena.fett@mail.mcgill.ca](serena.fett@mail.mcgill.ca)


