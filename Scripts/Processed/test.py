import os
import numpy as np
import metview as mv
import matplotlib.pyplot as plt

###################################################################################################
# CODE DESCRIPTION
# 22_Plot_Empirical_Quantile_Analysis.py plots the outcomes of the empirical quantile analysis for all the considered
# nwp models.
# Code runtime: up to 1 minute.

# DESCRIPTION OF INPUT PARAMETERS
# YearS (number, in YYYY format): start year to consider.
# YearF (number, in YYYY format): final year to consider.
# Acc (number, in hours): rainfall accumulation period.
# MinDays_Perc (float, from 0 to 1): % of min n. of days with valid obs at each location.
# Num_Perc (integer): number of percentiles considered when sampling the obs and nwp rainfall realizations. 
# SystemNWP_list (list of string): list of NWP model climatologies.
# Git_Repo (string): path of local github repository.
# DirIN (string): relative path for the directory containing the values of the AD statistic.
# DirOUT (string): relative path for the directory containing the AD statistic.

# INPUT PARAMETERS
YearS = 2000
YearF = 2019
Acc = 24
MinDays_Perc = 0.75
NumPerc = 98
SystemNWP_list = ["Reanalysis/ERA5_EDA"]
#SystemNWP_list = ["Reanalysis/ERA5_ecPoint", "Reanalysis/ERA5_EDA", "Reanalysis/ERA5", "Reforecasts/ECMWF_46r1"]
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_ClimateNWP_4Points"
DirIN = "Data/Compute/21_Empirical_Quantile_Analysis"
DirOUT = "Data/Plot/22_Empirical_Quantile_Analysis"
###################################################################################################


# Plotting the outcomes of the empirical quantile analysis for the nwp models
print()
print("Plotting the outcomes of the empirical quantile analysis for the nwp models: ")
for SystemNWP in SystemNWP_list:
      
      print(" - " + SystemNWP)

      # Reading the quantile differences for a specific nwp model
      MainDirIN = Git_Repo + "/" + DirIN + "/MinDays_Perc_" + str(MinDays_Perc*100) + "/NumPerc_" + str(NumPerc) + "/" +f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF) + "/" + SystemNWP
      perc_diff = np.load(MainDirIN + "/Perc_Diff.npy")
      perc_list = np.arange(1, 99, 1)
      lats = np.load(MainDirIN + "/" + "Stn_lats.npy")
      lons = np.load(MainDirIN + "/" + "Stn_lons.npy")
      num_stn = perc_diff.shape[0]

      for ind_stn in range(num_stn):

            perc_diff_temp = perc_diff[ind_stn,:]
            plt.plot(perc_list, perc_diff_temp, ".")
            plt.show()
            exit()

