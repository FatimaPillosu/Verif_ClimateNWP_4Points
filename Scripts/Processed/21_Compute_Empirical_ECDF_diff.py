import os
import numpy as np

#########################################################################################################
# CODE DESCRIPTION
# 21_Compute_Empirical_ECDF_diff.py computes the difference between the ECDF's quantiles from the obs and nwp rainfall 
# distributions.
# Code runtime: up to 7 min when ~100 percentiles are considered, and up to 37 min when ~10000 percentiles are considered.

# DESCRIPTION OF INPUT PARAMETERS
# YearS (number, in YYYY format): start year to consider.
# YearF (number, in YYYY format): final year to consider.
# Acc (number, in hours): rainfall accumulation period.
# MinDays_Perc (float, from 0 to 1): % of min n. of days with valid obs at each location.
# Perc_list (float, from 0 to 100 - not included): list of percentiles to consider when sampling the obs and nwp rainfall realizations. 
# SystemNWP_list (list of string): list of NWP model climatologies.
# Git_Repo (string): path of local github repository.
# DirIN_OBS (string): relative path for the directory containing the rainfall observational.
# DirIN_NWP (string): relative path for the directory containing the NWP modelled rainfall realizations.
# DirOUT (string): relative path for the directory containing the quantile differences for the NWP modelled rainfall realizations.

# INPUT PARAMETERS
YearS = 2000
YearF = 2019
Acc = 24
MinDays_Perc = 0.75
Perc_list = np.arange(0, 99.98, 0.01)
SystemNWP_list = ["Reanalysis/ERA5_ecPoint", "Reanalysis/ERA5_EDA", "Reanalysis/ERA5", "Reforecasts/ECMWF_46r1"]
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_ClimateNWP_4Points"
DirIN_OBS = "Data/Compute/10_AlignOBS_CleanSTVL/Coeff_Grid2Point_20"
DirIN_NWP = "Data/Compute/19_Merged_tp_NWP"
DirOUT = "Data/Compute/21_Empirical_ECDF_diff"
#########################################################################################################


# Reading the obs rainfall realizations
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

# Computing the average obs rainfall per station
print("Computing the average obs rainfall per station...")
tp_obs_mean = np.nanmean(tp_obs_MinNumDays, axis = 1)

# Computing the ECDF (percentiles) for the obs rainfall realizations
print("Computing the ECDF (percentiles) for the obs rainfall realizations...")
perc_obs = np.nanpercentile(tp_obs_MinNumDays, Perc_list, axis=1).T

# Computing the difference between the ECDF's quantiles from the obs and nwp rainfall distributions
print()
print("Computing the difference between the ECDF's quantiles from the obs and nwp rainfall distributions")
for SystemNWP in SystemNWP_list:

      # Reading the NWP modelled rainfall realizations
      print()
      print("Reading the NWP modelled rainfall realizations from " + SystemNWP + "...")
      FileIN = Git_Repo + "/" + DirIN_NWP + "/MinDays_Perc_" + str(MinDays_Perc*100) + "/" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF) + "/" +  SystemNWP + "/tp.npy"
      tp_nwp = np.load(FileIN)

      # Computing the percentiles for the nwp rainfall realizations
      print("Computing the ECDF (percentiles) for the nwp rainfall realizations...")
      perc_nwp = np.nanpercentile(tp_nwp, Perc_list, axis=1).T

      # Determining the difference between the obs and nwp ECDFs
      print("Determining the difference between the obs and nwp ECDFs...")
      perc_diff = perc_obs - perc_nwp

      # Saving the difference between the obs and nwp ECDFsl and the average observed rainfall
      print("Saving the difference between the obs and nwp ECDFsl and the average observed rainfall...")
      MainDirOUT = Git_Repo + "/" + DirOUT + "/MinDays_Perc_" + str(MinDays_Perc*100) + "/MaxPerc_" + str(np.max(Perc_list)) + "/" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF) + "/" + SystemNWP
      if not os.path.exists(MainDirOUT):
            os.makedirs(MainDirOUT)
      np.save(MainDirOUT + "/tp_obs_mean.npy", tp_obs_mean)
      np.save(MainDirOUT + "/ECDF_Diff.npy", perc_diff)
      np.save(MainDirOUT + "/Perc_List.npy", Perc_list)
      np.save(MainDirOUT + "/Stn_lats.npy", lats_obs_MinNumDays)      
      np.save(MainDirOUT + "/Stn_lons.npy", lons_obs_MinNumDays)