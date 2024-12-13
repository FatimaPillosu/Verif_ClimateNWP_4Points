import os
from os.path import exists
import numpy as np

###########################################################################
# CODE DESCRIPTION
# 12_Compute_Climate_OBS.py computes rainfall climatologies from point observations.
# Code runtime: ~ 3 minutes.

# DESCRIPTION OF INPUT PARAMETERS
# YearS (integer, in YYYY format): start year to consider.
# YearF (integer, in YYYY format): final year to consider.
# Acc (integer, in hours): rainfall accumulation period.
# RP_list (list of integers, in years): list of return periods to compute.
# Coeff_Grid2Point_list (list of integers): list of coefficients that make the CPC's gridded rainfall values comparable with STVL's point rainfall observations.
# MinDays_Perc_list (list of floats, from 0 to 1): percentage of min n. of days with valid obs at each location.
# NameOBS_list (list of strings): list of the observational datasets to quality check.
# Git_Repo (string): path of local GitHub repository.
# DirIN (string): relative path for the input directory.
# DirOUT (string): relative path for the output directory.

# INPUT PARAMETERS
YearS = 2000
YearF = 2019
Acc = 24
RP_list = [1, 2, 5, 10, 20]
Coeff_Grid2Point_list = [2, 5, 10, 20, 50, 100, 200, 500, 1000]
MinDays_Perc_list = [0.5, 0.75]
NameOBS_list = ["08_AlignOBS_Combine_Years_RawSTVL", "10_AlignOBS_CleanSTVL"]
Git_Repo = "/ec/vol/ecpoint_dev/mofp/papers_2_write/Verif_ClimateNWP_4Points"
DirIN = "Data/Compute"
DirOUT = "Data/Compute/12_Climate_OBS"
###########################################################################


# COMPUTE THE CLIMATOLOGY FROM OBSERVATIONS
def compute_climate_obs(MinDays_Perc, RP_list, DirIN, DirOUT):

      # Reading the rainfall observations and their metadata (i.e., ids/lats/lons/dates)
      print(" ")
      print("Reading the rainfall observations and their metadata (i.e., ids/lats/lons/dates)")
      stnids = np.load(DirIN + "/stn_ids.npy")
      lats = np.load(DirIN + "/stn_lats.npy")
      lons = np.load(DirIN + "/stn_lons.npy")
      dates = np.load(DirIN + "/dates.npy")
      obs = np.load(DirIN + "/obs.npy")

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
      obs_MinNumDays = np.column_stack((min_obs, obs_MinNumDays, max_obs))

      # Computing and saving the climatologies and their metadata
      print(" ")
      print("Computing the rainfall climatology")
      climate = np.transpose(np.round(np.float32(np.nanpercentile(obs_MinNumDays, Perc_2_Comp, axis=1, method="linear").astype(float)), decimals=1))

      # Saving the climatology and its metadata
      print(" ")
      print("Saving the climatology and its metadata")
      if not exists(DirOUT):
            os.makedirs(DirOUT)
      np.save(DirOUT + "/Climate.npy", climate)
      np.save(DirOUT + "/" + "Stn_lats.npy", lats_MinNumDays)
      np.save(DirOUT + "/" + "Stn_lons.npy", lons_MinNumDays)
      np.save(DirOUT + "/" + "Stn_ids.npy", stnids_MinNumDays)
      np.save(DirOUT + "/" + "Stn_dates.npy", dates)
      np.save(DirOUT + "/" + "Perc.npy", Perc_2_Comp)
      np.save(DirOUT + "/" + "RP.npy", RP_2_Comp)

###########################################################################


# Compute the climatologies for a different number of minimum days with valid observations 
for MinDays_Perc in MinDays_Perc_list:

      # Compute the climatologies from raw or clean point observations
      for NameOBS in NameOBS_list:

            if NameOBS == "08_AlignOBS_Combine_Years_RawSTVL": # raw

                  MainDirIN = Git_Repo + "/" + DirIN + "/" + NameOBS + "/" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF)
                  MainDirOUT = Git_Repo + "/" + DirOUT + "/" + NameOBS + "/MinDays_Perc_" + str(MinDays_Perc*100) + "/" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF)
                  compute_climate_obs(MinDays_Perc, RP_list, MainDirIN, MainDirOUT)
            
            if NameOBS == "10_AlignOBS_CleanSTVL": # clean
                  
                  for Coeff_Grid2Point in Coeff_Grid2Point_list:
                        
                        MainDirIN = Git_Repo + "/" + DirIN + "/" + NameOBS + "/Coeff_Grid2Point_" + str(Coeff_Grid2Point) + "/" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF)
                        MainDirOUT = Git_Repo + "/" + DirOUT + "/" + NameOBS + "/Coeff_Grid2Point_" + str(Coeff_Grid2Point) + "/MinDays_Perc_" + str(MinDays_Perc*100)  + "/" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF)
                        compute_climate_obs(MinDays_Perc, RP_list, MainDirIN, MainDirOUT)