import os
import sys
from datetime import datetime, timedelta
import numpy as np
import metview as mv

##################################################################################
# CODE DESCRIPTION
# 15_Compute_ClimateSA.py computes the modelled rainfall climatology for a specific sub-area.
# Code runtime: the code takes up to 5 minutes to run in serial but for ERA5_ecPoint it takes up to 
# 90 minutes.

# DESCRIPTION OF INPUT PARAMETERS
# YearS (integer, in the format YYYY): start year to consider.
# YearF (integer, in the format YYYY): final year to consider.
# Acc (integer, in hours): rainfall accumul
# CodeSA (integer): sub-area to consider.ation period.
# RP_list (list of integers, in years): list of return periods to compute.
# Dataset_SystemFC (string): name of the dataset and forecasting system to consider.
# Git_Repo (string): path of local GitHub repository.
# DirIN (string): relative path for the directory containing the rainfall realizations (sub-area).
# DirOUT_Climate_SA (string): relative path for the directory containing the climatology (sub-area).
# DirOUT_Climate_G (string): relative path for the directory containing the computed return periods.

# INPUT PARAMETERS
YearS = int(sys.argv[1])
YearF = int(sys.argv[2])
Acc = int(sys.argv[3])
CodeSA = int(sys.argv[4])
RP_list = sys.argv[5]
Dataset_SystemFC = sys.argv[6]
Git_Repo = sys.argv[7]
DirIN =  sys.argv[8]
DirOUT_Climate_SA = sys.argv[9]
DirOUT_Climate_G = sys.argv[10]
##################################################################################


# Creating the main output directories
DirOUT_Climate_SA_temp = Git_Repo + "/" + DirOUT_Climate_SA + "/" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF) + "/" + Dataset_SystemFC
DirOUT_Climate_G_temp = Git_Repo + "/" + DirOUT_Climate_G + "/" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF) + "/" + Dataset_SystemFC
if not os.path.exists(DirOUT_Climate_SA_temp):
      os.makedirs(DirOUT_Climate_SA_temp)
if not os.path.exists(DirOUT_Climate_G_temp):
      os.makedirs(DirOUT_Climate_G_temp)

# Defining the period to consider
BaseDateS = datetime(YearS,1,1,0)
BaseDateF = datetime(YearF,12,31,0)

# Converting "RP_list" into a list
RP_list = np.array(list(map(int, RP_list.split(","))))

# Extracting the names of the dataset and forecasting system to consider
Dataset = Dataset_SystemFC.split("/")[0]
SystemFC = Dataset_SystemFC.split("/")[1]

# Reading the indipendent rainfall realizations for the full period, for a specific sub-area
print("Reading the indipendent rainfall realizations for " + SystemFC + ", for the full climatological period and for the sub-area n." + str(CodeSA))
ind = 0
BaseDate = BaseDateS
while BaseDate <= BaseDateF:
      FileIN = Git_Repo + "/" + DirIN + "/" + f'{Acc:02d}' + "h/" + Dataset_SystemFC + "/" + BaseDate.strftime("%Y%m%d") + "/tp_" + BaseDate.strftime("%Y%m%d") + "_" + f'{CodeSA:03d}' + ".npy"
      if os.path.isfile(FileIN):
            print(" - Processing the date: ", BaseDate)
            tp_SA = np.load(FileIN)
            if ind == 0: 
                  BaseDate_template = BaseDate
                  tp_full_period_sa = tp_SA
            else:
                  if SystemFC == "ERA5":
                        tp_full_period_sa = np.vstack((tp_full_period_sa, tp_SA))
                  else:
                        tp_full_period_sa = np.concatenate((tp_full_period_sa, tp_SA), axis = 1)
            ind = ind + 1
      BaseDate = BaseDate + timedelta(days=1)

if SystemFC == "ERA5":
      tp_full_period_sa = tp_full_period_sa.T

# Defining the return periods that can be computed given the actual number of realizations available in the modelled dataset
Min_Num_Real = 365 * RP_list
Num_Real = tp_full_period_sa.shape[1]
ind_RP = np.where(Min_Num_Real < Num_Real)[0]
RP_list = RP_list[ind_RP]
Perc_2_Comp = 100 - ( (1/(RP_list * 365) ) * 100)
Perc_2_Comp = np.concatenate((np.arange(0,100), Perc_2_Comp))
RP_2_Comp = 100 / ( 365 * (100 - Perc_2_Comp) )
RP_2_Comp = (np.round(RP_2_Comp, decimals = 5)).astype('float64')

# Computing the rainfall climatology as percentiles
print("Computing the rainfall climatology")
percs_sa = np.percentile(tp_full_period_sa, Perc_2_Comp, axis=1).T

# Saving the rainfall climatology for the specific sub-area
print("Saving the rainfall climatology")
np.save(DirOUT_Climate_SA_temp + "/Climate_SA_" + f'{CodeSA:03d}' + ".npy", percs_sa)

# Saving metadata
if CodeSA == 0:

      # Saving the template for the global grib file 
      if Dataset_SystemFC == "Reanalysis/ERA5_EDA":
            template_global = mv.read(Git_Repo + "/Data/Raw/" + Dataset_SystemFC + "/" + BaseDate_template.strftime("%Y") + "/" + BaseDate_template.strftime("%Y%m%d") + "06/tp_" + BaseDate_template.strftime("%Y%m%d") + "_06_000.grib")[0]
      elif Dataset_SystemFC == "Reanalysis/ERA5":
            template_global = mv.read(Git_Repo + "/Data/Raw/" + Dataset_SystemFC + "/" + BaseDate_template.strftime("%Y") + "/" + BaseDate_template.strftime("%Y%m%d") + "06/tp_" + BaseDate_template.strftime("%Y%m%d") + "_06_000.grib")
      elif Dataset_SystemFC == "Reanalysis/ERA5_ecPoint":
            template_global = mv.read(Git_Repo + "/Data/Raw/" + Dataset_SystemFC + "_" + f'{Acc:02d}' + "h/Pt_BC_PERC/" + BaseDate_template.strftime("%Y%m") + "/Pt_BC_PERC_" + BaseDate_template.strftime("%Y%m%d") + ".grib2")[0]
      elif Dataset_SystemFC == "Reforecasts/ECMWF_46r1":
            template_global = mv.read(Git_Repo + "/Data/Raw/" + Dataset_SystemFC + "/" + BaseDate_template.strftime("%Y") + "/" + BaseDate_template.strftime("%Y%m%d") + "00/tp_" + BaseDate_template.strftime("%Y%m%d") + "_00_000.grib")
      mv.write(DirOUT_Climate_G_temp + "/Template_Global.grib", template_global)

      # Saving the array containing the return periods and percentiles that were actually computed
      np.save(DirOUT_Climate_G_temp + "/RP.npy", RP_2_Comp)
      np.save(DirOUT_Climate_G_temp + "/Perc.npy", Perc_2_Comp)