import os
from datetime import datetime, timedelta
import numpy as np

###################################################################################################
# CODE DESCRIPTION
# 19_Compute_Merged_tp_NWP.py combine the indipendent rainfall realizations from observations and NWP models for 
# the whole considered period.
# Code runtime: up to 15 minutes.

# DESCRIPTION OF INPUT PARAMETERS
# YearS (date, in YYYYMMDD format): start year to consider.
# YearF (date, in YYYY format): final year to consider.
# Acc (integer, in hours): rainfall accumulation period.
# MinDays_Perc (float, from 0 to 1): % of min n. of days with valid obs at each location.
# SystemNWP_list (list of string): list of considered NWP models.
# Git_Repo (string): path of local GitHub repository.
# DirIN_OBS (string): relative path for the directory containing the rainfall observations.
# DirIN_NWP (string): relative path for the directory containing the NWP modelled rainfall reanalysis/reforecasts.
# DirOUT (string): relative path for the directory containing the indipendent rainfall realizations.

# INPUT PARAMETERS
YearS = 2000
YearF = 2019
Acc = 24
MinDays_Perc = 0.75
SystemNWP_list = ["Reanalysis/ERA5_EDA", "Reanalysis/ERA5", "Reforecasts/ECMWF_46r1", "Reanalysis/ERA5_ecPoint"]
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_ClimateNWP_4Points"
DirIN = "Data/Compute/18_Extract_tp_NWP"
DirOUT = "Data/Compute/19_Merged_tp_NWP"
###################################################################################################


# Determining the range of dates to consider for the NWP models
BaseDateS = datetime(YearS-1, 1, 1) # to include the dates from the reforecasts
BaseDateF = datetime(YearF, 12, 31)

# Running  the Anderson-Darling statistic for rainfall realizations from different NWP models
for SystemNWP in SystemNWP_list:
      
      print()

      # Reading the rainfall realizations
      tp_nwp_list = [] # initializing the variable that will contain the rainfall realizations for a specific NWP model, for the whole considered period
      BaseDate = BaseDateS
      while BaseDate <= BaseDateF:

            DirIN_temp = Git_Repo + "/" + DirIN + "/MinDays_Perc_" + str(MinDays_Perc*100) + "/" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF) + "/" + SystemNWP + "/" + BaseDate.strftime("%Y")
            FileIN_temp = "tp_" + BaseDate.strftime("%Y%m%d") + ".npy"
            if os.path.exists(DirIN_temp + "/" + FileIN_temp):
                  print("Merge the realizations for '" + SystemNWP + "', on " + BaseDate.strftime("%Y%m%d") + "...")
                  tp_nwp_temp = np.load(DirIN_temp + "/" + FileIN_temp).astype(np.float16) # to reduce the needed memory
                  tp_nwp_list.append(tp_nwp_temp)

            BaseDate = BaseDate + timedelta(days=1)
      
      tp_nwp = np.vstack(tp_nwp_list).T # to have rain gauge stations as rows and tp realizations as columns 

      # Saving the extracted sub-areas
      DirOUT_temp = Git_Repo + "/" + DirOUT + "/MinDays_Perc_" + str(MinDays_Perc*100) + "/" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF) + "/" +  SystemNWP
      if not os.path.exists(DirOUT_temp):
            os.makedirs(DirOUT_temp)
      np.save(DirOUT_temp + "/tp.npy", tp_nwp) 