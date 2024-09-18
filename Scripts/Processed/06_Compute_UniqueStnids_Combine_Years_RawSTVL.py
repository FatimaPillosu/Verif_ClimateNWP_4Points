import os
from os.path import exists
import numpy as np

#######################################################################
# CODE DESCRIPTION
# 06_Compute_UniqueStnids_Combine_Years_RawSTVL.py combines the unique stnids 
# in each year for all the years considered.
# Code runtime: negligible

# DESCRIPTION OF INPUT PARAMETERS
# YearS (integer, in YYYY format): start year to consider.
# YearF (integer, in YYYY format): final year to consider.
# Acc (integer, in hours): rainfall accumulation period.
# Git_Repo (string): path of local GitHub repository
# DirIN (string): relative path for the input directory.
# DirOUT (string): relative path for the output directory.

# INPUT PARAMETERS
YearS = 2000
YearF = 2019
Acc = 24
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_ClimateNWP_4Points"
DirIN = "Data/Compute/05_UniqueStnids_Extract_List_PerYear_RawSTVL"
DirOUT = "Data/Compute/06_UniqueStnids_Combine_Years_RawSTVL"
#######################################################################

# Setting main input/output directories
MainDirIN = Git_Repo + "/" + DirIN + "/" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF) + "/" + str(Year)
MainDirOUT = Git_Repo + "/" + DirOUT + "/" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF) + "/" + str(Year)
if not exists(MainDirOUT):
      os.makedirs(MainDirOUT)

# Defining the unique stnids for the considered period of time
stnids_all = np.array([])
lats_all = np.array([])
lons_all = np.array([])
for Year in range(YearS,YearF+1):
      stnids_all = np.append(stnids_all, np.load(MainDirIN +  "/stnids_unique_" + str(Year) + ".npy"))
      lats_all = np.append(lats_all, np.load(MainDirIN +  "/lats_unique_" + str(Year) + ".npy"))
      lons_all = np.append(lons_all, np.load(MainDirIN +  "/lons_unique_" + str(Year) + ".npy"))
stnids_unique, ind_stnids_unique = np.unique(stnids_all, return_index=True)
lats_unique = lats_all[ind_stnids_unique]
lons_unique = lons_all[ind_stnids_unique]
print(str(len(stnids_unique)) + " unique stnids found for the period between " + str(YearS) + " and " + str(YearF))

# Saving the unique stnids for the period considered
np.save(MainDirOUT +  "/stnids_unique.npy", stnids_unique)
np.save(MainDirOUT +  "/lats_unique.npy", lats_unique)
np.save(MainDirOUT +  "/lons_unique.npy", lons_unique)