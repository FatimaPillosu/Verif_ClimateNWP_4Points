#!/bin/bash

###########################################################################################
# CODE DESCRIPTION
# Retrieve_Climate_NWP.sh retrieves the NWP modelled rainfall climatologies.

# DESCRIPTION OF INPUT PARAMETERS
# Git_Repo (string): path of local github repository.
# DirIN (string): full path of the directory containing the modelled climatologies.
# DirOUT (string): relative path of the directory where the modelled climatologies will be stored.

# INPUT PARAMETERS
Git_Repo="/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_ClimateNWP_4Points"
DirIN="/ec/vol/ecpoint_dev/mofp/Compute/Climate_NWP_tp/Data/Compute/03_Climate_G/24h_2000_2019"
DirOUT="Data/Raw/Climate_NWP/tp_24h_2000_2019"
###########################################################################################

# Copying the modelled climatologies from the input directory
mkdir -p "${Git_Repo}/${DirOUT}" 
cp -r ${DirIN}/* "${Git_Repo}/${DirOUT}" 