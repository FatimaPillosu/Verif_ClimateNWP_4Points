#!/bin/bash

##################################################################################################################
# CODE DESCRIPTION
# Retrieve_ERA5_ecPoint.sh retrieves 24-hourly ERA5-ecPoint rainfall reanalysis (point-scale over the ERA5 grid, at 31 km spatial resolution). 
# The total precipitation is already accumulated over the period of interest.
# Code runtime: up to 1 hour.

# DESCRIPTION OF INPUT PARAMETERS
# Git_Repo (string): path of local GitHub repository.
# DirIN (string): absolute path of the directory containing the 24-hourly ecPoint-ERA5 rainfall reanalysis.
# DirOUT (string): relative path of the output directory.

# INPUT PARAMETERS
Git_Repo="/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_ClimateNWP_4Points"
DirIN_full="/ec/vol/ecpoint/mofp/reanalysis/ERA5_ecPoint/SemiOper/ECMWF_ERA5/0001/Rainfall/024/Code2.0.0_Cal1.0.0/Pt_BC_PERC"
DirOUT="Data/Raw/NWP/Reanalysis/ERA5_ecPoint_24h"
##################################################################################################################


# Setting output directories
DirOUT_temp=${Git_Repo}/${DirOUT}
mkdir -p ${DirOUT_temp}

# Retrieving ecPoint_ERA5 rainfall forecasts
echo "Retrieving 24-hourly ERA5_ecPoint rainfall reanalysis..."
cd ${DirIN_full}; cp -r 200* 201* ${DirOUT_temp}