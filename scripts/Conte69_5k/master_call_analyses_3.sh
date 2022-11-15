
#!/bin/bash


# define some initial general variables 

serena_dir="/data/mica1/03_projects/serena/"
surf_mat="/data/mica1/03_projects/valeria/micasoft/parcellations/conte69_10k/conte69_10k.mat"
surf_vtp=$serena_dir+='conte69_5k_new.vtp'
kernel="normalized_angle"
alignment="hcp_procrustes_aligned"


# define which dataset first 

dataset="abide"

if $dataset="abide"
then

	subjects_file=$serena_dir+='/ABIDE1/ABIDE_n211.csv'

	ts_file="_s6_atlasroi_5k_fs_LR.func.gii"

	grad_fname="ABIDE'+=$alignment+=$kernel"

	input_dir="/data/mica2/ABIDE/Outputs/RSFC/timecourses_5k/"

	output_dir_fc="/data/mica2/ABIDE/Outputs/RSFC/Conte69_5k"

elif $dataset="ping"
then
	#ts_file = ### 
	#subjects_file = ###


elif $dataset="abcd"
then
	#ts_file= 
	#subjects_file= ####

fi (to end conditional statement) 


# identify all the master python scripts 

	# compute FC 
	# compute template grad 
	# compute individual grads from FC 
	# compute average grads from FC 
	# site harmonization on grads 
	# linear models 


# Compute FC 

#python compute_FC.py $ts_file $input_dir $ouput_dir_fc $fc_file $subjects_file $surf_vtp $surf_mat 


# Compute template gradient 

fc_file="/data/mica1/03_projects/serena/scripts/HCP_mean_connectivity_n217_v2.npz"
output_dir_temp="/data/mica1/03_projects/serena/HCP/"
output_name = ##

python compute_template_gradient.py $fc_file $surf_mat $kernel $output_dir_temp $output_name 


# Compute individual gradients 

template_grad="/data/mica2/ABIDE/Outputs/RSFC_gradients/Conte69_5k/cosine/HCP_N217_4ses_mean_gradient_cosine.pickle"
input_dir_fc="/data/mica2/ABIDE/Outputs/RSFC/Conte69_5k/"
output_grad_pth="/data/mica2/ABIDE/Outputs/RSFC_gradients/Conte69_5k/cosine/"


python create_individual_gradients.py $subjects_file $template_grad $input_dir_fc $output_dir_fc $ts_file $kernel $grad_name


done