import os
from os.path import exists
from datetime import date, timedelta
import numpy as np
import pandas as pd
import metview as mv

#####################################################################################################################
# CODE DESCRIPTION
# 07_Compute_AlignOBS_Extract_PerYear_RawSTVL.py aligns the observation stations to have the same number of stations per day over a year.
# Code Runtime: ~ 2 hours.

# DESCRIPTION OF INPUT PARAMETERS
# YearS (integer, in YYYY format): start year to consider.
# YearF (integer, in YYYY format): final year to consider.
# Acc (integer, in hours): rainfall accumulation period.
# Git_Repo (string): path of local GitHub repository.
# DirIN_UniqueOBS (string): relative path for the input directory containing the rainfall observations of interest.
# DirIN_UniqueStnids (string): relative path for the input directory containing the ids/lats/lons of the unique station over the period of interest.
# DirOUT (string): relative path for the output directory that will contain the aligned observations for the given year.

# INPUT PARAMETERS
YearS = 2000
YearF = 2019
Acc = 24
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_ClimateNWP_4Points"
DirIN_UniqueOBS = "Data/Compute/02_UniqueOBS_Combine_Datasets_Times_PerDay_RawSTVL"
DirIN_UniqueStnids = "Data/Compute/06_UniqueStnids_Combine_Years_RawSTVL"
DirOUT = "Data/Compute/07_AlignOBS_Extract_PerYear_RawSTVL"
#####################################################################################################################


# Setting main input/output directories
MainDirIN_UniqueOBS = Git_Repo + "/" + DirIN_UniqueOBS + "/" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF) + "/" + str(Year)
MainDirIN_UniqueStnids = Git_Repo + "/" + DirIN_UniqueStnids  + "/" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF) + "/" + str(Year)
MainDirOUT = Git_Repo + "/" + DirOUT + "/" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF) + "/" + str(Year)
if not exists(MainDirOUT):
      os.makedirs(MainDirOUT)

# Reading the ids/lats/lons for the unique stations over the period of interest
stnids_unique = np.load(MainDirIN_UniqueStnids+ "/stnids_unique.npy")
lats_unique = np.load(MainDirIN_UniqueStnids+ "/lats_unique.npy")
lons_unique = np.load(MainDirIN_UniqueStnids+ "/lons_unique.npy")
NumStns = len(stnids_unique)

# Splitting the computations in years due to memory issues
for Year in range(YearS, YearF+1):

      # Define the list of dates over the considered year
      DateS = date(Year,1,1)
      DateF = date(Year,12,31)
      Dates_range = np.array((pd.date_range(DateS.strftime("%Y%m%d"), DateF.strftime("%Y%m%d")).strftime('%Y%m%d')).tolist())
      NumDays = len(Dates_range) 

      # Aligning the observations for the considered year
      print("Aligning the observations for:")
      aligned_obs = np.empty((NumStns,NumDays,)) * np.nan # initialize the variable that will contain the aligned observations with NaNs, so there won't be any need to deal with stations with no observations on a given day
      TheDate = DateS
      while TheDate <= DateF:
            
            TheDateSTR  = TheDate.strftime("%Y%m%d")
            TheYearSTR = TheDate.strftime("%Y")
            ind_dates = np.where(Dates_range == TheDateSTR)[0][0]
            print(" - " + TheDateSTR)

            # Reading the rainfall observations as geopoints 
            FileIN_temp = MainDirIN_UniqueOBS + "/" + TheYearSTR + "/tp" + str(Acc) + "_obs_" + TheDateSTR + ".geo"
            geo = mv.read(FileIN_temp)
            geo_stnids = np.array(mv.stnids(geo))
            geo_obs = mv.values(geo)
            m = len(geo_stnids)
            
            # Assigning observations to the correspondent unique stations and dates
            for i in range(m):
                  stnids_temp = geo_stnids[i]
                  obs_temp = geo_obs[i]
                  ind_stnids = np.where(stnids_unique == stnids_temp)[0][0]
                  aligned_obs[ind_stnids,ind_dates] = obs_temp

            TheDate += timedelta(days=1)

      # Saving the aligned rainfall observations for the given year as a 2-d numpy array
      FileOUT = MainDirOUT + "/" + str(Year) + ".npy"
      np.save(FileOUT,aligned_obs)