import os
from os.path import exists
import numpy as np
from scipy.stats import anderson_ksamp

############################################################################################################################################
# CODE DESCRIPTION
# 13_Compute_Statistic_AD.py computes the Anderson-Darling statistic between the observational and modelled climatological distributions.
# Code runtime: negligible.

# DESCRIPTION OF INPUT PARAMETERS
# Acc (number, in hours): rainfall accumulation period.
# SystemFC_list (list of string): list of forecasting systems to consider.
# MinDays_Perc_list (list of number, from 0 to 1): list of percentages of minimum n. of days over the considered period with valid observations to compute the climatologies.
# NameOBS_list (list of strings): list of the names of the observations to quality check
# Coeff_Grid2Point_list (list of integer number): list of coefficients used to compare CPC's gridded rainfall values with  STVL's point rainfall observations. 
# Git_repo (string): path of local github repository.
# DirIN_Climate_OBS (string): relative path for the input directory containing the observational climatologies.
# DirIN_FC (string): relative path for the input directory containing the raw analysis/forecasts.
# DirOUT_Climate_FC (string): relative path for the output directory containing the modelled climatologies.

# INPUT PARAMETERS
Acc = 24
SystemFC_list = ["Reforecasts_46r1", "ERA5_ShortRange", "ERA5_EDA_ShortRange", "ERA5_LongRange", "ERA5_EDA_LongRange", "ERA5_ecPoint/Grid_BC_VALS", "ERA5_ecPoint/Pt_BC_PERC"]
MinDays_Perc_list = [0.75]
NameOBS_list = ["08_AlignOBS_CleanSTVL"]
Coeff_Grid2Point_list = [20]
Git_repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/ecPoint_Climate"
DirIN_Climate_OBS = "Data/Compute/09_Climate_OBS"
DirIN_Climate_FC = "Data/Compute/11_ClimateFC_atOBS"
DirOUT = "Data/Compute/13_Statistic_AD"
############################################################################################################################################

# Costum functions

######################################################
# Compute and save the Anderson-Darling Statistic for k-samples # 
######################################################
def statisticAD(DirIN_OBS, DirIN_FC, DirOUT):

      # Notes:
      # The Anderson-Darling test for k-samples tests the null hypothesis that k-samples are drawn from the same population without having to specify the distribution function of that population. 
      #     1. If the Anderson-Darling statistic is bigger than the critical values, this means that the test results are significant at every significance level.
      #         Therefore, we would reject the null hypothesis of the test no matter which significance level we choose to use. 
      #         Thus, we have sufficient evidence to say that the samples are not drawn from the same population.
      #     2. If the Anderson-Darling statistic is smaller than the critical values, this means that the test results are not significant at any significance level.
      #         Therefore, we would not reject the null hypothesis of the test.
      #         Thus, we don’t have sufficient evidence to say that the samples are not drawn from the same population.

      Season_list = ["Year", "DJF", "MAM", "JJA", "SON"]

      for Season in Season_list:
            
            print(" - Computing the Anderson-Darling statistic for k-samples for the " + Season + " climatology")

            # Reading the observational/modelled climatologies and their locations in lat/lon coordinates
            climate_obs = np.load(DirIN_OBS + "/Climate_" + Season + ".npy")
            climate_fc = np.load(DirIN_FC + "/Climate_" + Season + ".npy")
            lats = np.load(DirIN_OBS + "/Stn_lats_" + Season + ".npy")
            lons = np.load(DirIN_OBS + "/Stn_lons_" + Season + ".npy")
            num_stn = climate_obs.shape[0]
            num_perc = climate_obs.shape[1]
            climate_fc = climate_fc[:,0:num_perc] # to match the number of percentiles between the observational and modelled climatologies
            
            # Computing the Anderson-Darling statistic for k-samples
            StatisticAD = np.empty([num_stn,1]) * np.nan
            CriticalVal = np.empty([num_stn,1]) * np.nan
            for ind_stn in range(num_stn):
                  climate_obs_temp = climate_obs[ind_stn,:]
                  climate_fc_temp = climate_fc[ind_stn,:]
                  if np.sum(climate_obs_temp) != 0 and np.sum(climate_fc_temp) != 0:
                        TestAD = anderson_ksamp([climate_obs_temp, climate_fc_temp])
                        StatisticAD[ind_stn] = TestAD[0]
                        CriticalVal[ind_stn] = TestAD[1][-1] # for significance level 0.1%.

            # Saving the Anderson-Darling statistic for k-samples
            np.save(DirOUT + "/StatisticAD_" + Season + ".npy", StatisticAD)
            np.save(DirOUT + "/CriticalVal_" + Season + ".npy", CriticalVal)
            np.save(DirOUT + "/Stn_lats_" + Season + ".npy", lats)      
            np.save(DirOUT + "/Stn_lons_" + Season + ".npy", lons)

######################################################################################################################################################


for MinDays_Perc in MinDays_Perc_list:

      for NameOBS in NameOBS_list:

            if (NameOBS == "06_AlignOBS_Combine_Years_RawSTVL") or (NameOBS == "07_AlignOBS_Extract_GridCPC"):

                  for SystemFC in SystemFC_list:
                        
                        print(" ")
                        print("Computing the Anderson-Darling statistic between the observational and modelled (" + SystemFC + ") climatological distributions at stations for "+ NameOBS + " with a minimum of " + str(int(MinDays_Perc*100)) + "% of days over the considered period with valid observations")

                        # Computing and saving the modelled rainfall climatologies (i.e. the distribution of percentiles computed from the independent rainfall realizations)
                        MainDirIN_OBS = Git_repo + "/" + DirIN_Climate_OBS + "/MinDays_Perc" + str(int(MinDays_Perc*100)) + "/" + NameOBS
                        MainDirIN_FC = Git_repo + "/" + DirIN_Climate_FC + "/" + SystemFC + "/MinDays_Perc" + str(int(MinDays_Perc*100)) + "/" + NameOBS
                        MainDirOUT = Git_repo + "/" + DirOUT + "/" + SystemFC + "/MinDays_Perc" + str(int(MinDays_Perc*100)) + "/" + NameOBS
                        if not exists(MainDirOUT):
                              os.makedirs(MainDirOUT)
                        
                        # Computing the Anderson-Darling statistic for k-samples
                        statisticAD(MainDirIN_OBS, MainDirIN_FC, MainDirOUT)

            elif NameOBS == "08_AlignOBS_CleanSTVL":

                  for Coeff_Grid2Point in Coeff_Grid2Point_list:
                        
                        for SystemFC in SystemFC_list:
                              
                              print(" ")
                              print("Computing the Anderson-Darling statistic between the observational and modelled (" + SystemFC + ") climatological distributions at stations for "+ NameOBS + " (Coeff_Grid2Point=" + str(Coeff_Grid2Point) + ") with a minimum of " + str(int(MinDays_Perc*100)) + "% of days over the considered period with valid observations")

                              # Computing and saving the modelled rainfall climatologies (i.e. the distribution of percentiles computed from the independent rainfall realizations)
                              MainDirIN_OBS = Git_repo + "/" + DirIN_Climate_OBS + "/MinDays_Perc" + str(int(MinDays_Perc*100)) + "/" + NameOBS + "/Coeff_Grid2Point_" + str(Coeff_Grid2Point)
                              MainDirIN_FC = Git_repo + "/" + DirIN_Climate_FC + "/" + SystemFC + "/MinDays_Perc" + str(int(MinDays_Perc*100)) + "/" + NameOBS + "/Coeff_Grid2Point_" + str(Coeff_Grid2Point)
                              MainDirOUT = Git_repo + "/" + DirOUT + "/" + SystemFC + "/MinDays_Perc" + str(int(MinDays_Perc*100)) + "/" + NameOBS + "/Coeff_Grid2Point_" + str(Coeff_Grid2Point)
                              if not exists(MainDirOUT):
                                    os.makedirs(MainDirOUT)
                              
                              # Computing the Anderson-Darling statistic for k-samples
                              statisticAD(MainDirIN_OBS, MainDirIN_FC, MainDirOUT)
