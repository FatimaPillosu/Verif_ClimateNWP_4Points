#!/bin/bash

######################################################################
# CODE DESCRIPTION
# Retrieve_ERA5_ecPoint.sh retrieves 12- and 24-hourly ERA5-ecPoint rainfall 
# analysis (point-scale over the ERA5 grid, at 31 km spatial resolution). The total 
# precipitation is already accumulated over the period of interest.

# DESCRIPTION OF INPUT PARAMETERS
# Acc (integer, in hours): accumulation period to consider.
# Git_Repo (string): path of local GitHub repository.
# DirIN_full (string): full path of the directory containing ecPoint-ERA5 rainfall analysis.
# DirOUT (string): relative path of the output directory.

# INPUT PARAMETERS
Acc=24
Git_Repo="/ec/vol/ecpoint_dev/mofp/Compute/Climate_NWP_tp"
DirIN_full="/ec/vol/highlander/ERA5_ecPoint_70yr"
DirOUT="Data/Raw/Reanalysis/ERA5_ecPoint"
######################################################################


# Setting input directories
DirIN_full_Pt=${DirIN_full}/Rainfall_${Acc}h/Pt_BC_PERC

# Setting output directories
DirOUT_Pt=${Git_Repo}/${DirOUT}_${Acc}h/Pt_BC_PERC
mkdir -p ${DirOUT_Pt}

# Retrieving ecPoint_ERA5 rainfall forecasts
echo "Retrieving ERA5_ecPoint..."
cd ${DirIN_full_Pt}; cp -r 200* 201* ${DirOUT_Pt}