import os
from datetime import datetime, timedelta
import numpy as np
import metview as mv

###################################################################################################
# CODE DESCRIPTION
# 18_Compute_Extract_RealizationsTP.py extracts indipendent rainfall realizations from observations and NWP models.
# Code runtime: ~ 12 hours.

# DESCRIPTION OF INPUT PARAMETERS
# YearS (date, in YYYYMMDD format): start year to consider.
# YearF (date, in YYYY format): final year to consider.
# Acc (integer, in hours): rainfall accumulation period.
# MinDays_Perc (float, from 0 to 1): % of min n. of days with valid obs at each location.
# SystemNWP_list (list of string): list of considered NWP models.
# Git_Repo (string): path of local GitHub repository.
# DirIN_OBS (string): relative path for the directory containing the rainfall observations.
# DirIN_NWP (string): relative path for the directory containing the NWP modelled rainfall reanalysis/reforecasts.
# DirOUT (string): relative path for the directory containing the indipendent rainfall realizations.

# INPUT PARAMETERS
YearS = 2000
YearF = 2019
Acc = 24
MinDays_Perc = 0.75
SystemNWP_list = ["Reanalysis/ERA5_EDA", "Reanalysis/ERA5", "Reforecasts/ECMWF_46r1", "Reanalysis/ERA5_ecPoint"]
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_ClimateNWP_4Points"
DirIN_OBS = "Data/Compute/10_AlignOBS_CleanSTVL/Coeff_Grid2Point_20"
DirIN_NWP = "Data/Raw/NWP"
DirOUT = "Data/Compute/18_Extract_RealizationsTP"
###################################################################################################


# CUSTOM FUNCTIONS

########################################################
# Rainfall realizations (for multiple accumulations) from Reforecasts #
########################################################

def tp_Reforecast(Acc, BaseDateTime, DirIN):

      tp = None
      DirIN = DirIN + "/" + BaseDateTime.strftime("%Y") + "/" + BaseDateTime.strftime("%Y%m%d%H")
      if os.path.exists(DirIN):
            for StepS in range(0, 240+1-Acc, Acc):
                  StepF = StepS + Acc
                  FileIN1 =  "tp_" + BaseDateTime.strftime("%Y%m%d") + "_" + BaseDateTime.strftime("%H") + "_" + f'{StepS:03d}' + ".grib"
                  FileIN2 =  "tp_" + BaseDateTime.strftime("%Y%m%d") + "_" + BaseDateTime.strftime("%H") + "_" + f'{StepF:03d}' + ".grib"
                  tp1 = mv.read(DirIN + "/" + FileIN1)
                  tp2 = mv.read(DirIN + "/" + FileIN2)
                  tp = mv.merge(tp, (tp2-tp1)*1000 )
      else:
            tp = np.array([])
      return tp


#############################################
# 24-hourly rainfall realizations from short-range ERA5 #
#############################################

def tp_ShortRange_ERA5_24h(BaseDateTime, DirIN):

      # Computing the accumulated rainfall totals
      BaseDateTime_0 = BaseDateTime + timedelta(hours=6)
      BaseDateTime_1 = BaseDateTime - timedelta(days=1) + timedelta(hours=18)
      count_steps = 0 # to make sure that both required dates are available in the datebase
      tp = 0
      
      for Step in range(7,(12+1)):
            DirIN_1 = DirIN + "/" + BaseDateTime_1.strftime("%Y") + "/" + BaseDateTime_1.strftime("%Y%m%d%H")
            FileIN_1 =  "tp_" + BaseDateTime_1.strftime("%Y%m%d") + "_" + BaseDateTime_1.strftime("%H") + "_" + f'{Step:03d}' + ".grib"
            if os.path.exists(DirIN_1 + "/" + FileIN_1):
                  count_steps = count_steps + 1
                  tp = tp + mv.read(DirIN_1 + "/" + FileIN_1)

      for Step in range(1,(18+1)):  
            DirIN_0 = DirIN + "/" + BaseDateTime_0.strftime("%Y") + "/" + BaseDateTime_0.strftime("%Y%m%d%H")
            FileIN_0 =  "tp_" + BaseDateTime_0.strftime("%Y%m%d") + "_" + BaseDateTime_0.strftime("%H") + "_" + f'{Step:03d}' + ".grib"
            if os.path.exists(DirIN_0 + "/" + FileIN_0):
                  count_steps = count_steps + 1
                  tp = tp + mv.read(DirIN_0 + "/" + FileIN_0)

      # Converting the accumulated rainfall totals from m to mm, and converting the fieldset into a 16-byte float numpy array (to reduce memory consumption)
      if count_steps == 24:
            tp = tp * 1000
      else:
            tp = np.array([])
      
      return tp

##################################################
# 24-hourly rainfall realizations from short-range ERA5-EDA #
##################################################

def tp_ShortRange_ERA5_EDA_24h(BaseDateTime, DirIN):

      # Computing the accumulated rainfall totals
      BaseDateTime_0 = BaseDateTime + timedelta(hours=6)
      BaseDateTime_1 = BaseDateTime - timedelta(days=1) + timedelta(hours=18)
      count_steps = 0 # to make sure that both required dates are available in the datebase
      tp = 0
      
      for Step in range(9, (12+1), 3):
            DirIN_1 = DirIN + "/" + BaseDateTime_1.strftime("%Y") + "/" + BaseDateTime_1.strftime("%Y%m%d%H")
            FileIN_1 =  "tp_" + BaseDateTime_1.strftime("%Y%m%d") + "_" + BaseDateTime_1.strftime("%H") + "_" + f'{Step:03d}' + ".grib"
            if os.path.exists(DirIN_1 + "/" + FileIN_1):
                  count_steps = count_steps + 1
                  tp = tp + mv.read(DirIN_1 + "/" + FileIN_1)

      for Step in range(3, (18+1), 3):  
            DirIN_0 = DirIN + "/" + BaseDateTime_0.strftime("%Y") + "/" + BaseDateTime_0.strftime("%Y%m%d%H")
            FileIN_0 =  "tp_" + BaseDateTime_0.strftime("%Y%m%d") + "_" + BaseDateTime_0.strftime("%H") + "_" + f'{Step:03d}' + ".grib"
            if os.path.exists(DirIN_0 + "/" + FileIN_0):
                  count_steps = count_steps + 1
                  tp = tp + mv.read(DirIN_0 + "/" + FileIN_0)

      # Converting the accumulated rainfall totals from m to mm, and converting the fieldset into a 16-byte float numpy array (to reduce memory consumption)
      if count_steps == 8:
            tp = tp * 1000
      else:
            tp = np.array([])
      
      return tp

###########################################
# 24-hourly rainfall realizations from ERA5_ecPoint #
###########################################

# Note: the rainfall values are already in mm and are valid for the period 00-00 UTC
def tp_ERA5_ecPoint_24h(BaseDateTime, DirIN):

      # Reading the accumulated rainfall values, and converting the fieldset into a 16-byte float numpy array (to reduce memory consumption)
      DirIN = DirIN + "/" + BaseDateTime.strftime("%Y%m")
      FileIN =  "Pt_BC_PERC_" + BaseDateTime.strftime("%Y%m%d") + ".grib2"

      if os.path.exists(DirIN + "/" + FileIN):
            tp = mv.read(DirIN + "/" + FileIN)
      else:
            tp = np.array([])
      
      return tp

###############################################################################################################


# Reading the observational climatology
print()
print("Reading the realizations from rainfall observations...")
MainDirIN_OBS = Git_Repo + "/" + DirIN_OBS + "/" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF)
vals_obs = np.load(MainDirIN_OBS + "/obs.npy")
lats_obs = np.load(MainDirIN_OBS + "/stn_lats.npy")
lons_obs = np.load(MainDirIN_OBS + "/stn_lons.npy")
num_stn = vals_obs.shape[0]

# Selecting the stations with the required minimum number of days with valid observations
print("Selecting the stations with the considered minimum number of days with valid observations...")
MinNumDays = round(vals_obs.shape[1] * MinDays_Perc)
NumDays_NotNaN = np.sum(~np.isnan(vals_obs), axis=1) # array containing the n. of days with observations for each rain gauge
ind_stns_MinNumDays = np.where(NumDays_NotNaN >= MinNumDays)[0]
obs_MinNumDays = vals_obs[ind_stns_MinNumDays,:] # array containin only the stations that satisfied the minimum n. of days with observationss
lats_MinNumDays = lats_obs[ind_stns_MinNumDays]
lons_MinNumDays = lons_obs[ind_stns_MinNumDays]
print(" - Total number of days between " + str(YearS) + " and " + str(YearF) + ": " + str(vals_obs.shape[1]))
print(" - Totals number of stations with at least " + str(int(MinDays_Perc*100)) + "% of days (= " + str(int(MinNumDays)) + ") with valid observations: " + str(len(ind_stns_MinNumDays)) + "/" + str(str(vals_obs.shape[0])))

# Saving the extracted sub-areas
DirOUT_temp = Git_Repo + "/" + DirOUT + "/" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF) + "/OBS"
if not os.path.exists(DirOUT_temp):
      os.makedirs(DirOUT_temp)
FileOUT_temp = "tp.npy"
np.save(DirOUT_temp + "/" + FileOUT_temp, obs_MinNumDays) 

# Determining the range of dates to consider for the NWP models
BaseDateS = datetime(1999, 1, 1) # to include the dates from the reforecasts
BaseDateF = datetime(2019, 12, 31)

# Extracting the indipendent rainfall realizations
for SystemNWP in SystemNWP_list:
      
      print()

      # Defining the input directories for each NWP model
      DirIN_temp = Git_Repo + "/" + DirIN_NWP + "/" + SystemNWP
      if SystemNWP == "Reanalysis/ERA5_ecPoint":
            DirIN_temp = DirIN_temp + "_" + f'{Acc:02d}' + "h"
      
      # Computing the indipendent accumulated rainfall totals
      BaseDate = BaseDateS
      while BaseDate <= BaseDateF:
      
            print("Computing the realizations for '" + SystemNWP + "', on " + BaseDate.strftime("%Y%m%d") + "...")

            if SystemNWP == "Reforecasts/ECMWF_46r1":  
                  tp_grib = tp_Reforecast(Acc, BaseDate, DirIN_temp)
            elif SystemNWP == "Reanalysis/ERA5_EDA" and Acc == 24:
                  tp_grib = tp_ShortRange_ERA5_EDA_24h(BaseDate, DirIN_temp)      
            elif SystemNWP == "Reanalysis/ERA5" and Acc == 24:
                  tp_grib = tp_ShortRange_ERA5_24h(BaseDate, DirIN_temp)
            elif SystemNWP == "Reanalysis/ERA5_ecPoint" and Acc == 24:
                  tp_grib = tp_ERA5_ecPoint_24h(BaseDate, DirIN_temp)
            else:
                  print("ERROR! Considered dataset not valid.")

            if len(tp_grib) != 0:
                  
                  # Extracting the rainfall values at the location of the considered rainfall observations
                  tp_obs = mv.nearest_gridpoint(tp_grib, lats_MinNumDays, lons_MinNumDays)

                  # Saving the extracted sub-areas
                  DirOUT_temp = Git_Repo + "/" + DirOUT + "/MinDays_Perc_" + str(MinDays_Perc*100) + "/" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF) + "/NWP/" +  SystemNWP + "/" + BaseDate.strftime("%Y")
                  if not os.path.exists(DirOUT_temp):
                        os.makedirs(DirOUT_temp)
                  FileOUT_temp = "tp_" + BaseDate.strftime("%Y%m%d") + ".npy"
                  np.save(DirOUT_temp + "/" + FileOUT_temp, tp_obs) 

            BaseDate = BaseDate + timedelta(days=1)