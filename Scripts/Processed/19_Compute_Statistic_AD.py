import os
from datetime import datetime, timedelta
import numpy as np
from scipy.stats import anderson_ksamp, PermutationMethod

###################################################################################################
# CODE DESCRIPTION
# 19_Compute_Statistic_AD.py computes the Anderson-Darling statistic between the observational and the NWP
# modelled climatology.
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
# MinDays_Perc (float, from 0 to 1): % of min n. of days with valid obs at each location.
# SystemNWP_list (list of string): list of NWP model climatologies.
# Git_Repo (string): path of local github repository.
# DirIN (string): relative path for the directory containing the rainfall realizations.
# DirOUT (string): relative path for the directory containing the AD statistic.

# INPUT PARAMETERS
YearS = 2000
YearF = 2019
Acc = 24
MinDays_Perc = 0.75
SystemNWP_list = ["Reanalysis/ERA5_EDA", "Reanalysis/ERA5", "Reforecasts/ECMWF_46r1", "Reanalysis/ERA5_ecPoint"]
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_ClimateNWP_4Points"
DirIN = "Data/Compute/18_Extract_RealizationsTP"
DirOUT = "Data/Compute/19_Statistic_AD"
###################################################################################################


# Reading the rainfall realizations from observations
print()
print("Reading the rainfall realizations from observations...")
DirIN_temp = Git_Repo + "/" + DirIN + "/MinDays_Perc_" + str(MinDays_Perc*100) + "/" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF) + "/OBS" 
tp_obs = np.load(DirIN_temp + "/vals_obs.npy")
lat_obs = np.load(DirIN_temp + "/lats_obs.npy")
lon_obs = np.load(DirIN_temp + "/lons_obs.npy")
num_stn = tp_obs.shape[0]

# Determining the range of dates to consider for the NWP models
BaseDateS = datetime(YearS-1, 1, 1) # to include the dates from the reforecasts
BaseDateF = datetime(YearF, 12, 31)

# Running  the Anderson-Darling statistic for rainfall realizations from different NWP models
for SystemNWP in SystemNWP_list:
      
      print()
      print("Reading the rainfall realizations from NWP models...")

      # Reading the rainfall realizations
      tp_nwp = None # initializing the variable that will contain the rainfall realizations for a specific NWP model, for the whole considered period
      BaseDate = BaseDateS
      while BaseDate <= BaseDateF:

            DirIN_temp = Git_Repo + "/" + DirIN + "/MinDays_Perc_" + str(MinDays_Perc*100) + "/" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF) + "/NWP/" + SystemNWP + "/" + BaseDate.strftime("%Y")
            FileIN_temp = "tp_" + BaseDate.strftime("%Y%m%d") + ".npy"
            if os.path.exists(DirIN_temp + "/" + FileIN_temp):
                  print(" - Reading the realizations for '" + SystemNWP + "', on " + BaseDate.strftime("%Y%m%d") + "...")
                  tp_nwp_temp = np.load(DirIN_temp + "/" + FileIN_temp)
                  if tp_nwp is None:
                        tp_nwp = tp_nwp_temp
                  else:
                        tp_nwp = np.vstack((tp_nwp, tp_nwp_temp))

            BaseDate = BaseDate + timedelta(days=1)
      
      tp_nwp = tp_nwp.T # to convert it with the same dimensions of the rainfall realizations from observations
      
      # Computing the Anderson-Darling test for k-samples
      print("Computing the Anderson-Darling test for k-samples between observations and " + SystemNWP + "...")
      StatisticAD = np.empty([num_stn,1]) * np.nan
      CriticalVal = np.empty([num_stn,1]) * np.nan
      Pvalue = np.empty([num_stn,1]) * np.nan
      for ind_stn in range(num_stn):
            TestAD = anderson_ksamp([tp_obs[ind_stn,:], tp_nwp[ind_stn,:]], method=PermutationMethod(n_resamples=100))
            StatisticAD[ind_stn] = TestAD[0]
            CriticalVal[ind_stn] = TestAD[1][-1] # critical values for significance levels at the 0.1% (= 0.001)
            Pvalue[ind_stn] = TestAD[2]

      # Saving the outcomes Anderson-Darling test
      print("Saving the outcomes of the Anderson-Darling test...")
      MainDirOUT = Git_Repo + "/" + DirOUT + "/MinDays_Perc_" + str(MinDays_Perc*100) + "/" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF) + "/" + SystemNWP
      if not os.path.exists(MainDirOUT):
            os.makedirs(MainDirOUT)
      np.save(MainDirOUT + "/StatisticAD.npy", StatisticAD)
      np.save(MainDirOUT + "/CriticalVal.npy", CriticalVal)
      np.save(MainDirOUT + "/Pvalue.npy", Pvalue)
      np.save(MainDirOUT + "/Stn_lats.npy", lat_obs)      
      np.save(MainDirOUT + "/Stn_lons.npy", lon_obs)