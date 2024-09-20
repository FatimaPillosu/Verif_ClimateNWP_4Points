import os
import numpy as np
import matplotlib.pyplot as plt

#######################################################################################################
# CODE DESCRIPTION
# 05_Plot_Statistic_AD_piecharts.py plots the Anderson-Darling statistic between the observational and the NWP modelled
# climatology distributions.
# Note:
# The Anderson-Darling test for k-samples tests the null hypothesis that k-samples are drawn from the same population 
# without having to specify the distribution function of that population. 
#     1. If the Anderson-Darling statistic is bigger than the critical values, this means that the test results are significant at 
#         every significance level. Therefore, we would reject the null hypothesis of the test no matter which significance 
#         level we choose to use. Thus, we have sufficient evidence to say that the samples are not drawn from the same
#         population.
#     2. If the Anderson-Darling statistic is smaller than the critical values, this means that the test results are not 
#         significant at any significance level. Therefore, we would not reject the null hypothesis of the test. Thus, we don’t 
#         have sufficient evidence to say that the samples are not drawn from the same population.
# Code runtime: ~ 1 minute.

# DESCRIPTION OF INPUT PARAMETERS
# YearS (number, in YYYY format): start year to consider.
# YearF (number, in YYYY format): final year to consider.
# Acc (number, in hours): rainfall accumulation period.
# MinDays_Perc (float, from 0 to 1): % of min n. of days with valid obs at each location.
# NumPer (integer): number of permutations for the Anderson-Darling test statistic.
# SystemNWP_list (list of strings): list of NWP model climatologies.
# Domain_Coord_list (list of floats): list of coordinates of the domain of interest.
# Domain_Name_list (list of strings): list of the names of the domain of interest.
# Git_Repo (string): path of local github repository.
# DirIN (string): relative path for the directory containing the values of the AD statistic.
# DirOUT (string): relative path for the directory containing the AD statistic.

# INPUT PARAMETERS
YearS = 2000
YearF = 2019
Acc = 24
MinDays_Perc = 0.75
NumPer = 0
SystemNWP_list = ["Reforecasts/ECMWF_46r1", "Reanalysis/ERA5_EDA", "Reanalysis/ERA5", "Reanalysis/ERA5_ecPoint"]
Domain_Coord_list = [ [90,-170,15,-50], [15, -100, -60, -30], [90, -30, 30, 60], [30,-30,-40,60], [90, 60, 5, 180], [5, 60, -60, 180] ]
Domain_Name_list = ["North_America", "South_America", "Europe_Mediterranean", "Africa", "Asia", "Oceania"]
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_ClimateNWP_4Points"
DirIN = "Data/Compute/21_Statistic_AD"
DirOUT = "Data/Plot/23_Statistic_AD_piecharts"
#######################################################################################################

# Plotting the Anderson-Darling statistic for different NWP modelled climatologies
print()
print("Plotting the pie-charts for the Anderson-Darling statistic for the NWP modelled climatology: ")
for SystemNWP in SystemNWP_list:
      
      print(" - " + SystemNWP)

      # Reading the considered NWP modelled climatology
      MainDirIN = Git_Repo + "/" + DirIN + "/MinDays_Perc_" + str(MinDays_Perc*100) + "/" + "NumPer_" + f'{NumPer:03d}' + "/" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF) + "/" + SystemNWP
      Stat_AD = np.load(MainDirIN + "/StatisticAD.npy")
      Crit_Val = np.load(MainDirIN + "/CriticalVal.npy")
      lats = np.load(MainDirIN + "/" + "Stn_lats.npy")
      lons = np.load(MainDirIN + "/" + "Stn_lons.npy")

      # Defining when to reject or not-reject the null hypothesis of the Anderson-Darling test
      test_AD = (Stat_AD < Crit_Val) * 1 # the value of 1 is given to those locations where the modelled climatology is representative of the observational climatology

      #Computing the pie-charts for each considered domain
      for ind_domain in np.arange(len(Domain_Name_list)):

            Domain_Name = Domain_Name_list[ind_domain]
            Domain_Coord = Domain_Coord_list[ind_domain]
            
            # Selecting the domain to consider
            ind_gp_domain = np.where( (lats < Domain_Coord[0]) & (lats > Domain_Coord[2]) & (lons > Domain_Coord[1]) & (lons < Domain_Coord[3]) )
            test_AD_domain = test_AD[ind_gp_domain]

            # Creating the pie-charts
            fig,ax = plt.subplots()
            repr = np.where(test_AD_domain == 1)[0].shape[0]
            no_repr = np.where(test_AD_domain == 0)[0].shape[0]
            sizes = [repr, no_repr]
            colors = ["dodgerblue", "deeppink"]
            ax.pie(sizes, colors=colors, startangle=0, autopct='%1.1f%%')
            plt.axis('equal')

            # Saving the pie-charts
            MainDirOUT = Git_Repo + "/" + DirOUT + "/MinDays_Perc_" + str(MinDays_Perc*100) + "/" + "NumPer_" + f'{NumPer:03d}' + "/" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF) + "/" + SystemNWP
            if not os.path.exists(MainDirOUT):
                  os.makedirs(MainDirOUT)
            FileOUT = Domain_Name + ".png"
            fig.savefig(MainDirOUT + "/" + FileOUT)
            plt.close()