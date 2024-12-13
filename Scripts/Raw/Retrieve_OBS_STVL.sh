#!/bin/bash

#####################################################################
# CODE DESCRIPTION
# Retrieve_OBS_STVL.sh retrieves 24-hourly rainfall observations from the STVL 
# database @ECMWF. Database description available here: 
# https://confluence.ecmwf.int/display/VER/STVL+datasets
# Code runtime: up to 1 hour.

# DESCRIPTION OF INPUT PARAMETERS
# Acc (number, in hours): accumulation period for rainfall.
# DateS (integer, in YYYYMMDD format): start date to retrieve.
# DateF (integer, in YYYYMMDD format): final date to retrieve.
# Dataset_array (array of strings): list of available datasets in stvl.
# Git_Repo (string): path of local GitHub repository.
# DirOUT (string): relative path for the output directory.

# INPUT PARAMETERS
Acc=24
DateS=20000101
DateF=20200101
Dataset_array=("synop" "hdobs" "bom" "india" "efas" "vnm")
Git_Repo = "/ec/vol/ecpoint_dev/mofp/papers_2_write/Verif_ClimateNWP_4Points"
DirOUT="Data/Raw/OBS/STVL"
#####################################################################

# Setting general parameters
DateS=$(date -d $DateS +%Y%m%d)
DateF=$(date -d $DateF +%Y%m%d)

# Retrieving observations for a considered dataset
for Dataset in ${Dataset_array[@]}; do 

    # Setting main directory
    MainDir=${Git_Repo}/${DirOUT}_${Acc}h/${Dataset}
    mkdir -p ${MainDir}
    
    TheDate=${DateS}
    while [[ ${TheDate} -le ${DateF} ]]; do
        
        echo "Retrieving ${Acc}-hourly rainfall observations from ${Dataset} for ${TheDate}..."
    
        # Creating the sub-directories for each considered date
        Dir_temp=${MainDir}/${TheDate}
        mkdir -p ${Dir_temp}
 
        # Retrieve the rainfall observations for the considered date
        ~moz/bin/stvl_getgeo --parameter tp --sources ${Dataset} --period ${Acc} --dates ${TheDate} --times 0/to/23/by/1 --columns value_0 elevation --outdir ${Dir_temp} --flattree

        # Delete empty temporary directories
        if [ -z "$(ls -A ${Dir_temp})" ]; then
            rm -rf ${Dir_temp}
	    fi

    TheDate=$(date -d "${TheDate} + 1 day" +"%Y%m%d")

    done 

done