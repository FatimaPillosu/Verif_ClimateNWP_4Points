import sys
import os
from os.path import exists
from datetime import date, timedelta
import numpy as np
import metview as mv

#####################################################################
# CODE DESCRIPTION
# 03_Compute_UniqueStnids_Extract-List-PerYear.py extracts the list of unique stnids 
# in a given year.
# Code runtime: ~ 2 minutes. 
# The code is splitted in years not because of long runtimes but for memory issues.

# DESCRIPTION OF INPUT PARAMETERS
# Year (number, in YYYY format): year to consider.
# Acc (number, in hours): rainfall accumulation period.
# Git_repo (string): path of local github repository
# DirIN (string): relative path for the input directory
# DirOUT (string): relative path for the output directory

# INPUT PARAMETERS
Year = int(sys.argv[1])
Acc = 24
Git_repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/ecPoint_Climate"
DirIN = "Data/Compute/02_UniqueOBS_Combine-Datasets-Times-PerDay"
DirOUT = "Data/Compute/03_UniqueStnids_Extract-List-PerYear"
#####################################################################

# Setting main output directory
MainDirOUT = Git_repo + "/" + DirOUT
if not exists(MainDirOUT):
      os.makedirs(MainDirOUT)

# Identify unique stnids over the considered period
print("Extracting the stnids for rainfall observations on...")
stnids_year = np.array([])
lats_year = np.array([])
lons_year = np.array([])

TheDateS = date(Year,1,2)
TheDateF = date(Year,12,31)
TheDate = TheDateS

while TheDate <= TheDateF:
      TheDateSTR = TheDate.strftime("%Y%m%d")
      TheYearSTR = TheDate.strftime("%Y")
      print(" - " + TheDateSTR)
      FileIN = Git_repo + "/" + DirIN + "/" + TheYearSTR + "/tp" + str(Acc) + "_obs_" + TheDateSTR + ".geo"
      geo = mv.read(FileIN)
      stnids_year = np.append(stnids_year, np.array(mv.stnids(geo)))
      lats_year = np.append(lats_year, mv.latitudes(geo))
      lons_year = np.append(lons_year, mv.longitudes(geo))
      TheDate += timedelta(days=1)

# Extracting the unique stnids
print("Extracting the unique stnids...")
stnids_unique_year, ind_stnids_unique = np.unique(stnids_year, return_index=True)
lats_unique_year = lats_year[ind_stnids_unique]
lons_unique_year = lons_year[ind_stnids_unique]
print(str(len(stnids_unique_year)) + " unique stnids found for " + str(Year))

# Saving the unique stnids
np.save(MainDirOUT + "/stnids_unique_" + str(Year), stnids_unique_year)
np.save(MainDirOUT + "/lats_unique_" + str(Year), lats_unique_year)
np.save(MainDirOUT + "/lons_unique_" + str(Year), lons_unique_year)