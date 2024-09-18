#!/bin/bash

# Note: the maximum number of jobs that can be submitted at the same time is 99

# General Inputs
Acc=24
RP_list="1,2,5,10,20,50,100,200,500,1000,2000,5000,10000"
Git_Repo="/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_ClimateNWP_4Points"
DirIN="Data/Compute/14_AccTP_SA"
DirOUT_Climate_SA="Data/Compute/15_Climate_SA"
DirOUT_Climate_G="Data/Compute/16_Climate_G"


############
# Reforecasts #
############
# YearS=1999
# YearF=2019
# Dataset_SystemFC="Reforecasts/ECMWF_46r1"

# NumSA_S=0
# NumSA_F=159 # Max NumSA_F = 159
# echo "Computing the rainfall climatology for $Dataset_SystemFC for sub-areas from n. $NumSA_S to n. $NumSA_F"
# for CodeSA in $(seq $NumSA_S $NumSA_F); do
#       sbatch 15a_SubmitterATOS_Climate_SA.sh ${YearS} ${YearF} ${Acc} ${CodeSA} ${RP_list} ${Dataset_SystemFC} ${Git_Repo} ${DirIN} ${DirOUT_Climate_SA} ${DirOUT_Climate_G}
# done


###########
# ERA5_EDA #
###########
# YearS=2000
# YearF=2019
# Dataset_SystemFC="Reanalysis/ERA5_EDA"

# NumSA_S=0
# NumSA_F=33 # Max NumSA_F = 33
# echo "Computing the rainfall climatology for $Dataset_SystemFC for sub-areas from n. $NumSA_S to n. $NumSA_F"
# for CodeSA in $(seq $NumSA_S $NumSA_F); do
#       sbatch 15a_SubmitterATOS_Climate_SA.sh ${YearS} ${YearF} ${Acc} ${CodeSA} ${RP_list} ${Dataset_SystemFC} ${Git_Repo} ${DirIN} ${DirOUT_Climate_SA} ${DirOUT_Climate_G}
# done


#######
# ERA5 #
#######
# YearS=2000
# YearF=2019
# Dataset_SystemFC="Reanalysis/ERA5"

# NumSA_S=0
# NumSA_F=159 # Max NumSA_F = 159
# echo "Computing the rainfall climatology for $Dataset_SystemFC for sub-areas from n. $NumSA_S to n. $NumSA_F"
# for CodeSA in $(seq $NumSA_S $NumSA_F); do
#       sbatch 15a_SubmitterATOS_Climate_SA.sh ${YearS} ${YearF} ${Acc} ${CodeSA} ${RP_list} ${Dataset_SystemFC} ${Git_Repo} ${DirIN} ${DirOUT_Climate_SA} ${DirOUT_Climate_G}
# done


##############
# ERA5_ecPoint #
##############
YearS=2000
YearF=2019
Dataset_SystemFC="Reanalysis/ERA5_ecPoint"

NumSA_S=0
NumSA_F=25 # Max NumSA_F = 219
echo "Computing the rainfall climatology for $Dataset_SystemFC for sub-areas from n. $NumSA_S to n. $NumSA_F"
for CodeSA in $(seq $NumSA_S $NumSA_F); do
      sbatch 15a_SubmitterATOS_Climate_SA.sh ${YearS} ${YearF} ${Acc} ${CodeSA} ${RP_list} ${Dataset_SystemFC} ${Git_Repo} ${DirIN} ${DirOUT_Climate_SA} ${DirOUT_Climate_G}
done
echo "Submitted SA n. ${NumSA_S} to ${NumSA_F}"
sleep 1h 30m

NumSA_S=26
NumSA_F=50 # Max NumSA_F = 219
echo "Computing the rainfall climatology for $Dataset_SystemFC for sub-areas from n. $NumSA_S to n. $NumSA_F"
for CodeSA in $(seq $NumSA_S $NumSA_F); do
      sbatch 15a_SubmitterATOS_Climate_SA.sh ${YearS} ${YearF} ${Acc} ${CodeSA} ${RP_list} ${Dataset_SystemFC} ${Git_Repo} ${DirIN} ${DirOUT_Climate_SA} ${DirOUT_Climate_G}
done
echo "Submitted SA n. ${NumSA_S} to ${NumSA_F}"
sleep 1h 30m

NumSA_S=51
NumSA_F=75 # Max NumSA_F = 219
echo "Computing the rainfall climatology for $Dataset_SystemFC for sub-areas from n. $NumSA_S to n. $NumSA_F"
for CodeSA in $(seq $NumSA_S $NumSA_F); do
      sbatch 15a_SubmitterATOS_Climate_SA.sh ${YearS} ${YearF} ${Acc} ${CodeSA} ${RP_list} ${Dataset_SystemFC} ${Git_Repo} ${DirIN} ${DirOUT_Climate_SA} ${DirOUT_Climate_G}
done
echo "Submitted SA n. ${NumSA_S} to ${NumSA_F}"
sleep 1h 30m

NumSA_S=76
NumSA_F=100 # Max NumSA_F = 219
echo "Computing the rainfall climatology for $Dataset_SystemFC for sub-areas from n. $NumSA_S to n. $NumSA_F"
for CodeSA in $(seq $NumSA_S $NumSA_F); do
      sbatch 15a_SubmitterATOS_Climate_SA.sh ${YearS} ${YearF} ${Acc} ${CodeSA} ${RP_list} ${Dataset_SystemFC} ${Git_Repo} ${DirIN} ${DirOUT_Climate_SA} ${DirOUT_Climate_G}
done
echo "Submitted SA n. ${NumSA_S} to ${NumSA_F}"
sleep 1h 30m

NumSA_S=101
NumSA_F=125 # Max NumSA_F = 219
echo "Computing the rainfall climatology for $Dataset_SystemFC for sub-areas from n. $NumSA_S to n. $NumSA_F"
for CodeSA in $(seq $NumSA_S $NumSA_F); do
      sbatch 15a_SubmitterATOS_Climate_SA.sh ${YearS} ${YearF} ${Acc} ${CodeSA} ${RP_list} ${Dataset_SystemFC} ${Git_Repo} ${DirIN} ${DirOUT_Climate_SA} ${DirOUT_Climate_G}
done
echo "Submitted SA n. ${NumSA_S} to ${NumSA_F}"
sleep 1h 30m

NumSA_S=126
NumSA_F=150 # Max NumSA_F = 219
echo "Computing the rainfall climatology for $Dataset_SystemFC for sub-areas from n. $NumSA_S to n. $NumSA_F"
for CodeSA in $(seq $NumSA_S $NumSA_F); do
      sbatch 15a_SubmitterATOS_Climate_SA.sh ${YearS} ${YearF} ${Acc} ${CodeSA} ${RP_list} ${Dataset_SystemFC} ${Git_Repo} ${DirIN} ${DirOUT_Climate_SA} ${DirOUT_Climate_G}
done
echo "Submitted SA n. ${NumSA_S} to ${NumSA_F}"
sleep 1h 30m

NumSA_S=151
NumSA_F=175 # Max NumSA_F = 219
echo "Computing the rainfall climatology for $Dataset_SystemFC for sub-areas from n. $NumSA_S to n. $NumSA_F"
for CodeSA in $(seq $NumSA_S $NumSA_F); do
      sbatch 15a_SubmitterATOS_Climate_SA.sh ${YearS} ${YearF} ${Acc} ${CodeSA} ${RP_list} ${Dataset_SystemFC} ${Git_Repo} ${DirIN} ${DirOUT_Climate_SA} ${DirOUT_Climate_G}
done
echo "Submitted SA n. ${NumSA_S} to ${NumSA_F}"
sleep 1h 30m

NumSA_S=175
NumSA_F=200 # Max NumSA_F = 219
echo "Computing the rainfall climatology for $Dataset_SystemFC for sub-areas from n. $NumSA_S to n. $NumSA_F"
for CodeSA in $(seq $NumSA_S $NumSA_F); do
      sbatch 15a_SubmitterATOS_Climate_SA.sh ${YearS} ${YearF} ${Acc} ${CodeSA} ${RP_list} ${Dataset_SystemFC} ${Git_Repo} ${DirIN} ${DirOUT_Climate_SA} ${DirOUT_Climate_G}
done
echo "Submitted SA n. ${NumSA_S} to ${NumSA_F}"
sleep 1h 30m

NumSA_S=201
NumSA_F=219 # Max NumSA_F = 219
echo "Computing the rainfall climatology for $Dataset_SystemFC for sub-areas from n. $NumSA_S to n. $NumSA_F"
for CodeSA in $(seq $NumSA_S $NumSA_F); do
      sbatch 15a_SubmitterATOS_Climate_SA.sh ${YearS} ${YearF} ${Acc} ${CodeSA} ${RP_list} ${Dataset_SystemFC} ${Git_Repo} ${DirIN} ${DirOUT_Climate_SA} ${DirOUT_Climate_G}
done
echo "Submitted SA n. ${NumSA_S} to ${NumSA_F}"