import os
from os.path import exists
import numpy as np

###########################################################################
# CODE DESCRIPTION
# 12_Compute_Climate_OBS.py computes rainfall climatologies from point observations.
# Code runtime: ~ 5 minutes.

# DESCRIPTION OF INPUT PARAMETERS
# YearS (integer, in YYYY format): start year to consider.
# YearF (integer, in YYYY format): final year to consider.
# Acc (integer, in hours): rainfall accumulation period.
# MinDays_Perc (float, from 0 to 1): % of min n. of days with valid obs at each location.
# RP_list (list of integers, in years): list of return periods to compute.
# Git_Repo (string): path of local GitHub repository.
# DirIN (string): relative path for the input directory.
# DirOUT (string): relative path for the output directory.

# INPUT PARAMETERS
YearS = 2000
YearF = 2019
Acc = 24
MinDays_Perc = 0.75
RP_list = [1, 2, 5, 10, 20]
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_ClimateNWP_4Points"
DirIN = "Data/Compute/10_AlignOBS_CleanSTVL/Coeff_Grid2Point_20"
DirOUT = "Data/Compute/12_Climate_OBS/Coeff_Grid2Point_20"
###########################################################################


# Reading the rainfall observations and their metadata (i.e., ids/lats/lons/dates)
print(" ")
print("Reading the rainfall observations and their metadata (i.e., ids/lats/lons/dates)")
MainDirIN = Git_Repo + "/" + DirIN  + "/" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF)
stnids = np.load(MainDirIN + "/stn_ids.npy")
lats = np.load(MainDirIN + "/stn_lats.npy")
lons = np.load(MainDirIN + "/stn_lons.npy")
dates = np.load(MainDirIN + "/dates.npy")
obs = np.load(MainDirIN + "/obs.npy")

# Selecting the stations with the required minimum number of days with valid observations
print(" ")
print("Selecting the stations with the considered minimum number of days with valid observations")
MinNumDays = round(obs.shape[1] * MinDays_Perc)
NumDays_NotNaN = np.sum(~np.isnan(obs), axis=1) # array containing the n. of days with observations for each rain gauge
ind_stns_MinNumDays = np.where(NumDays_NotNaN >= MinNumDays)[0]
obs_MinNumDays = obs[ind_stns_MinNumDays,:] # array containin only the stations that satisfied the minimum n. of days with observationss
lats_MinNumDays = lats[ind_stns_MinNumDays]
lons_MinNumDays = lons[ind_stns_MinNumDays]
stnids_MinNumDays = stnids[ind_stns_MinNumDays]
print(" - Total number of days between " + str(YearS) + " and " + str(YearF) + ": " + str(obs.shape[1]))
print(" - Totals number of stations with at least " + str(int(MinDays_Perc*100)) + "% of days (= " + str(int(MinNumDays)) + ") with valid observations: " + str(len(ind_stns_MinNumDays)) + "/" + str(str(obs.shape[0])))

# Defining the return periods that can be computed given the number of realizations available
RP_list = np.array(RP_list)
Min_Num_Realizations_RP = 365 * np.array(RP_list)
Min_Num_Realizations = MinNumDays * (24/Acc)
ind_RP = np.where(Min_Num_Realizations_RP < Min_Num_Realizations)[0]
RP_list = RP_list[ind_RP]
Perc_2_Comp = 100 - ( (1/(RP_list * 365) ) * 100)
Perc_2_Comp = np.concatenate((np.arange(0,100), Perc_2_Comp))
RP_2_Comp = 100 / ( 365 * (100 - Perc_2_Comp) )

# Adjusting the dataset to not have the minimum and the maximum values assigned to the 0th and 100th percentile
# This is done to ensure the minimum and the maximum rainfall totals are used in the computations of the percentiles greater than 0 and smaller than 100th. 
# For example, in the case of the maximum value in the dataset, if this trick is not applied, the code might interpreted as the maximum rainfall
# total that is possible (but that is not known) and it will be not considered for the computation of smaller percentiles such as 99.8th, 99.9th, etc. 
print(" ")
print("Adjusting the dataset to not have the minimum and the maximum values in the observational dataset assigned to the 0th and 100th percentile...")
min_obs = np.nanmin(obs_MinNumDays, axis=1)
max_obs = np.nanmax(obs_MinNumDays, axis=1)
obs_MinNumDays_new = np.column_stack((min_obs, obs_MinNumDays, max_obs))

# Computing and saving the climatologies and their metadata
print(" ")
print("Computing the rainfall climatology")
climate = np.transpose(np.round(np.float32(np.nanpercentile(obs_MinNumDays_new, Perc_2_Comp, axis=1, method="linear").astype(float)), decimals=1))

# Saving the climatology and its metadata
print(" ")
print("Saving the climatology and its metadata")
MainDirOUT = Git_Repo + "/" + DirOUT + "/MinDays_Perc_" + str(MinDays_Perc*100) + "/" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF)
if not exists(MainDirOUT):
      os.makedirs(MainDirOUT)
np.save(MainDirOUT + "/Climate.npy", climate)
np.save(MainDirOUT + "/" + "Stn_lats.npy", lats_MinNumDays)
np.save(MainDirOUT + "/" + "Stn_lons.npy", lons_MinNumDays)
np.save(MainDirOUT + "/" + "Perc.npy", Perc_2_Comp)
np.save(MainDirOUT + "/" + "RP.npy", RP_2_Comp)