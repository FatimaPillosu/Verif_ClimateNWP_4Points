import os
from os.path import exists
from datetime import date, timedelta
import metview as mv

########################################################################
# CODE DESCRIPTION
# 02_Compute_UniqueOBS_Combine_Datasets_Times_PerDay_RawSTVL.py combines 
# into a single geopoint file all rainfall observations from different datasets and times for 
# a given day. Observations saved as day X refer to measurements valid for day (X-1).
# Code runtime: ~ 10 minutes.

# DESCRIPTION OF INPUT PARAMETERS
# YearS (integer, in YYYY format): start year to consider.
# YearF (integer, in YYYY format): final year to consider.
# Acc (integer, in hours): rainfall accumulation period.
# Dataset_list (string): name of datasets to consider.
# Git_Repo (string): path of local GitHub repository.
# DirIN (string): relative path for the input directory.
# DirOUT (string): relative path for the output directory.

# INPUT PARAMETERS
YearS = 2000
YearF = 2019
Acc = 24
Dataset_list = ["synop", "bom", "india", "vnm", "efas"]
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_ClimateNWP_4Points"
DirIN = "Data/Compute/01_UniqueOBS_Extract_FromReference_RawSTVL"
DirOUT = "Data/Compute/02_UniqueOBS_Combine_Datasets_Times_PerDay_RawSTVL"
########################################################################

# Combining, into a single geopoint file for a given day, all rainfall observations from different datasets and times in a day
for Year in range(YearS,YearF+1):

      # Setting main output directory for the given year
      MainDirOUT = Git_Repo + "/" + DirOUT + "/" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF) + "/" + str(Year)
      if not exists(MainDirOUT):
            os.makedirs(MainDirOUT)

      # Reading and combining all the rainfall observations for the given year (for all considered datasets and for all times in a day)
      TheDateS = date(Year,1,1)
      TheDateF = date(Year,12,31)
      TheDate = TheDateS
      while TheDate <= TheDateF:
            
            TheDateSTR  = TheDate.strftime("%Y%m%d")
            print(" ")
            print("Reading the rainfall observations for " + TheDateSTR + "...")

            print("  - Combining the observations for all considered datasets and times in the day into a single geopoint file...")
            obs_combined = None
            for TheTime in range(0,24):
                  TheTimeSTR = f"{TheTime:02d}"
                  for Dataset in Dataset_list:
                        FileIN_temp = Git_Repo + "/" + DirIN + "/" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF) + "/" + Dataset + "/" + TheDateSTR + "/tp" + f'{Acc:02d}' + "_obs_" + TheDateSTR + TheTimeSTR + ".geo"
                        if exists(FileIN_temp):
                              obs_combined = mv.merge(obs_combined, mv.read(FileIN_temp))

            # Saving the combined observations into a single geopoint file
            if mv.count(obs_combined) != 0:
                  print("  - Saving the single geopoint file for the combined observations ...")
                  FileOUT_temp = MainDirOUT + "/tp" + f'{Acc:02d}' + "_obs_" + TheDateSTR + ".geo"
                  mv.write(FileOUT_temp, obs_combined)
            else:
                  print("  - Empty geopoint. Nothing to save.")
            
            TheDate += timedelta(days=1)