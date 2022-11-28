%% This MATLAB script is used to downsample timeseries data from higher resolution (i.e., 32k) to lower (i.e.,5k) in conte69 space. 
%% Downsampling timeseries data is often used for purposes of computational efficiency, especially with large datasets. 

root_path = '/data/mica3/BIDS_PING/derivatives/micapipe/' ;
surf_path = '/github/Project_PRS-ASD_2022/surfaces/' ; 

% file name of inital resolution 
input_ts_name = '_ses-01_rsfmri_space-conte69-32k_desc-timeseries_clean.txt' 

% file name of target downsample resolution
output_ts_name = '_ses-01_rsfmri_space-conte69-10k_desc-timeseries_clean.txt'

% Load subject list
subj = %uplaod csv file of subjects
S = readtable(subj);
sID = S.Subjects;

% Get mapping 32k -> 10k
load(fullfile(surf_path, 'fsaverage.midthickness_mni_32k_fs_LR.mat');
C69 = G; clear G;

load(fullfile(surf_path, 'conte69_10k.mat');

C69_10k = struct('coord', coord, 'tri', int32(tri));
downSampIdx = idx;

g = gifti(fullfile(surf_path, 'conte69_10k.surf.gii');

% Iterate for all subjects
for sub = 1:length(sID)
    sub_path = fullfile(root_path,['sub-' sID{sub}], 'ses-01','func','surfaces');
    sub_file = fullfile(sub_path, ['sub-' sID{sub}, input_ts_name]) ;
    TS_clean = load(sub_file);
    
    %remove first 48 vertices 
    TS_clean(:,1:48)=[];

    % Downsample to 10k
    for iter = 1:length(downSampIdx)
        this_idx = downSampIdx(iter);
        TS_clean_10k(:,iter) = TS_clean(:,this_idx);
        clear this_idx
    end

    % Create a table with the data and variable namesp
    T = table(TS_clean_10k);
    
    % Write data to text file
    writetable(T,fullfile(sub_path, ['sub-' sID{sub}, output_ts_name]),'WriteVariableNames',0);
    
    clear T TS_clean TS_clean_10k sub_path sub_file
end 
