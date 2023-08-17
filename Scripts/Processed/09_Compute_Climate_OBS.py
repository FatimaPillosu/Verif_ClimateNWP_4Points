import os
from os.path import exists
from datetime import datetime
import numpy as np

##########################################################################################################################################################
# CODE DESCRIPTION
# 09_Compute_Climate_OBS.py computes rainfall climatologies from point observations.

# DESCRIPTION OF INPUT PARAMETERS
# YearS (number, in YYYY format): start year to consider.
# YearF (number, in YYYY format): final year to consider.
# Acc (number, in hours): rainfall accumulation period.
# NameOBS_list (list of strings): list of the names of the observations to quality check
# Coeff_Grid2Point_list (list of integer number): list of coefficients used to make comparable CPC's gridded rainfall values with  STVL's point rainfall observations. 
#                                                                                    Used only when running the quality check on the clean STVL observations.
# MinDays_Perc_list (list of number, from 0 to 1): list of percentages for the minimum number of days over the considered period with valid observations to compute the climatologies.
# Perc_year (array of float numbers): percentiles to compute for the year climatology.
# Perc_season (array of float numbers): percentiles to compute for the seasonal climatologies.
# Git_repo (string): path of local github repository.
# DirIN (string): relative path for the input directory.
# DirOUT (string): relative path for the output directory.

# INPUT PARAMETERS
YearS = 2000
YearF = 2019
Acc = 24
NameOBS_list = ["06_AlignOBS_Combine-Years-RawSTVL", "07_AlignOBS_Extract-GridCPC", "08_AlignOBS-CleanSTVL"]
Coeff_Grid2Point_list = [2,5,10,20,50,100]
MinDays_Perc_list = [0.5, 0.75]
Perc_year = np.concatenate([np.arange(0,100), np.array([99.5, 99.8, 99.9, 99.95])], axis=0)
Perc_season = np.concatenate([np.arange(0,100), np.array([99.5, 99.8])], axis=0)
Git_repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/ecPoint_Climate"
DirIN = "Data/Compute"
DirOUT = "Data/Compute/09_Climate_OBS"
##########################################################################################################################################################

np.set_printoptions(threshold = np.inf, suppress=True, formatter={'float_kind':'{:0.2f}'.format})

# Costum functions

def compute_climate_obs(MinDays_Perc, Perc_year, Perc_season, DirIN, DirOUT):

      # Reading the rainfall observations over the period of interest and the correspondent metadata (i.e., ids/lats/lons/dates)
      print(" ")
      print(" - Reading the rainfall observations over the period of interest and the correspondent metadata (i.e., ids/lats/lons/dates)")
      stnids = np.load(DirIN + "/stn_ids.npy")
      lats = np.load(DirIN + "/stn_lats.npy")
      lons = np.load(DirIN + "/stn_lons.npy")
      dates = np.load(DirIN + "/dates.npy")
      obs = np.load(DirIN + "/obs.npy")
      
      # Computing the climatologies
      ClimateType_list = ["Year", "DJF", "MAM", "JJA", "SON"]
      for ClimateType in ClimateType_list:

            # Selecting the year or the seasonal subset with the observational dataset
            print(" ")
            print("     - Selecting the " + ClimateType + "  subset with the observational dataset")
            if ClimateType == "Year":
                  obs_temp = obs
                  percs = Perc_year
                  NamePercs = "Percentiles_Year"
            else:
                  if ClimateType == "DJF":
                        M1 = 12; M2 = 1; M3 = 2
                  if ClimateType == "MAM":
                        M1 = 3; M2 = 4; M3 = 5
                  if ClimateType == "JJA":
                        M1 = 6; M2 = 7; M3 = 8
                  if ClimateType == "SON":
                        M1 = 9; M2 = 10; M3 = 11
                  ind_dates_season = []
                  for ind_dates in range(obs.shape[1]):
                        month = (datetime.strptime(dates[ind_dates], "%Y%m%d")).month
                        if (month == M1) or (month == M2) or (month == M3):
                              ind_dates_season.append(ind_dates)
                  obs_temp = obs[:,ind_dates_season]
                  percs = Perc_season
                  NamePercs = "Percentiles_Season"
            
            # Selecting the stations with the considered minimum number of days with valid observations
            print("     - Selecting the stations with the considered minimum number of days with valid observations")
            MinNumDays = round(obs_temp.shape[1] * MinDays_Perc)
            NumDays_NotNaN = np.sum(~np.isnan(obs_temp), axis=1) # array containing the n. of days with observations for each rain gauge
            ind_stns_MinNumDays = np.where(NumDays_NotNaN >= MinNumDays)[0]
            obs_temp_MinNumDays = obs_temp[ind_stns_MinNumDays,:] # array containin only the stations that satisfied the minimum n. of days with observationss
            lats_MinNumDays = lats[ind_stns_MinNumDays]
            lons_MinNumDays = lons[ind_stns_MinNumDays]
            stnids_MinNumDays = stnids[ind_stns_MinNumDays]

            # Adjusting the dataset to not have the minimum and the maximum values assigned to the 0th and 100th percentile
            print("     - Adjusting the dataset to not have the minimum and the maximum values in the observational dataset assigned to the 0th and 100th percentile...")
            min_obs = np.nanmin(obs_temp_MinNumDays, axis=1)
            max_obs = np.nanmax(obs_temp_MinNumDays, axis=1)
            obs_temp_MinNumDays_new = np.column_stack((min_obs, obs_temp_MinNumDays, max_obs))

            # Computing and saving the climatologies and their metadata
            print("     - Computing and saving the climatologies and their metadata")
            climate = np.transpose(np.round(np.float32(np.nanpercentile(obs_temp_MinNumDays_new, percs, axis=1, interpolation="linear").astype(float)), decimals=1))
            np.save(DirOUT + "/" + NamePercs + ".npy", percs)
            np.save(DirOUT + "/Climate_" + ClimateType + ".npy", climate)
            np.save(DirOUT + "/" + "Stn_ids.npy", stnids_MinNumDays)
            np.save(DirOUT + "/" + "Stn_lats.npy", lats_MinNumDays)
            np.save(DirOUT + "/" + "Stn_lons.npy", lons_MinNumDays)
###############################################################################################################

# Computing the observational climatologies

for MinDays_Perc in MinDays_Perc_list:

      for NameOBS in NameOBS_list:

            if (NameOBS == "06_AlignOBS_Combine-Years-RawSTVL") or (NameOBS == "07_AlignOBS_Extract-GridCPC"):
                  
                  print(" ")
                  print("Computing the observational climatologies for "+ NameOBS + " with a minimum of " + str(int(MinDays_Perc*100)) + "% of days over the considered period with valid observations to compute the climatologies")
                  
                  # Setting main input/output directories
                  MainDirIN = Git_repo + "/" + DirIN + "/" + NameOBS
                  MainDirOUT = Git_repo + "/" + DirOUT + "/MinDays_Perc" + str(int(MinDays_Perc*100)) + "/" + NameOBS
                  if not exists(MainDirOUT):
                        os.makedirs(MainDirOUT)
                  
                  # Computing the observational climatologies
                  compute_climate_obs(MinDays_Perc, Perc_year, Perc_season, MainDirIN, MainDirOUT)

            elif NameOBS == "08_AlignOBS-CleanSTVL":

                  for Coeff_Grid2Point in Coeff_Grid2Point_list:
                        
                        print(" ")
                        print("Computing the observational climatologies for "+ NameOBS + " (Coeff_Grid2Point=" + str(Coeff_Grid2Point) + ") with a minimum of " + str(int(MinDays_Perc*100)) + "% of days over the considered period with valid observations to compute the climatologies")
                        
                        # Setting main input/output directories
                        MainDirIN = Git_repo + "/" + DirIN + "/" + NameOBS + "/Coeff_Grid2Point_" + str(Coeff_Grid2Point)
                        MainDirOUT = Git_repo + "/" + DirOUT + "/MinDays_Perc" + str(int(MinDays_Perc*100)) + "/" + NameOBS + "/Coeff_Grid2Point_" + str(Coeff_Grid2Point)
                        if not exists(MainDirOUT):
                              os.makedirs(MainDirOUT)

                        # Computing the observational climatologies
                        compute_climate_obs(MinDays_Perc, Perc_year, Perc_season, MainDirIN, MainDirOUT)