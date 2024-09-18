#!/bin/bash

############
# Reforecasts #
############

Year_S=1999
Year_F=2019
Acc=24
NumSA=160
Dataset_SystemFC="Reforecasts/ECMWF_46r1"
Git_Repo="/ec/vol/ecpoint_dev/mofp/Compute/Climate_NWP_tp"
DirIN="Data/Raw"
DirOUT="Data/Compute/01_AccTP_SA"

echo "Extracting realizations for ${Acc}-hourly rainfall for the following years:"
for Year in $(seq $Year_S $Year_F); do
      echo " - $Year"
      sbatch 01a_SubmitterATOS_AccTP_SA.sh $Year $Acc $NumSA $Dataset_SystemFC $Git_Repo $DirIN $DirOUT
done


###########
# ERA5_EDA #
###########

Year_S=2000
Year_F=2019
Acc=24
NumSA=34
Dataset_SystemFC="Reanalysis/ERA5_EDA"
Git_Repo="/ec/vol/ecpoint_dev/mofp/Compute/Climate_NWP_tp"
DirIN="Data/Raw"
DirOUT="Data/Compute/01_AccTP_SA"

echo "Extracting realizations for ${Acc}-hourly rainfall for the following years:"
for Year in $(seq $Year_S $Year_F); do
      echo " - $Year"
      sbatch 01a_SubmitterATOS_AccTP_SA.sh $Year $Acc $NumSA $Dataset_SystemFC $Git_Repo $DirIN $DirOUT
done


#######
# ERA5 #
#######

Year_S=2000
Year_F=2019
Acc=24
NumSA=160
Dataset_SystemFC="Reanalysis/ERA5"
Git_Repo="/ec/vol/ecpoint_dev/mofp/Compute/Climate_NWP_tp"
DirIN="Data/Raw"
DirOUT="Data/Compute/01_AccTP_SA"

echo "Extracting realizations for ${Acc}-hourly rainfall for the following years:"
for Year in $(seq $Year_S $Year_F); do
      echo " - $Year"
      sbatch 01a_SubmitterATOS_AccTP_SA.sh $Year $Acc $NumSA $Dataset_SystemFC $Git_Repo $DirIN $DirOUT
done


##############
# ERA5-ecPoint #
##############

Year_S=2000
Year_F=2019
Acc=24
NumSA=220
Dataset_SystemFC="Reanalysis/ERA5_ecPoint"
Git_Repo="/ec/vol/ecpoint_dev/mofp/Compute/Climate_NWP_tp"
DirIN="Data/Raw"
DirOUT="Data/Compute/01_AccTP_SA"

echo "Extracting realizations for ${Acc}-hourly rainfall for the following years:"
for Year in $(seq $Year_S $Year_F); do
      echo " - $Year"
      sbatch 01a_SubmitterATOS_AccTP_SA.sh $Year $Acc $NumSA $Dataset_SystemFC $Git_Repo $DirIN $DirOUT
done