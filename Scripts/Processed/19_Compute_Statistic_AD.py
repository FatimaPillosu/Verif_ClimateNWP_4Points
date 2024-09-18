import os
import numpy as np
import metview as mv
from scipy.stats import anderson_ksamp

###################################################################################################
# CODE DESCRIPTION
# 03_Compute_Statistic_AD.py computes the Anderson-Darling statistic between the observational and the NWP
# modelled climatology distributions.
# Note:
# The Anderson-Darling test for k-samples tests the null hypothesis that k-samples are drawn from the same population 
# without having to specify the distribution function of that population. 
#     1. If the Anderson-Darling statistic is bigger than the critical values, this means that the test results are significant at 
#         every significance level. Therefore, we would reject the null hypothesis of the test no matter which significance 
#         level we choose to use. Thus, we have sufficient evidence to say that the samples are not drawn from the same
#         population.
#     2. If the Anderson-Darling statistic is smaller than the critical values, this means that the test results are not 
#         significant at any significance level. Therefore, we would not reject the null hypothesis of the test. Thus, we don’t 
#         have sufficient evidence to say that the samples are not drawn from the same population.
# Code runtime: ~ 1 minute.

# DESCRIPTION OF INPUT PARAMETERS
# YearS (number, in YYYY format): start year to consider.
# YearF (number, in YYYY format): final year to consider.
# Acc (number, in hours): rainfall accumulation period.
# SystemNWP_list (list of string): list of NWP model climatologies.
# Git_Repo (string): path of local github repository.
# DirIN_OBS (string): relative path for the directory containing the observational climatologies.
# DirIN_NWP (string): relative path for the directory containing the NWP modelled climatologies.
# DirOUT (string): relative path for the directory containing the AD statistic.

# INPUT PARAMETERS
YearS = 2000
YearF = 2019
Acc = 24
SystemNWP_list = ["Reforecasts/ECMWF_46r1", "Reanalysis/ERA5_EDA", "Reanalysis/ERA5", "Reanalysis/ERA5_ecPoint"]
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_ClimateNWP_4Points"
DirIN_OBS = "Data/Raw/Climate_OBS"
DirIN_NWP = "Data/Raw/Climate_NWP"
DirOUT = "Data/Compute/03_Statistic_AD"
###################################################################################################


# Reading the observational climatology
print()
print("Reading the observational climatology...")
MainDirIN_OBS = Git_Repo + "/" + DirIN_OBS + "/tp_" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF)
climate_OBS = np.load(MainDirIN_OBS + "/Climate.npy")
lats_OBS = np.load(MainDirIN_OBS + "/Stn_lats.npy")
lons_OBS = np.load(MainDirIN_OBS + "/Stn_lons.npy")
rp_OBS = np.load(MainDirIN_OBS + "/RP.npy")
rp_OBS = (np.round(rp_OBS, decimals = 5)).astype('float64')
num_stn = climate_OBS.shape[0]

# Computing the Anderson-Darling statistic for different NWP modelled climatologies
print()
print("Computing the Anderson-Darling statistic for the NWP modelled climatology: ")
for SystemNWP in SystemNWP_list:
      
      print(" - " + SystemNWP)

      # Reading the considered NWP modelled climatology
      MainDirIN_NWP = Git_Repo + "/" + DirIN_NWP + "/tp_" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF) + "/" + SystemNWP
      climate_NWP = mv.read(MainDirIN_NWP + "/Climate.grib")
      rp_NWP = np.load(MainDirIN_NWP + "/RP.npy")

      # Select the nearest grid-point to the rain gauge locations
      climate_NWP_OBS = mv.nearest_gridpoint(climate_NWP, lats_OBS, lons_OBS).T

      # Selecting the return-periods that were also computed for the observational climatologies
      ind_rp = np.isin(rp_NWP, rp_OBS)
      climate_NWP_OBS = climate_NWP_OBS[:, ind_rp]

      # Running the Anderson-Darling test for k-samples
      StatisticAD = np.empty([num_stn,1]) * np.nan
      CriticalVal = np.empty([num_stn,1]) * np.nan
      for ind_stn in range(num_stn):
            climate_OBS_temp = climate_OBS[ind_stn,:]
            climate_NWP_OBS_temp = climate_NWP_OBS[ind_stn,:]
            if np.sum(climate_OBS_temp) != np.sum(climate_NWP_OBS_temp): # to eliminate all those cases where the values are only zeros
                  TestAD = anderson_ksamp([climate_OBS_temp, climate_NWP_OBS_temp])
                  StatisticAD[ind_stn] = TestAD[0]
                  CriticalVal[ind_stn] = TestAD[1][-1] # at the 0.1% significance level

      # Saving the outcomes Anderson-Darling test
      MainDirOUT = Git_Repo + "/" + DirOUT + "/tp_" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF) + "/" + SystemNWP
      if not os.path.exists(MainDirOUT):
            os.makedirs(MainDirOUT)
      np.save(MainDirOUT + "/StatisticAD.npy", StatisticAD)
      np.save(MainDirOUT + "/CriticalVal.npy", CriticalVal)
      np.save(MainDirOUT + "/Stn_lats.npy", lats_OBS)      
      np.save(MainDirOUT + "/Stn_lons.npy", lons_OBS)