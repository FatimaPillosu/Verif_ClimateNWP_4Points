#!/bin/bash

###########################################################################################################################################
# CODE DESCRIPTION
# Retrieve_Climate_OBS.sh retrieves the observational (point) rainfall climatologies.

# DESCRIPTION OF INPUT PARAMETERS
# Git_Repo (string): path of local github repository.
# DirIN (string): full path of the directory containing the observational climatologies.
# DirOUT (string): relative path of the directory where the observational climatologies will be stored.

# INPUT PARAMETERS
Git_Repo="/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_ClimateNWP_4Points"
DirIN="/ec/vol/ecpoint_dev/mofp/Compute/Climate_OBS_tp/Data/Compute/12_Climate_OBS/10_AlignOBS_CleanSTVL/Coeff_Grid2Point_20/24h_2000_2019"
DirOUT="Data/Raw/Climate_OBS/tp_24h_2000_2019"
###########################################################################################################################################

# Copying the modelled climatologies from the input directory
mkdir -p "${Git_Repo}/${DirOUT}" 
cp ${DirIN}/* "${Git_Repo}/${DirOUT}" 