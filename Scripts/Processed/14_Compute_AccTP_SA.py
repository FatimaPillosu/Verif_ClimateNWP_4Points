import os
import sys
from datetime import datetime, timedelta
import numpy as np
import metview as mv

############################################################################

# CODE DESCRIPTION
# 01_Compute_AccTP_SA.py computes the indipendent accumulated rainfall realizations. It 
# also saves the global field in the required number of sub-areas. The currently implemented 
# functions compute rainfall realizations for:
#     -> 12-hourly ERA5
#     -> 24-hourly ERA5
#     -> 12-hourly ERA5_ecPoint
#     -> 24-hourly ERA5_ecPoint
#     -> multiple rainfall accumulations from Reforecasts
# Code runtime: the code can take up to 3 hours to run in serial. The runtime might vary  
# substantially according to the considered dataset.

# DESCRIPTION OF INPUT PARAMETERS
# Year (date, in the format YYYY): year to consider.
# Acc (integer, in hours): rainfall accumulation period.
# NumSA (integer): number of sub-areas to consider.
# Dataset_SystemFC (string): name of the dataset and forecasting system to consider.
# Git_Repo (string): path of local github repository.
# DirIN (string): relative path for the directory containing the modelled rainfall datasets.
# DirOUT (string): relative path for the directory containing the rainfall realizations (sub-area).

# INPUT PARAMETERS
Year = int(sys.argv[1])
Acc =  int(sys.argv[2])
NumSA =  int(sys.argv[3])
Dataset_SystemFC =  sys.argv[4]
Git_Repo = sys.argv[5]
DirIN = sys.argv[6]
DirOUT = sys.argv[7]
############################################################################


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
            tp = mv.values(tp).T.astype(np.float16)
      else:
            tp = np.array([])
      return tp

#############################################
# 12-hourly rainfall realizations from short-range ERA5 #
#############################################

def tp_ShortRange_ERA5_12h(BaseDateTime, DirIN):
      
      # Initializing the variable that stores the accumulated rainfall for the accumulation periods 00-12 UTC and 12-00 UTC
      tp_12 = 0
      tp_00 = 0
      count_steps_12 = 0 # to make sure that both required dates are available in the datebase
      count_steps_00 = 0 # to make sure that both required dates are available in the datebase

      # Extracting the accumulated rainfall values for the accumulation period 00-12 UTC
      BaseDateTime_1 = BaseDateTime - timedelta(days=1) + timedelta(hours=18)
      BaseDateTime_0 = BaseDateTime + timedelta(hours=6)
      for Step in range(7,(12+1)):
            DirIN_1 = DirIN + "/" + BaseDateTime_1.strftime("%Y") + "/" + BaseDateTime_1.strftime("%Y%m%d%H")
            FileIN_1 =  "tp_" + BaseDateTime_1.strftime("%Y%m%d") + "_" + BaseDateTime_1.strftime("%H") + "_" + f'{Step:03d}' + ".grib"
            if os.path.exists(DirIN_1 + "/" + FileIN_1):
                  count_steps_12 = count_steps_12 + 1
                  tp_12 = tp_12 + mv.read(DirIN_1 + "/" + FileIN_1)
      for Step in range(1,(6+1)):  
            DirIN_0 = DirIN + "/" + BaseDateTime_0.strftime("%Y") + "/" + BaseDateTime_0.strftime("%Y%m%d%H")
            FileIN_0 =  "tp_" + BaseDateTime_0.strftime("%Y%m%d") + "_" + BaseDateTime_0.strftime("%H") + "_" + f'{Step:03d}' + ".grib"
            if os.path.exists(DirIN_0 + "/" + FileIN_0):
                  count_steps_12 = count_steps_12 + 1
                  tp_12 = tp_12 + mv.read(DirIN_0 + "/" + FileIN_0)

      # Extracting the accumulated rainfall values for the accumulation period 12-00 UTC
      BaseDateTime_0 = BaseDateTime + timedelta(hours=6)
      BaseDateTime_1 = BaseDateTime + timedelta(hours=18)
      for Step in range(7,(12+1)):
            DirIN_0 = DirIN + "/" + BaseDateTime_0.strftime("%Y") + "/" + BaseDateTime_0.strftime("%Y%m%d%H")
            FileIN_0 =  "tp_" + BaseDateTime_0.strftime("%Y%m%d") + "_" + BaseDateTime_0.strftime("%H") + "_" + f'{Step:03d}' + ".grib"
            if os.path.exists(DirIN_0 + "/" + FileIN_0):
                  count_steps_00 = count_steps_00 + 1
                  tp_00 = tp_00 + mv.read(DirIN_0 + "/" + FileIN_0)
      for Step in range(1,(6+1)):
            DirIN_1 = DirIN + "/" + BaseDateTime_1.strftime("%Y") + "/" + BaseDateTime_1.strftime("%Y%m%d%H")
            FileIN_1 =  "tp_" + BaseDateTime_1.strftime("%Y%m%d") + "_" + BaseDateTime_1.strftime("%H") + "_" + f'{Step:03d}' + ".grib"
            if os.path.exists(DirIN_1 + "/" + FileIN_1):
                  count_steps_00 = count_steps_00 + 1
                  tp_00 = tp_00 + mv.read(DirIN_1 + "/" + FileIN_1)

      # Converting the accumulated rainfall totals from m to mm, creating the variable that stores the independent rainfall realizations, and converting the fieldset into a 16-byte float numpy array (to reduce memory consumption)
      if count_steps_12 == 12 and count_steps_00 == 12: 
            tp_12 = tp_12 * 1000
            tp_00 = tp_00 * 1000
            tp = mv.merge(tp_12, tp_00)
            tp = mv.values(tp).T.astype(np.float16)
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
            tp = mv.values(tp).T.astype(np.float16)
      else:
            tp = np.array([])
      
      return tp

##################################################
# 24-hourly rainfall realizations from short-range ERA5_EDA #
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
            tp = mv.values(tp).T.astype(np.float16)
      else:
            tp = np.array([])
      
      return tp

###########################################
# 12-hourly rainfall realizations from ERA5_ecPoint #
###########################################

# Note: the rainfall values are already in mm
def tp_ERA5_ecPoint_12h(BaseDateTime, DirIN):

      # Initializing the variable that stores the accumulated rainfall for the accumulation periods 00-12 UTC and 12-00 UTC
      tp_12 = 0
      tp_00 = 0

      # Extracting the accumulated rainfall values for the accumulation period 00-12 UTC
      DirIN_12 = DirIN + "/Pt_BC_PERC/" + BaseDateTime.strftime("%Y%m")
      FileIN_12 =  "Pt_BC_PERC_" + BaseDateTime.strftime("%Y%m%d") + "_12.grib2"
      if os.path.exists(DirIN_12 + "/" + FileIN_12):
            tp_12 = mv.read(DirIN_12 + "/" + FileIN_12)
      
      # Extracting the accumulated rainfall values for the accumulation period 12-00 UTC
      DirIN_00 = DirIN + "/Pt_BC_PERC/" + BaseDateTime.strftime("%Y%m")
      FileIN_00 =  "Pt_BC_PERC_" + BaseDateTime.strftime("%Y%m%d") + "_24.grib2"
      if os.path.exists(DirIN_00 + "/" + FileIN_00):
            tp_00 = mv.read(DirIN_00 + "/" + FileIN_00)

      # Creating the variable that stores the independent rainfall realizations, and converting the fieldset into a 16-byte float numpy array (to reduce memory consumption)
      if tp_12 != 0 and tp_00 != 0: 
            tp = mv.merge(tp_12, tp_00)
            tp = mv.values(tp).T.astype(np.float16)
      else:
            tp = np.array([])

      return tp

###########################################
# 24-hourly rainfall realizations from ERA5_ecPoint #
###########################################

# Note: the rainfall values are already in mm and are valid for the period 00-00 UTC
def tp_ERA5_ecPoint_24h(BaseDateTime, DirIN):

      # Reading the accumulated rainfall values, and converting the fieldset into a 16-byte float numpy array (to reduce memory consumption)
      DirIN = DirIN + "/Pt_BC_PERC/" + BaseDateTime.strftime("%Y%m")
      FileIN =  "Pt_BC_PERC_" + BaseDateTime.strftime("%Y%m%d") + ".grib2"
      if os.path.exists(DirIN + "/" + FileIN):
            tp = mv.read(DirIN + "/" + FileIN)
            tp = mv.values(tp).T.astype(np.float16)
      else:
            tp = np.array([])
      
      return tp

###############################################################################################################


# Extracting the names of the dataset and forecasting system to consider
Dataset = Dataset_SystemFC.split("/")[0]
SystemFC = Dataset_SystemFC.split("/")[1]

# Extracting the indipendent accumulated rainfall realizations for a specific number of sub-areas
print("Extracting accumulated rainfall totals for " + Dataset + " " + SystemFC)
BaseDateS = datetime(Year,1,2)
BaseDateF = datetime(Year,12,31)
BaseDate = BaseDateS

while BaseDate <= BaseDateF:
      
      print(" - Processing the date: ", BaseDate)

      # Defining the input directories
      DirIN_temp = Git_Repo + "/" + DirIN + "/" + Dataset + "/" + SystemFC
      if SystemFC == "ERA5_ecPoint":
            DirIN_temp = DirIN_temp + "_" + f'{Acc:02d}' + "h"

      # Computing the indipendent accumulated rainfall totals
      if Dataset == "Reforecasts":  
            tp_temp = tp_Reforecast(Acc, BaseDate, DirIN_temp)
      elif Dataset == "Reanalysis" and SystemFC == "ERA5_EDA" and Acc == 24:
            tp_temp = tp_ShortRange_ERA5_EDA_24h(BaseDate, DirIN_temp)      
      elif Dataset == "Reanalysis" and SystemFC == "ERA5" and Acc == 12:  
            tp_temp = tp_ShortRange_ERA5_12h(BaseDate, DirIN_temp)
      elif Dataset == "Reanalysis" and SystemFC == "ERA5" and Acc == 24:
            tp_temp = tp_ShortRange_ERA5_24h(BaseDate, DirIN_temp)      
      elif Dataset == "Reanalysis" and SystemFC == "ERA5_ecPoint" and Acc == 12:
            tp_temp = tp_ERA5_ecPoint_12h(BaseDate, DirIN_temp)
      elif Dataset == "Reanalysis" and SystemFC == "ERA5_ecPoint" and Acc == 24:
            tp_temp = tp_ERA5_ecPoint_24h(BaseDate, DirIN_temp)
      else:
            print("ERROR! Considered dataset not valid.")
            exit()
      NumGP_Global = tp_temp.shape[0]

      # Extracting the sub-areas
      if NumGP_Global != 0:
            
            i = int(0)
            j = int(NumGP_Global/NumSA)
            
            for ind_SA in range(NumSA):
                  
                  if SystemFC == "ERA5" and Acc == 24:
                        tp_sa_temp = tp_temp[i:j] # for datasets that have only one realization per day
                  else:
                        tp_sa_temp = tp_temp[i:j,:] # for datasets that have more than one realization per day

                  # Saving the extracted sub-areas
                  DirOUT_temp = Git_Repo + "/" + DirOUT + "/" + f'{Acc:02d}' + "h/" + Dataset_SystemFC + "/" + BaseDate.strftime("%Y%m%d")
                  if not os.path.exists(DirOUT_temp):
                        os.makedirs(DirOUT_temp)
                  FileOUT_temp = "tp_" + BaseDate.strftime("%Y%m%d") + "_" + f'{ind_SA:03d}' + ".npy"
                  np.save(DirOUT_temp + "/" + FileOUT_temp, tp_sa_temp) 

                  i = int(j)
                  j = int(j + (NumGP_Global/NumSA))

      BaseDate = BaseDate + timedelta(days=1)