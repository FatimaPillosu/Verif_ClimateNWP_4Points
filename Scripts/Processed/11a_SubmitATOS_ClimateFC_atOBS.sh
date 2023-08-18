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
YearS=${1}
YearF=${2}
SystemFC_list=${3}

# CODE
time python3 11_Compute_ClimateFC_atOBS.py ${YearS} ${YearF} ${SystemFC_list}