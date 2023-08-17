#!/bin/bash

for SystemFC_list in "HRES_46r1" "Reforecasts_46r1" "ERA5_ShortRange" "ERA5_EDA_ShortRange" "ERA5_LongRange" "ERA5_EDA_LongRange" "ERA5_ecPoint/Grid_BC_VALS" "ERA5_ecPoint/Pt_BC_PERC"; do
      sbatch 11a_SubmitATOS_ClimateFC_atOBS.sh ${SystemFC_list}
done