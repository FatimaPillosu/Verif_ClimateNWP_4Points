import os
import numpy as np
import matplotlib.pyplot as plt

##########################################################################################################
# CODE DESCRIPTION
# 23_Plot_ECDF_Diff_Piechart.py plots piecharts for the mean areal separation between obs & nwp ECDFs. 
# Code runtime: ~ 1 minute.

# DESCRIPTION OF INPUT PARAMETERS
# YearS (number, in YYYY format): start year to consider.
# YearF (number, in YYYY format): final year to consider.
# Acc (number, in hours): rainfall accumulation period.
# MinDays_Perc (float, from 0 to 1): % of min n. of days with valid obs at each location.
# MaxPerc (integer or float, from 0 to 100 - not included): max percentile considered when sampling the obs & nwp ECDFs. 
# SystemNWP_list (list of strings): list of NWP model climatologies.
# Domain_Coord_list (list of floats): list of coordinates of the domain of interest.
# Domain_Name_list (list of strings): list of the names of the domain of interest.
# Git_Repo (string): path of local github repository.
# DirIN (string): relative path for the directory containing the differences between obs & nwp ECDFs.
# DirOUT (string): relative path for the directory containing the piecharts for the mean areal separation between obs & nwp ECDFs.

# INPUT PARAMETERS
YearS = 2000
YearF = 2019
Acc = 24
MinDays_Perc = 0.75
MaxPerc = 99
SystemNWP_list = ["Reforecasts/ECMWF_46r1", "Reanalysis/ERA5_EDA", "Reanalysis/ERA5", "Reanalysis/ERA5_ecPoint"]
Domain_Coord_list = [ [90,-170,15,-50], [15, -100, -60, -30], [90, -30, 30, 60], [30,-30,-40,60], [90, 60, 5, 180], [5, 60, -60, 180] ]
Domain_Name_list = ["North_America", "South_America", "Europe_Mediterranean", "Africa", "Asia", "Oceania"]
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_ClimateNWP_4Points"
DirIN = "Data/Compute/21_ECDF_diff"
DirOUT = "Data/Plot/23_ECDF_Diff_Piechart"
##########################################################################################################


# Plotting the piecharts for the mean areal separation between obs & nwp ECDFs
for SystemNWP in SystemNWP_list:
      
      print()
      print("Plotting piecharts for the mean areal separation between obs & nwp ECDFs for " + SystemNWP)
      
      # Reading the ECDF differences for specific nwp models
      MainDirIN = Git_Repo + "/" + DirIN + "/MinDays_Perc_" + str(MinDays_Perc*100) + "/MaxPerc_" + str(MaxPerc) + "/" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF) + "/" + SystemNWP
      tp_obs_mean = np.load(MainDirIN + "/tp_obs_mean.npy")
      perc_diff = np.load(MainDirIN + "/ECDF_Diff.npy")
      perc_list = np.load(MainDirIN + "/Perc_List.npy")
      lats = np.load(MainDirIN + "/" + "Stn_lats.npy")
      lons = np.load(MainDirIN + "/" + "Stn_lons.npy")

      # Computing the mean areal separation between obs & nwp ECDFs expressed as percentage of the mean obs rainfall
      ECDF_diff_mean = ( np.nanmean( np.absolute(perc_diff), axis=1 ) / tp_obs_mean ) * 100

      #Plotting the piecharts for the considered domains
      for ind_domain in np.arange(len(Domain_Name_list)):

            Domain_Name = Domain_Name_list[ind_domain]
            Domain_Coord = Domain_Coord_list[ind_domain]
            
            # Selecting the domain to consider
            ind_gp_domain = np.where( (lats < Domain_Coord[0]) & (lats > Domain_Coord[2]) & (lons > Domain_Coord[1]) & (lons < Domain_Coord[3]) )
            ECDF_diff_mean_domain = ECDF_diff_mean[ind_gp_domain]

            # Creating the piecharts
            fig,ax = plt.subplots()
            a = np.where(ECDF_diff_mean_domain < 10)[0].shape[0]
            b = np.where( (ECDF_diff_mean_domain >= 10) & (ECDF_diff_mean_domain < 30) )[0].shape[0]
            c = np.where( (ECDF_diff_mean_domain >= 30) & (ECDF_diff_mean_domain < 50) )[0].shape[0]
            d = np.where( (ECDF_diff_mean_domain >= 50) & (ECDF_diff_mean_domain < 100) )[0].shape[0]
            e = np.where(ECDF_diff_mean_domain >= 100)[0].shape[0]
            sizes = [a, b, c, d, e]
            colors = ["#000000", "#f9df4d", "#6b6bf7", "#ff007f", "#7fff00"]
            ax.pie(sizes, colors=colors, startangle=0)
            plt.axis("equal")

            # Print on screen the percentage for each area category
            print(" - Percentage for each area category in " + Domain_Name)
            print("     a: " + str(a/ECDF_diff_mean.shape[0] * 100))
            print("     b: " + str(b/ECDF_diff_mean.shape[0] * 100))
            print("     c: " + str(c/ECDF_diff_mean.shape[0] * 100))
            print("     d: " + str(d/ECDF_diff_mean.shape[0] * 100))
            print("     e: " + str(e/ECDF_diff_mean.shape[0] * 100))

            # Saving the piecharts
            MainDirOUT = Git_Repo + "/" + DirOUT + "/MinDays_Perc_" + str(MinDays_Perc*100) + "/MaxPerc_" + str(MaxPerc) + "/" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF) + "/" + SystemNWP
            if not os.path.exists(MainDirOUT):
                  os.makedirs(MainDirOUT)
            FileOUT = "ECDF_Diff_" + Domain_Name + ".png"
            fig.savefig(MainDirOUT + "/" + FileOUT)
            plt.close()