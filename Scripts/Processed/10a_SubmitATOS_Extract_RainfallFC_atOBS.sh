#!/bin/bash

#SBATCH --job-name=Extract_Rainfall_atOBS
#SBATCH --output=LogATOS/Extract_Rainfall_atOBS-%J.out
#SBATCH --error=LogATOS/Extract_Rainfall_atOBS-%J.out
#SBATCH --cpus-per-task=1
#SBATCH --mem=64G
#SBATCH --qos=nf
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=fatima.pillosu@ecmwf.int

# INPUTS
Year=${1}
SystemFC_list=${2}

# CODE
python3 10_Compute_Extract_RainfallFC_atOBS.py ${Year} ${SystemFC_list}