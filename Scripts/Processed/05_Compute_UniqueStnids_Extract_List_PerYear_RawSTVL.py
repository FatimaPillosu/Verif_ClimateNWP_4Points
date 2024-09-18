import os
from os.path import exists
from datetime import date, timedelta
import numpy as np
import metview as mv

######################################################################
# CODE DESCRIPTION
# 05_Compute_UniqueStnids_Extract_List_PerYear_RawSTVL.py extracts the list of 
# unique stnids in a given year.
# Code runtime: ~ 40 minutes. 

# DESCRIPTION OF INPUT PARAMETERS
# YearS (integer, in YYYY format): start year to consider.
# YearF (integer, in YYYY format): final year to consider.
# Acc (integer, in hours): rainfall accumulation period.
# Git_Repo (string): path of local github repository.
# DirIN (string): relative path for the input directory.
# DirOUT (string): relative path for the output directory.

# INPUT PARAMETERS
YearS = 2000
YearF = 2019
Acc = 24
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_ClimateNWP_4Points"
DirIN = "Data/Compute/02_UniqueOBS_Combine_Datasets_Times_PerDay_RawSTVL"
DirOUT = "Data/Compute/05_UniqueStnids_Extract_List_PerYear_RawSTVL"
######################################################################

# Setting main output directory
MainDirOUT = Git_Repo + "/" + DirOUT + "/" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF)
if not exists(MainDirOUT):
      os.makedirs(MainDirOUT)

# Splitting the computations in years due to memory issues
for Year in range(YearS, YearF+1):

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
            
            FileIN = Git_Repo + "/" + DirIN + "/" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF) + "/" + TheYearSTR + "/tp" + str(Acc) + "_obs_" + TheDateSTR + ".geo"
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