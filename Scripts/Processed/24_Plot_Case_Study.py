import os
from datetime import datetime, timedelta
import numpy as np
import metview as mv

###################################################################################################
# CODE DESCRIPTION
# 24_Plot_Case_Study.py plots maps of rainfall totals (from observations and NWP models) to illustrate case studies.
# Code runtime: ~ negligible.

# DESCRIPTION OF INPUT PARAMETERS
# BaseDate (date, in YYYYMMDD format): date to consider.
# Acc (integer, in hours): rainfall accumulation period.
# SystemNWP_list (list of string): list of considered NWP models.
# Git_Repo (string): path of local GitHub repository.
# DirIN (string): relative path for the directory containing the NWP modelled rainfall reanalysis/reforecasts.
# DirOUT (string): relative path for the directory containing the indipendent rainfall realizations.

# INPUT PARAMETERS
BaseDate = datetime(2008, 10, 22)
Acc = 24
SystemNWP_list = ["Reanalysis/ERA5_EDA", "Reanalysis/ERA5", "Reforecasts/ECMWF_46r1", "Reanalysis/ERA5_ecPoint"]
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_ClimateNWP_4Points"
DirIN = "Data/Raw/NWP"
DirOUT = "Data/Compute/24_Case_Study"
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


# Plotting the rainfall observations for the considered date
BaseDate

mv.shell("~moz/bin/stvl_getgeo --sources synop hdobs efas --parameter tp --period " + str(Acc) + " --dates  --times 06 --outdir data")