
#!/bin/bash

# Bash script for calling python functions for gradient analyses
# Working in Schaefer 400 parcellation space

serena_dir="/data/mica1/03_projects/serena/"

echo "Hello, which dataset are you using (abcd, abide or ping)?" 

read dataset

echo "You are using the $dataset dataset"

# define dataset specific inputs

if [[ "$dataset" == "abide" ]] ; then 

	echo "add abide inputs" 

	#subjs_file="${serena_dir}/ABIDE1/ABIDE_n211.csv"
	#ts_file=	

	#input_dir_fc=
	#output_grad_pth=

elif [[ "$dataset" == "ping" ]] ; then 
	
	echo "add ping inputs" 

	#subjects_file =
	#ts_file = 

	#input_dir_fc = 
	#output_dir_grads = 


elif [[ "$dataset" == "abcd" ]] ; then 

	# subjects

	root_path="/data/mica2/ABCD/imaging/"
	subjects_file="${root_path}/ABCD_subjects_PRS_rsfMRI.txt"
	
	# rsfc 
	
	input_dir_fc="${root_path}/RSFC/"
	fc_fname="_rest_mc_skip_residc_interp_FDRMS0.3_DVARS50_bp_0.009_0.08_fs6_sm6_all2all.mat"
	fc_label="corr_mat"

	# gradients

	output_dir_grads="${root_path}/RSFC_gradients/Schaefer_400/"
	grad_fname="_gm_Schaefer-400_dm_na_0.9"
	kernel='normalized_angle'


	# harmonization and linear model 
	demo ="${root_path}/abcd_demog_w_gradients_noPRS.csv" # needs to be updated with all PRS thresholds 

	
fi #( ends conditional statement) 

# Compute FC 

# not needed for ABCD
# python compute_FC.py $ts_file $input_dir $ouput_dir_fc $fc_file $subjects_file $surf_vtp $surf_mat 


# Compute template & individual gradients 


template="hcp" # set to name of dataset or None if no alignment to be performed. 
template_grad_path="${serena_dir}/HCP/Schaefer_400/" # path to dataset


#python create_individual_gradients_Schaefer400.py $subjects_file $input_dir_fc $fc_fname $fc_label #$output_dir_grads $grad_fname $template $template_grad_path


## Apply site harmonization 

d_gradient = 400 # dimension of gradient

# define covariates to input in model
# string must be same as it is written in column name in demographic file. 


# for continuous based variables
continuous_covar1 = "interview_age"
continuous_covar2 = "Pt_0.1" 


# for categorical variables
categorical_covar3 = "sex"


# the variable representing site to harmonize
batch_covar4 = "mri_info_manufacturer" 

python gradient_site_harmonization_S400.py $subjects_file $output_grad_pth $template $grad_fname $continuous_covar1 $continuous_covar2 $categorical_covar3 $batch_covar4 $kernel $dataset




