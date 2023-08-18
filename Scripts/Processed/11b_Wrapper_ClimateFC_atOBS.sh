#!/bin/bash

# HRES_46r1
sbatch 11a_SubmitATOS_ClimateFC_atOBS.sh 2019 2020 "HRES_46r1"

# Reforecasts_46r1
sbatch 11a_SubmitATOS_ClimateFC_atOBS.sh 1999 2019 "Reforecasts_46r1"

# The rest of the datasets
for SystemFC_list in "ERA5_ShortRange" "ERA5_EDA_ShortRange" "ERA5_LongRange" "ERA5_EDA_LongRange" "ERA5_ecPoint/Grid_BC_VALS" "ERA5_ecPoint/Pt_BC_PERC"; do
      sbatch 11a_SubmitATOS_ClimateFC_atOBS.sh 2000 2019 ${SystemFC_list}
done