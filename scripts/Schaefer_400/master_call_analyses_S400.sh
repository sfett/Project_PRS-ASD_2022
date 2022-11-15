
#!/bin/bash

# Bash script for calling python functions for gradient analyses
# Working in Schaefer 400 parcellation space

serena_dir="/data/mica1/03_projects/serena/'

echo Hello, which dataset are you using (abcd, abide or ping)? 

read dataset

echo You are using the $dataset dataset


if $dataset="abide"
then
	
	#subjs_file=${serena_dir}'/ABIDE1/ABIDE_n211.csv'
	#ts_file=	

	#input_dir_fc=
	#output_grad_pth=

elif $dataset="ping"
then
	
	#subjects_file =
	#ts_file = 

	#input_dir_fc = 
	#output_dir_grads = 


elif $dataset="abcd"
then

	# subjects

	root_path='/data/mica2/ABCD/imaging/'
	subjects_file='${root_path}/ABCD_subjects_PRS_rsfMRI.txt'
	
	# rsfc 

	input_dir_fc='${root_path}/RSFC/'
	fc_fname='_rest_mc_skip_residc_interp_FDRMS0.3_DVARS50_bp_0.009_0.08_fs6_sm6_all2all.mat'
	fc_label='corr_mat'

	# gradients

	output_dir_grads='${root_path}/RSFC_gradients/Schaefer_400/'
	grad_fname ='_gm_Schaefer-400_dm_na_0.9'
	
fi #( ends conditional statement) 


# Compute FC 

# not needed for ABCD
# python compute_FC.py $ts_file $input_dir $ouput_dir_fc $fc_file $subjects_file $surf_vtp $surf_mat 


# Compute template & individual gradients 

template='hcp'
template_grad_pth='${serena_dir}/HCP/Schaefer_400/'


python create_individual_gradients_Schaefer400.py $subjects_file $input_dir_fc $fc_fname $fc_label $output_dir_grads $grad_fname $template $template_grad_path

 








done