import os
import sys
from os.path import exists
from datetime import datetime, timedelta
import numpy as np
import metview as mv

###########################################################################
# CODE DESCRIPTION
# 01_Compute_UniqueOBS_Extract_FromReference_RawSTVL.py determines, over different 
# times and datasets, which stations are not present in the reference stations (i.e., synop at 
# 00 UTC). This is done to maximize the geographical coverage of considered rainfall 
# observations, without double counting overlapping rainfall observations at different 
# reporting times and in different datasets.
# Code runtime: ~ 10 hours.

# DESCRIPTION OF INPUT PARAMETERS
# YearS (integer, in YYYY format): start year to consider.
# YearF (integer, in YYYY format): final year to consider.
# Acc (integer, in hours): rainfall accumulation period.
# Dataset_ref (string): name of the reference dataset.
# Time_ref (integer, in UTC hours): reference time.
# Dataset_extra_list (list of strings): names of extra datasets relative to the reference dataset.
# Git_Repo (string): path of local GitHub repository.
# DirIN (string): relative path for the input directory.
# DirOUT (string): relative path for the output directory.

# INPUT PARAMETERS
YearS = 2000
YearF = 2019
Acc = 24
Dataset_ref = "synop"
Time_ref = 0
Dataset_extra_list = ["synop","hdobs", "bom", "india", "efas", "vnm"]
Git_Repo = "/ec/vol/ecpoint_dev/mofp/papers_2_write/Verif_ClimateNWP_4Points"
DirIN = "Data/Raw/OBS/STVL"
DirOUT = "Data/Compute/01_UniqueOBS_Extract_FromReference_RawSTVL"
###########################################################################


# Setting general parameters 
DateTimeS = datetime(YearS, 1, 1, Time_ref)
DateTimeF = datetime(YearF, 12, 31, Time_ref)

# Extracting the unique stations compared to the reference ones
TheDateTime_ref = DateTimeS
while TheDateTime_ref <= DateTimeF:
      
      # Reading the observations for the reference date/time and dataset
      TheDateSTR_ref = TheDateTime_ref.strftime("%Y%m%d")
      TheTimeSTR_ref = TheDateTime_ref.strftime("%H")
      FileIN_ref_temp = Git_Repo + "/" + DirIN + "_" + f'{Acc:02d}' + "h/" + Dataset_ref + "/" + TheDateSTR_ref + "/tp" + f'{Acc:02d}' + "_obs_" + TheDateSTR_ref + TheTimeSTR_ref + ".geo"
      
      if exists(FileIN_ref_temp):
            print(" ")
            print("Extracting stations from the reference dataset (" + Dataset_ref +"), for " + TheDateSTR_ref + " at " + TheTimeSTR_ref + " UTC")
            geo_ref = mv.read(FileIN_ref_temp)
            geo_ref = mv.remove_missing_values(geo_ref)
            stnids_ref = mv.stnids(geo_ref) # list
            lats_ref = mv.latitudes(geo_ref) # array
            lons_ref = mv.longitudes(geo_ref) # array
            elevation_ref = mv.levels(geo_ref) # array
            date_ref = mv.dates(geo_ref) # list
            time_ref = mv.times(geo_ref) # array
            vals_ref = mv.values(geo_ref) # array
            
            # Saving the observations for the reference date/time and dataset
            MainDirOUT_ref_temp = Git_Repo + "/" + DirOUT + "/" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF) + "/" + Dataset_ref + "/" + TheDateSTR_ref
            if not exists(MainDirOUT_ref_temp):
                  os.makedirs(MainDirOUT_ref_temp)
            FileOUT_ref_temp = MainDirOUT_ref_temp + "/tp" + f'{Acc:02d}' + "_obs_" + TheDateSTR_ref + TheTimeSTR_ref + ".geo"
            geo_ref = mv.create_geo( # To match the format in which the extra geopoints are going to be saved
                                    type = 'ncols',
                                    latitudes = lats_ref,
                                    longitudes = lons_ref,
                                    stnids = stnids_ref,
                                    levels = elevation_ref,
                                    dates = date_ref,
                                    times = time_ref, 
                                    values = vals_ref,
                                    )
            mv.write(FileOUT_ref_temp, geo_ref)
            
            # Creating geopoint files containing extra unique stations respect to the reference dataset
            for Dataset_extra in Dataset_extra_list:
                  
                  # Defining the starting extra times to consider
                  if Dataset_extra == Dataset_ref:
                        ExtraTimeS = TheDateTime_ref.hour + 1
                  else:
                        ExtraTimeS = TheDateTime_ref.hour

                  # Creating geopoint files containing unique stations over extra times respect to the reference date/time
                  for hours_extra in range(ExtraTimeS, 24, 1):
                        
                        # Reading the observations for the extra stations
                        TheDateTime_extra = TheDateTime_ref + timedelta(hours=hours_extra)
                        TheDateSTR_extra = TheDateTime_extra.strftime("%Y%m%d")
                        TheTimeSTR_extra = TheDateTime_extra.strftime("%H")
                        FileIN_extra_temp = Git_Repo + "/" + DirIN + "_" + f'{Acc:02d}' + "h/"  + "/" + Dataset_extra + "/" + TheDateSTR_extra + "/tp" + f'{Acc:02d}' + "_obs_" + TheDateSTR_extra + TheTimeSTR_extra + ".geo"
                        
                        if exists(FileIN_extra_temp):
                              print(" - Considering extra unique stations from '" + Dataset_extra + "', for " + TheDateSTR_extra + " at " + TheTimeSTR_extra + " UTC")
                              geo_extra = mv.read(FileIN_extra_temp)
                              geo_extra = mv.remove_missing_values(geo_extra)
                              stnids_extra = mv.stnids(geo_extra)
                              lats_extra = mv.latitudes(geo_extra)
                              lons_extra = mv.longitudes(geo_extra)
                              elevation_extra = mv.levels(geo_extra)
                              date_extra = mv.dates(geo_extra)
                              time_extra = mv.times(geo_extra)
                              vals_extra = mv.values(geo_extra)

                              # Defining the ids in stnids_extra that are not included in stnids_ref
                              stnids_unique = list(np.setdiff1d(stnids_extra,stnids_ref))
                              if len(stnids_unique) != 0:
                                    
                                    # Extracting different values for the unique stations
                                    lats_unique = np.array([])
                                    lons_unique = np.array([])
                                    elevation_unique = np.array([])
                                    date_unique = []
                                    time_unique = np.array([])
                                    vals_unique = np.array([])
                                    for item in stnids_unique:
                                          ind = stnids_extra.index(item)
                                          lats_unique = np.append(lats_unique, lats_extra[ind])
                                          lons_unique = np.append(lons_unique, lons_extra[ind])
                                          elevation_unique = np.append(elevation_unique, elevation_extra[ind])
                                          date_unique.append(date_extra[ind])
                                          time_unique = np.append(time_unique, time_extra[ind])
                                          vals_unique = np.append(vals_unique, vals_extra[ind])
                                    
                                    # Creating the geopoint file containing only the unique stations 
                                    geo_unique = mv.create_geo(
                                          type = 'ncols',
                                          latitudes = lats_unique,
                                          longitudes = lons_unique,
                                          stnids = stnids_unique,
                                          levels = elevation_unique,
                                          dates = date_unique,
                                          times = time_unique, 
                                          values = vals_unique,
                                          )
                                    
                                    # Saving the geopoint file containing only the unique stations 
                                    MainDirOUT_extra_temp = Git_Repo + "/" + DirOUT + "/" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF) + "/" + Dataset_extra + "/" + TheDateSTR_extra
                                    if not exists(MainDirOUT_extra_temp):
                                          os.makedirs(MainDirOUT_extra_temp)
                                    FileOUT_extra_temp = MainDirOUT_extra_temp + "/tp" + f'{Acc:02d}' + "_obs_" + TheDateSTR_extra + TheTimeSTR_extra + ".geo"
                                    mv.write(FileOUT_extra_temp, geo_unique)

                                    # Adding the ids of the unique stations to the ids of the reference stations
                                    stnids_ref.extend(stnids_unique)

      TheDateTime_ref += timedelta(days=1)