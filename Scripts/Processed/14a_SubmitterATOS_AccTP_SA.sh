#!/bin/bash

#SBATCH --job-name=AccTP_SA
#SBATCH --output=LogATOS/AccTP_SA-%J.out
#SBATCH --error=LogATOS/AccTP_SA-%J.out
#SBATCH --cpus-per-task=64
#SBATCH --mem=128G
#SBATCH --time=2-00:00:00
#SBATCH --qos=nf
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=fatima.pillosu@ecmwf.int

# INPUTS
Year=${1}
Acc=${2}
NumSA=${3}
SystemFC=${4}
Git_Repo=${5}
DirIN=${6}
DirOUT=${7}

python3 01_Compute_AccTP_SA.py $Year $Acc $NumSA $SystemFC $Git_Repo $DirIN $DirOUT