import sys
import os
from os.path import exists
import numpy as np

#############################################################################################################################################
# CODE DESCRIPTION
# 11_Compute_ClimateFC_atOBS.py computes modelled rainfall climatologies from different forecasting systems, at the location of available point rainfall climatologies over 
# a given period. The climatologies are computed in the form of a distribution of percentiles (using the method of linear interpolation), with the highest percentiles computed 
# on the basis of how many realizations are provided by the modelled analysis/forecasts. Separate climatologies are computed for year and seasonal (i.e. DJF, MAM, JJA, 
# SON) climatologies. 
# Code runtime: Depends on the number of datasets processed, but it is on the order of 10 minutes for all datasets.
# Note: this script must be run on the HPC because it is memory demanding.

# DESCRIPTION OF INPUT PARAMETERS
# YearS (number, in YYYY format): start year to consider.
# YearF (number, in YYYY format): final year to consider.
# Acc (number, in hours): rainfall accumulation period.
# SystemFC_list (list of string): list of forecasting systems to consider.
# MinDays_Perc_list (list of number, from 0 to 1): list of percentages of minimum n. of days over the considered period with valid observations to compute the climatologies.
# NameOBS_list (list of strings): list of the names of the observations to quality check.
# Coeff_Grid2Point_list (list of integer number): list of coefficients used to compare CPC's gridded rainfall values with  STVL's point rainfall observations. 
# Git_repo (string): path of local github repository.
# DirIN_Climate_OBS (string): relative path for the input directory containing the observational climatologies.
# DirIN_FC (string): relative path for the input directory containing the raw analysis/forecasts.
# DirOUT_Climate_FC (string): relative path for the output directory containing the modelled climatologies.

# INPUT PARAMETERS
YearS = int(sys.argv[1])
YearF = int(sys.argv[2])
Acc = 24
SystemFC_list = sys.argv[3].split(',')
MinDays_Perc_list = [0.75]
NameOBS_list = ["08_AlignOBS_CleanSTVL"]
Coeff_Grid2Point_list = [20]
Git_repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/ecPoint_Climate"
DirIN_Climate_OBS = "Data/Compute/09_Climate_OBS"
DirIN_FC = "Data/Compute/10_Extract_RainfallFC_atOBS"
DirOUT_Climate_FC = "Data/Compute/11_ClimateFC_atOBS"
#############################################################################################################################################


# Costum functions

########################################
# Compute and save distribution of percentiles  # 
########################################
def distribution_percentiles(YearS, YearF, PercYear, PercSeason, DirIN_Climate_OBS, DirIN_FC, DirOUT_Climate_FC):
      
      Season_list = ["Year", "DJF", "MAM", "JJA", "SON"]
      for Season in Season_list:
            
            print(" - Computing percentiles for " + Season)
            
            # Reading and saving the metadata (i.e. station id/lat/lon) for the considered point observational climatologies         
            stn_lats = np.load(DirIN_Climate_OBS + "/Stn_lats_" + Season + ".npy")
            stn_lons = np.load(DirIN_Climate_OBS + "/Stn_lons_" + Season + ".npy")
            stn_ids = np.load(DirIN_Climate_OBS + "/Stn_ids_" + Season + ".npy")
            np.save(DirOUT_Climate_FC + "/Stn_ids_" + Season + ".npy", stn_ids)
            np.save(DirOUT_Climate_FC + "/Stn_lats_" + Season + ".npy", stn_lats)
            np.save(DirOUT_Climate_FC + "/Stn_lons_" + Season + ".npy", stn_lons)

            # Reading the indipendent rainfall realizations for the period under consideration
            print("     - Reading the indipendent rainfall realizations for year: " + str(YearS))
            tp = np.load(DirIN_FC + "/tp_" + Season + "_" + str(YearS) + ".npy")
            for Year in range (YearS+1,YearF+1):
                        print("     - Reading the indipendent rainfall realizations for year: " + str(Year))
                        tp_raw = np.hstack((tp, np.load(DirIN_FC + "/tp_" + Season + "_" + str(Year) + ".npy")))

            # Adjusting the dataset to not have the minimum and the maximum values in "align_obs" assigned to the 0th and 100th percentile
            # Note: If the whole dataset for a station contains only nan, a warning message will appear on the screen, and the minimum or maximum
            # value that will be associated to that station will be a nan. This issue does not stop the computations or compromise the results. This 
            # happens mainly for the CPC dataset where a point station on the coast my be seen by CPC in the sea where there is no data available.
            print("     - Adjusting the dataset to not have the minimum and the maximum values in the observational dataset assigned to the 0th and 100th percentile...")
            min_tp = np.nanmin(tp_raw, axis=1)
            max_tp = np.nanmax(tp_raw, axis=1)
            tp = np.column_stack((min_tp, tp_raw, max_tp))

            # Computing the percentiles for the year/seasonal climatologies
            print("     - Computing the percentiles for the year/seasonal climatologies")
            if Season == "Year":
                  Perc = PercYear
            else:
                  Perc = PercSeason
            climate = np.transpose(np.around(np.float32(np.nanpercentile(tp, Perc, axis=1, interpolation="linear").astype(float)), decimals=1))

            # Saving the year/seasonal climatologies and their correspondent metadata
            print("     - Saving the year/seasonal climatologies and their correspondent metadata")
            np.save(DirOUT_Climate_FC + "/Climate_" + Season + ".npy", climate)

      # Saving the percentiles computed for the year/seasonal climatologies
      np.save(DirOUT_Climate_FC + "/Percentiles_Year.npy", PercYear)
      np.save(DirOUT_Climate_FC + "/Percentiles_Season.npy", PercSeason)

#############################################################################################################################################


# Computing the modelled climatologies
for MinDays_Perc in MinDays_Perc_list:

      for NameOBS in NameOBS_list:

            if (NameOBS == "06_AlignOBS_Combine_Years_RawSTVL") or (NameOBS == "07_AlignOBS_Extract_GridCPC"):

                  for SystemFC in SystemFC_list:
                        
                        print(" ")
                        print("Computing modelled (" + SystemFC + ") climatologies at stations for "+ NameOBS + " with a minimum of " + str(int(MinDays_Perc*100)) + "% of days over the considered period with valid observations")

                        # Definition of the percentiles to compute for different forecasting system
                        if SystemFC == "HRES_46r1":
                              PercYear = np.concatenate([np.arange(0,100), np.array([99.5, 99.8, 99.9, 99.95])])
                              PercSeason = np.concatenate([np.arange(0,100), np.array([99.5, 99.8])])
                        elif SystemFC == "Reforecasts_46r1":
                              PercYear = np.concatenate([np.arange(0,100), np.array([99.5, 99.8, 99.9, 99.95, 99.98, 99.99, 99.995])])
                              PercSeason = np.concatenate([np.arange(0,100), np.array([99.5, 99.8, 99.9, 99.95, 99.98])])
                        elif SystemFC == "ERA5_ShortRange":
                              PercYear = np.concatenate([np.arange(0,100), np.array([99.5, 99.8, 99.9, 99.95, 99.98])])
                              PercSeason = np.concatenate([np.arange(0,100), np.array([99.5, 99.8, 99.9])])
                        elif SystemFC == "ERA5_EDA_ShortRange":
                              PercYear = np.concatenate([np.arange(0,100), np.array([99.5, 99.8, 99.9, 99.95, 99.98, 99.99, 99.995, 99.998])])
                              PercSeason = np.concatenate([np.arange(0,100), np.array([99.5, 99.8, 99.9, 99.95, 99.98, 99.99])])
                        elif SystemFC == "ERA5_LongRange":
                              PercYear = np.concatenate([np.arange(0,100), np.array([99.5, 99.8, 99.9, 99.95, 99.98, 99.99, 99.995, 99.998])])
                              PercSeason = np.concatenate([np.arange(0,100), np.array([99.5, 99.8, 99.9, 99.95, 99.98, 99.99])])
                        elif SystemFC == "ERA5_EDA_LongRange":
                              PercYear = np.concatenate([np.arange(0,100), np.array([99.5, 99.8, 99.9, 99.95, 99.98, 99.99, 99.995, 99.998])])
                              PercSeason = np.concatenate([np.arange(0,100), np.array([99.5, 99.8, 99.9, 99.95, 99.98, 99.99])])
                        elif SystemFC == "ERA5_ecPoint/Grid_BC_VALS":
                              PercYear = np.concatenate([np.arange(0,100), np.array([99.5, 99.8, 99.9, 99.95, 99.98])])
                              PercSeason = np.concatenate([np.arange(0,100), np.array([99.5, 99.8, 99.9])])
                        elif SystemFC == "ERA5_ecPoint/Pt_BC_PERC":
                              PercYear = np.concatenate([np.arange(0,100), np.array([99.5, 99.8, 99.9, 99.95, 99.98, 99.99, 99.995, 99.998, 99.999, 99.9995, 99.9998])])
                              PercSeason = np.concatenate([np.arange(0,100), np.array([99.5, 99.8, 99.9, 99.95, 99.98, 99.99, 99.995, 99.998, 99.999])])

                        # Setting the input directory for the observational climatologies
                        MainDirIN_Climate_OBS = Git_repo + "/" + DirIN_Climate_OBS + "/MinDays_Perc" + str(int(MinDays_Perc*100)) + "/" + NameOBS
                        
                        # Computing and saving the modelled rainfall climatologies (i.e. the distribution of percentiles computed from the independent rainfall realizations)
                        MainDirIN_FC = Git_repo + "/" + DirIN_FC + "/" + SystemFC + "/MinDays_Perc" + str(int(MinDays_Perc*100)) + "/" + NameOBS
                        MainDirOUT_Climate_FC = Git_repo + "/" + DirOUT_Climate_FC + "/" + SystemFC + "/MinDays_Perc" + str(int(MinDays_Perc*100)) + "/" + NameOBS
                        if not exists(MainDirOUT_Climate_FC):
                              os.makedirs(MainDirOUT_Climate_FC)
                        distribution_percentiles(YearS, YearF, PercYear, PercSeason, MainDirIN_Climate_OBS, MainDirIN_FC, MainDirOUT_Climate_FC)

            elif NameOBS == "08_AlignOBS_CleanSTVL":

                  for Coeff_Grid2Point in Coeff_Grid2Point_list:
                        
                        for SystemFC in SystemFC_list:
                              
                              print(" ")
                              print("Computing modelled (" + SystemFC + ") climatologies at stations for "+ NameOBS + " (Coeff_Grid2Point=" + str(Coeff_Grid2Point) + ") with a minimum of " + str(int(MinDays_Perc*100)) + "% of days over the considered period with valid observations")

                              # Definition of the percentiles to compute for different forecasting system
                              if SystemFC == "HRES_46r1":
                                    PercYear = np.concatenate([np.arange(0,100), np.array([99.5, 99.8, 99.9, 99.95])])
                                    PercSeason = np.concatenate([np.arange(0,100), np.array([99.5, 99.8])])
                              elif SystemFC == "Reforecasts_46r1":
                                    PercYear = np.concatenate([np.arange(0,100), np.array([99.5, 99.8, 99.9, 99.95, 99.98, 99.99, 99.995])])
                                    PercSeason = np.concatenate([np.arange(0,100), np.array([99.5, 99.8, 99.9, 99.95, 99.98])])
                              elif SystemFC == "ERA5_ShortRange":
                                    PercYear = np.concatenate([np.arange(0,100), np.array([99.5, 99.8, 99.9, 99.95, 99.98])])
                                    PercSeason = np.concatenate([np.arange(0,100), np.array([99.5, 99.8, 99.9])])
                              elif SystemFC == "ERA5_EDA_ShortRange":
                                    PercYear = np.concatenate([np.arange(0,100), np.array([99.5, 99.8, 99.9, 99.95, 99.98, 99.99, 99.995, 99.998])])
                                    PercSeason = np.concatenate([np.arange(0,100), np.array([99.5, 99.8, 99.9, 99.95, 99.98, 99.99])])
                              elif SystemFC == "ERA5_LongRange":
                                    PercYear = np.concatenate([np.arange(0,100), np.array([99.5, 99.8, 99.9, 99.95, 99.98, 99.99, 99.995, 99.998])])
                                    PercSeason = np.concatenate([np.arange(0,100), np.array([99.5, 99.8, 99.9, 99.95, 99.98, 99.99])])
                              elif SystemFC == "ERA5_EDA_LongRange":
                                    PercYear = np.concatenate([np.arange(0,100), np.array([99.5, 99.8, 99.9, 99.95, 99.98, 99.99, 99.995, 99.998])])
                                    PercSeason = np.concatenate([np.arange(0,100), np.array([99.5, 99.8, 99.9, 99.95, 99.98, 99.99])])
                              elif SystemFC == "ERA5_ecPoint/Grid_BC_VALS":
                                    PercYear = np.concatenate([np.arange(0,100), np.array([99.5, 99.8, 99.9, 99.95, 99.98])])
                                    PercSeason = np.concatenate([np.arange(0,100), np.array([99.5, 99.8, 99.9])])
                              elif SystemFC == "ERA5_ecPoint/Pt_BC_PERC":
                                    PercYear = np.concatenate([np.arange(0,100), np.array([99.5, 99.8, 99.9, 99.95, 99.98, 99.99, 99.995, 99.998, 99.999, 99.9995, 99.9998])])
                                    PercSeason = np.concatenate([np.arange(0,100), np.array([99.5, 99.8, 99.9, 99.95, 99.98, 99.99, 99.995, 99.998, 99.999])])

                              # Setting the input directory for the observational climatologies
                              MainDirIN_Climate_OBS = Git_repo + "/" + DirIN_Climate_OBS + "/MinDays_Perc" + str(int(MinDays_Perc*100)) + "/" + NameOBS + "/Coeff_Grid2Point_" + str(Coeff_Grid2Point)
                  
                              # Computing and saving the modelled rainfall climatologies (i.e. the distribution of percentiles computed from the independent rainfall realizations)
                              MainDirIN_FC = Git_repo + "/" + DirIN_FC + "/" + SystemFC + "/MinDays_Perc" + str(int(MinDays_Perc*100)) + "/" + NameOBS + "/Coeff_Grid2Point_" + str(Coeff_Grid2Point)
                              MainDirOUT_Climate_FC = Git_repo + "/" + DirOUT_Climate_FC + "/" + SystemFC + "/MinDays_Perc" + str(int(MinDays_Perc*100)) + "/" + NameOBS + "/Coeff_Grid2Point_" + str(Coeff_Grid2Point)
                              if not exists(MainDirOUT_Climate_FC):
                                    os.makedirs(MainDirOUT_Climate_FC)
                              distribution_percentiles(YearS, YearF, PercYear, PercSeason, MainDirIN_Climate_OBS, MainDirIN_FC, MainDirOUT_Climate_FC)
