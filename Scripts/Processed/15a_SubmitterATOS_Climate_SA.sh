#!/bin/bash

#SBATCH --job-name=Climate_SA
#SBATCH --output=LogATOS/Climate_SA-%J.out
#SBATCH --error=LogATOS/Climate_SA-%J.out
#SBATCH --cpus-per-task=64
#SBATCH --mem=128G
#SBATCH --time=2-00:00:00
#SBATCH --qos=nf
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=fatima.pillosu@ecmwf.int

# INPUTS
YearS=${1}
YearF=${2}
Acc=${3}
CodeSA=${4}
RP_list=${5}
Dataset_SystemFC=${6}
Git_Repo=${7}
DirIN=${8}
DirOUT_Climate_SA=${9}
DirOUT_Climate_G=${10}

python3 15_Compute_Climate_SA.py ${YearS} ${YearF} ${Acc} ${CodeSA} ${RP_list} ${Dataset_SystemFC} ${Git_Repo} ${DirIN} ${DirOUT_Climate_SA} ${DirOUT_Climate_G}