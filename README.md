# PRS-ASD Project 2022

This project aims to examine the effects of genetic risk for autism (via proxy of polygenic risk score) on functional connectivity. Specifically, the relationship between elevated genetic risk and abnormalities in the sensory-fugal gradient in a cohort of typically developed youth. 

Computational methods were used to probe the brain on multiple scales inlcuding: fMRI timeseries, functional connectomes and gradients. 

For further background on functional gradients, see ([Margulies et al., 2016](https://www.pnas.org/doi/10.1073/pnas.1608282113)) and ([Hong et al., 2019](https://rdcu.be/c0z9K)). 

## Description

Scripts in this repository include building functional connectomes and gradients, harmonizing site data and plotting onto hemispheres. 

**/scripts** is divided into two categories based on your chosen surface space resolution. 

#### *Schaefer 400*
* Data in parcellation space.
* Reduced dimensionality of high-resolution neuroimaging data by averaging voxels into 400 parcels, or brain regions. 
* See: [Schaefer et al., 2018](https://pubmed.ncbi.nlm.nih.gov/28981612/)

#### *Conte69 (5k)*

* Data in vertex-wise space.
* Conte69 (a.k.a fsLR) is a surface-based atlas generated from 69 healthy adults registered to the fsLR surface mesh. 
* For the sake of computational efficiency, we used a resolution of 5k per hemisphere. 
* Files needed for the construction of the surface space can be found in the **/surfaces** directory. 


## Getting Started

### Dependencies

* The scripts utilize MICA's in-house toolboxes BrainSpace and BrainStat, and all their subsequent required packages must be installed in the python environment before analyses. 
* See installation guides here: [BrainSpace](https://brainspace.readthedocs.io/en/latest/pages/install.html#python-installation), [BrainStat]( https://brainstat.readthedocs.io/en/master/generic/install.html#python-installation)


### Code format

* All python scripts are designed to be called from an external BASH script, where dataset specific inputs are to be defined. 
* Written in Python 3.8


## Authors

Serena Fett   
[serena.fett@mail.mcgill.ca](serena.fett@mail.mcgill.ca)

## Acknowledgments

### BrainSpace

Code available here: [BrainSpace ](https://github.com/MICA-MNI/BrainSpace)

Vos de Wael, R., Benkarim, O., Paquola, C. et al. BrainSpace: a toolbox for the analysis of macroscale gradients in neuroimaging and connectomics datasets. Commun Biol 3, 103 (2020). https://doi.org/10.1038/s42003-020-0794-7

### BrainStat

Code available here:  [BrainStat ](https://github.com/MICA-MNI/BrainStat)

Vos de Wael, R., Bayrak, Ş., Benkarim, O. et al. BrainStat: A toolbox for brain-wide statistics and Multimodal Feature Associations. (2022) https://doi.org/10.1101/2022.01.18.476795 

### neuroCombat 

Code available here: [neuroCombat](https://github.com/Jfortin1/neuroCombat)

Fortin, J. P., Cullen, N., Sheline, Y. I. et al. Harmonization of cortical thickness measurements across scanners and sites. (2018) NeuroImage, 167, 104–120. https://doi.org/10.1016/j.neuroimage.2017.11.024



