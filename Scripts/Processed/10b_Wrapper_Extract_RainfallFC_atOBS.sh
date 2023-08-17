#!/bin/bash

# To extract the independent realizations from HRES
SystemFC_list="HRES_46r1"
for Year in 2019 2020; do
      sbatch 10a_SubmitATOS_Extract_RainfallFC_atOBS.sh ${Year} ${SystemFC_list}
done

# To extract the independent realizations from Reforecasts
SystemFC_list="Reforecasts_46r1"
for Year in {1999..2019}; do
      sbatch 10a_SubmitATOS_Extract_RainfallFC_atOBS.sh ${Year} ${SystemFC_list}
done

# To extract the independent realizations from all the other forecasting systems
SystemFC_list="ERA5_ShortRange,ERA5_EDA_ShortRange,ERA5_LongRange,ERA5_EDA_LongRange,ERA5_ecPoint/Grid_BC_VALS,ERA5_ecPoint/Pt_BC_PERC"
for Year in {2000..2019}; do
      sbatch 10a_SubmitATOS_Extract_RainfallFC_atOBS.sh ${Year} ${SystemFC_list}
done