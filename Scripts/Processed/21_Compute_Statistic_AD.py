import os
import numpy as np
from scipy.stats import anderson_ksamp, PermutationMethod

###################################################################################################
# CODE DESCRIPTION
# 21_Compute_Statistic_AD.py computes the Anderson-Darling statistic between the observational and the NWP
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
# Code runtime: from 5 minutes in serial without permutations to 2 hours with 100 permutations.

# DESCRIPTION OF INPUT PARAMETERS
# YearS (number, in YYYY format): start year to consider.
# YearF (number, in YYYY format): final year to consider.
# Acc (number, in hours): rainfall accumulation period.
# MinDays_Perc (float, from 0 to 1): % of min n. of days with valid obs at each location.
# NumPer (integer): number of permutations for the Anderson-Darling test statistic.
# SystemNWP_list (list of string): list of NWP model climatologies.
# Git_Repo (string): path of local github repository.
# DirIN_OBS (string): relative path for the directory containing the rainfall observational.
# DirIN_NWP (string): relative path for the directory containing the NWP modelled rainfall realizations.
# DirOUT (string): relative path for the directory containing the AD statistic.

# INPUT PARAMETERS
YearS = 2000
YearF = 2019
Acc = 24
MinDays_Perc = 0.75
NumPer = 0
SystemNWP_list = ["Reanalysis/ERA5_ecPoint", "Reanalysis/ERA5_EDA", "Reanalysis/ERA5", "Reforecasts/ECMWF_46r1"]
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_ClimateNWP_4Points"
DirIN_OBS = "Data/Compute/10_AlignOBS_CleanSTVL/Coeff_Grid2Point_20"
DirIN_NWP = "Data/Compute/19_Merged_tp_NWP"
DirOUT = "Data/Compute/21_Statistic_AD"
###################################################################################################


# Reading the observational climatology
print()
print("Reading the realizations from rainfall observations...")
MainDirIN_OBS = Git_Repo + "/" + DirIN_OBS + "/" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF)
tp_obs = np.load(MainDirIN_OBS + "/obs.npy")
lats_obs = np.load(MainDirIN_OBS + "/stn_lats.npy")
lons_obs = np.load(MainDirIN_OBS + "/stn_lons.npy")
num_stn = tp_obs.shape[0]

# Selecting the stations with the required minimum number of days with valid observations
print("Selecting the stations with the considered minimum number of days with valid observations...")
MinNumDays = round(tp_obs.shape[1] * MinDays_Perc)
NumDays_NotNaN = np.sum(~np.isnan(tp_obs), axis=1) # array containing the n. of days with observations for each rain gauge
ind_stns_MinNumDays = np.where(NumDays_NotNaN >= MinNumDays)[0]
tp_obs_MinNumDays = tp_obs[ind_stns_MinNumDays]
lats_obs_MinNumDays = lats_obs[ind_stns_MinNumDays]
lons_obs_MinNumDays = lons_obs[ind_stns_MinNumDays]
num_stn_MinNumDays = tp_obs_MinNumDays.shape[0]
print(" - Total number of days between " + str(YearS) + " and " + str(YearF) + ": " + str(tp_obs.shape[1]))
print(" - Totals number of stations with at least " + str(int(MinDays_Perc*100)) + "% of days (= " + str(int(MinNumDays)) + ") with valid observations: " + str(num_stn_MinNumDays) + "/" + str(num_stn))

# Computing the Anderson-Darling test for k-samples for the different NWP models
print()
print("Computing the Anderson-Darling test for k-samples for the different NWP models")
for SystemNWP in SystemNWP_list:

      # Reading the NWP modelled rainfall realizations
      print()
      print(" - Reading the NWP modelled rainfall realizations from " + SystemNWP + "...")
      FileIN = Git_Repo + "/" + DirIN_NWP + "/MinDays_Perc_" + str(MinDays_Perc*100) + "/" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF) + "/" +  SystemNWP + "/tp.npy"
      tp_nwp = np.load(FileIN)

      # Initialazing the output variables
      StatisticAD = np.empty([num_stn,1]) * np.nan
      CriticalVal = np.empty([num_stn,1]) * np.nan
      Pvalue = np.empty([num_stn,1]) * np.nan
      
      for ind_stn in range(num_stn_MinNumDays):
            
            print(" - Running the Anderson-Darling test for k-samples for " + SystemNWP + " and the rain gauge station n. " + str(ind_stn) + "/" + str(num_stn_MinNumDays))

            # Reading the rainfall realizations (from observations and NWP) for a single rain gauge station
            tp_obs_temp = tp_obs_MinNumDays[ind_stn,:]
            tp_obs_nonan_temp = tp_obs_temp[~np.isnan(tp_obs_temp)] # eliminate all nan values from the calculation of the ECDF
            tp_nwp_temp = tp_nwp[ind_stn,:]

            # Sampling the rainfall realizations from observations and NWP models
            # NOTE: this is done to avoid that different size datasets might influence negatively the results of the study
            perc_obs = np.percentile(tp_obs_nonan_temp, np.arange(1,100))
            perc_nwp = np.percentile(tp_nwp_temp, np.arange(1,100))

            # Running the Anderson-Darling test for k-samples
            if np.sum(perc_obs) != 0 and np.sum(perc_nwp) != 0: # the A-D test need arrays with at least one value different from zero

                  if NumPer == 0:
                        TestAD = anderson_ksamp([perc_obs, perc_nwp])
                  else:
                        TestAD = anderson_ksamp([perc_obs, perc_nwp], method=PermutationMethod(n_resamples=NumPer))
                  StatisticAD[ind_stn] = TestAD[0]
                  CriticalVal[ind_stn] = TestAD[1][-1] # critical values for significance levels at the 0.1% (= 0.001)
                  Pvalue[ind_stn] = TestAD[2]

      # Saving the outcomes Anderson-Darling test
      print()
      print(" - Saving the outcomes of the Anderson-Darling test...")
      MainDirOUT = Git_Repo + "/" + DirOUT + "/MinDays_Perc_" + str(MinDays_Perc*100) + "/" + "NumPer_" + f'{NumPer:03d}' + "/" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF) + "/" + SystemNWP
      if not os.path.exists(MainDirOUT):
            os.makedirs(MainDirOUT)
      np.save(MainDirOUT + "/StatisticAD.npy", StatisticAD)
      np.save(MainDirOUT + "/CriticalVal.npy", CriticalVal)
      np.save(MainDirOUT + "/Pvalue.npy", Pvalue)
      np.save(MainDirOUT + "/Stn_lats.npy", lats_obs_MinNumDays)      
      np.save(MainDirOUT + "/Stn_lons.npy", lons_obs_MinNumDays)