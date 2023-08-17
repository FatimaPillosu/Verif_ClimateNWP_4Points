#!/bin/bash

#SBATCH --job-name=Compute_ClimateFC_atOBS
#SBATCH --output=LogATOS/Compute_ClimateFC_atOBS-%J.out
#SBATCH --error=LogATOS/Compute_ClimateFC_atOBS-%J.out
#SBATCH --cpus-per-task=1
#SBATCH --mem=64G
#SBATCH --qos=nf
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=fatima.pillosu@ecmwf.int

# INPUTS
SystemFC_list=${1}

# CODE
time python3 11_Compute_Climate_FC_atOBS.py ${SystemFC_list}
