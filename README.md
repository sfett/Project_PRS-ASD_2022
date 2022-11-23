# PRS-ASD Project 2022

Project Objective: Examining the effects of genetic risk for autism spectrum disorder (via proxy of polygenic risk score) on functional connectivity. 

## Description

The scripts in this repository are divided into two categories based on your chosen surface space resolution. 

* **Conte69_5k:** Data in vertex-wise space. Surface derived from FreeSurfer segmentation. For the sake of this project, working in 5k resolution per hemisphere. 

* **Schaefer_400:** Data in parcellation space. Reduced dimensionality of high-resolution neuroimaging data by merging voxels into 400 parcels. 

## Specifics

### Dependencies

* The scripts utilize MICA's in-house toolboxes BrainSpace and BrainStat, and all their subsequent required packages must be installed in the python environment before analyses. 
* See installation guides here: [BrainSpace](https://brainspace.readthedocs.io/en/latest/pages/install.html#python-installation), [BrainStat]( https://brainstat.readthedocs.io/en/master/generic/install.html#python-installation)


### Code format

* All python scripts are designed to be called from a BASH script `master_call_analyses.sh`, where dataset specific inputs are to be defined. 


## Authors

Serena Fett   
[serena.fett@mail.mcgill.ca](serena.fett@mail.mcgill.ca)



