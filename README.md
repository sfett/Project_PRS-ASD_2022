# PRS-ASD Project 2022

Project Objective: Examining the effects of genetic risk for autism spectrum disorder (via proxy of polygenic risk score) on functional connectivity. 

## Description

The scripts in this repository are divided into two categories based on your chosen surface space resolution. 

* **Conte69_5k:** Data in vertex-wise space. Surface derived from FreeSurfer segmentation. For the sake of this project, working in 5k resolution per hemisphere. 

* **Schaefer_400:** Data in parcellation space. Reduced dimensionality of high-resolution neuroimaging data by merging voxels into 400 parcels, or brain regions. 

## Getting Started

### Dependencies

* The scripts utilize MICA's in-house toolboxes BrainSpace and BrainStat, and all their subsequent required packages must be installed in the python environment before analyses. 
* See installation guides here: [BrainSpace](https://brainspace.readthedocs.io/en/latest/pages/install.html#python-installation), [BrainStat]( https://brainstat.readthedocs.io/en/master/generic/install.html#python-installation)


### Code format

* All python scripts are designed to be called from a BASH script `master_call_analyses.sh`, where dataset specific inputs are to be defined. 


## Authors

Serena Fett   
[serena.fett@mail.mcgill.ca](serena.fett@mail.mcgill.ca)

## Acknowledgments


### BrainSpace

Code available here: [BrainSpace ](https://github.com/MICA-MNI/BrainSpace)

Vos de Wael, R., Benkarim, O., Paquola, C. et al. BrainSpace: a toolbox for the analysis of macroscale gradients in neuroimaging and connectomics datasets. Commun Biol 3, 103 (2020). https://doi.org/10.1038/s42003-020-0794-7

### BrainStat

Code available here:  [BrainStat ](https://github.com/MICA-MNI/BrainStat)

Vos de Wael, R. V., Bayrak, Ş., Benkarim, O. et al. BrainStat: A toolbox for brain-wide statistics and Multimodal Feature Associations. (2022) https://doi.org/10.1101/2022.01.18.476795 

### neuroCombat 

Code available here [neuroCombat](https://github.com/Jfortin1/neuroCombat)

Fortin, J. P., Cullen, N., Sheline, Y. I. et al. (2018). Harmonization of cortical thickness measurements across scanners and sites. NeuroImage, 167, 104–120. https://doi.org/10.1016/j.neuroimage.2017.11.024

