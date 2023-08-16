import os
from os.path import exists
from datetime import date
import numpy as np
import pandas as pd

####################################################################################################################
# CODE DESCRIPTION
# 06_Compute_AlignOBS_Combine-Years-RawSTVL-RawSTVL.py combines the raw aligned stvl observations for all the years in the period of 
# interest.
# Code runtime: negligible.

# DESCRIPTION OF INPUT PARAMETERS
# YearS (number, in YYYY format): start year to consider.
# YearF (number, in YYYY format): final year to consider.
# Acc (number, in hours): rainfall accumulation period.
# Git_repo (string): path of local github repository.
# DirIN_UniqueStnids (string): relative path for the input directory containing the ids/lats/lons of the unique station over the period of interest.
# DirIN_AlignOBS_Year (string): relative path for the input directory containing the aligned rainfall observations on a given year.
# DirOUT (string): relative path for the output directory that will contain the aligned observations for the whole period of interest.

# INPUT PARAMETERS
YearS = 2000
YearF = 2019
Acc = 24
Git_repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/ecPoint_Climate"
DirIN_UniqueStnids = "Data/Compute/04_UniqueStnids_Combine-Years-RawSTVL"
DirIN_AlignOBS_Year = "Data/Compute/05_AlignOBS_Extract-PerYear-RawSTVL"
DirOUT = "Data/Compute/06_AlignOBS_Combine-Years-RawSTVL-RawSTVL"
####################################################################################################################

# Setting main input/output directory
MainDirIN_UniqueStnids = Git_repo + "/" + DirIN_UniqueStnids
MainDirIN_AlignOBS_Year = Git_repo + "/" + DirIN_AlignOBS_Year
MainDirOUT = Git_repo + "/" + DirOUT
if not exists(MainDirOUT):
      os.makedirs(MainDirOUT)

# Reading the ids/lats/lons for the unqiue stations over the period of interest
stnids_unique = np.load(MainDirIN_UniqueStnids+ "/stnids_unique.npy")
lats_unique = np.load(MainDirIN_UniqueStnids+ "/lats_unique.npy")
lons_unique = np.load(MainDirIN_UniqueStnids+ "/lons_unique.npy")
NumStns_period = len(stnids_unique)

# Defining the list of dates over the considered period
DateS = date(YearS,1,1)
DateF = date(YearF,12,31)
Dates_range = np.array((pd.date_range(DateS.strftime("%Y%m%d"), DateF.strftime("%Y%m%d")).strftime('%Y%m%d')).tolist())
NumDays_period = len(Dates_range)

# Merging the aligned observations for each year over the period of interest
print(" ")
print("Merging aligned observations over the period of interest for year ...")
print(" - " + str(YearS))
FileIN_temp = MainDirIN_AlignOBS_Year + "/" + str(YearS) + ".npy"
align_obs = np.load(FileIN_temp)
for Year in range(YearS+1,YearF+1):
      print(" - " + str(Year))
      FileIN_temp = MainDirIN_AlignOBS_Year + "/" + str(Year) + ".npy"
      align_obs = np.concatenate((align_obs, np.load(FileIN_temp)), axis=1)
NumStns = align_obs.shape[0]
NumDays = align_obs.shape[1]

# Checking that the shape of the final matrix contains the expected number of unique stations and days over the considered period
print(" ")
if (NumStns == NumStns_period) and (NumDays == NumDays_period):
      print("Considering " + str(NumStns) + " rainfall stations each day over the period of interest.")
      print("There are " + str(NumDays) + " days over the period of interest.")
elif (NumStns != NumStns_period):
      print("ERROR! The number of the unique stations over the considered period does not match the number of the stations in the single imported files.")
      exit()
elif (NumDays != NumDays_period):
      print("ERROR! The number of days over the considered period does not match the number of the days in the single imported files.")
      exit()

# Saving the aligned observations over the whole considered period
print(" ")
print("Saving the aligned observations for the whole considered period")
np.save(MainDirOUT + "/stn_ids.npy", stnids_unique)
np.save(MainDirOUT + "/stn_lats.npy", lats_unique)
np.save(MainDirOUT + "/stn_lons.npy", lons_unique)
np.save(MainDirOUT + "/dates.npy", Dates_range)
np.save(MainDirOUT + "/stvl_obs.npy", align_obs)