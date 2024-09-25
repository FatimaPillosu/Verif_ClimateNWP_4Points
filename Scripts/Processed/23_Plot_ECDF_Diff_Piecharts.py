import os
import numpy as np
import matplotlib.pyplot as plt

###############################################################################################################
# CODE DESCRIPTION
# 23_Plot_ECDF_Diff_Piecharts.py plots the piecharts for the mean areal separation between the ECDF of the obs and nwp rainfall 
# distributions.
# Code runtime: ~ 1 minute.

# DESCRIPTION OF INPUT PARAMETERS
# YearS (number, in YYYY format): start year to consider.
# YearF (number, in YYYY format): final year to consider.
# Acc (number, in hours): rainfall accumulation period.
# MinDays_Perc (float, from 0 to 1): % of min n. of days with valid obs at each location.
# MaxPerc (integer or float, from 0 to 100 - not included): max percentile considered when sampling the obs and nwp rainfall realization.
# SystemNWP_list (list of strings): list of NWP model climatologies.
# Domain_Coord_list (list of floats): list of coordinates of the domain of interest.
# Domain_Name_list (list of strings): list of the names of the domain of interest.
# Git_Repo (string): path of local github repository.
# DirIN (string): relative path for the directory containing the quantile differences for the NWP modelled rainfall realizations.
# DirOUT (string): relative path for the directory containing piecharts for different NWP modelled rainfall realizations.

# INPUT PARAMETERS
YearS = 2000
YearF = 2019
Acc = 24
MinDays_Perc = 0.75
MaxPerc = 99.97
SystemNWP_list = ["Reforecasts/ECMWF_46r1", "Reanalysis/ERA5_EDA", "Reanalysis/ERA5", "Reanalysis/ERA5_ecPoint"]
Domain_Coord_list = [ [90,-170,15,-50], [15, -100, -60, -30], [90, -30, 30, 60], [30,-30,-40,60], [90, 60, 5, 180], [5, 60, -60, 180] ]
Domain_Name_list = ["North_America", "South_America", "Europe_Mediterranean", "Africa", "Asia", "Oceania"]
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_ClimateNWP_4Points"
DirIN = "Data/Compute/21_Empirical_ECDF_diff"
DirOUT = "Data/Plot/23_ECDF_Diff_Piecharts"
###############################################################################################################


# Plotting the piecharts for the mean areal separation between the ECDF of the obs and nwp rainfall distributions
for SystemNWP in SystemNWP_list:
      
      print()
      print("Plotting the piecharts for the mean areal separation between the ECDF of the obs and nwp rainfall distributions for " + SystemNWP)
      
      # Reading the ECDF differences for specific nwp models
      MainDirIN = Git_Repo + "/" + DirIN + "/MinDays_Perc_" + str(MinDays_Perc*100) + "/MaxPerc_" + str(MaxPerc) + "/" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF) + "/" + SystemNWP
      tp_obs_mean = np.load(MainDirIN + "/tp_obs_mean.npy")
      perc_diff = np.load(MainDirIN + "/ECDF_Diff.npy")
      perc_list = np.load(MainDirIN + "/Perc_List.npy")
      lats = np.load(MainDirIN + "/" + "Stn_lats.npy")
      lons = np.load(MainDirIN + "/" + "Stn_lons.npy")

      # Computing the mean areal separation between the ECDF of the obs and nwp rainfall distributions (excluding the tail's distribution)
      # expressed as percentage of the mean obs rainfall
      ECDF_diff_mean_notail = np.nanmean(np.absolute(perc_diff[:, np.where(perc_list<90)[0]]), axis=1) / tp_obs_mean
      
      # Computing the mean areal separation between the ECDF of the obs and nwp rainfall distributions (only tail's distribution)
      # expressed as percentage of the mean obs rainfall
      ECDF_diff_mean_tail = np.nanmean(np.absolute(perc_diff[:, np.where(perc_list>=90)[0]]), axis=1) / tp_obs_mean

      #Computing the pie-charts for each considered domains
      for ind_domain in np.arange(len(Domain_Name_list)):

            Domain_Name = Domain_Name_list[ind_domain]
            Domain_Coord = Domain_Coord_list[ind_domain]
            
            # Selecting the domain to consider
            ind_gp_domain = np.where( (lats < Domain_Coord[0]) & (lats > Domain_Coord[2]) & (lons > Domain_Coord[1]) & (lons < Domain_Coord[3]) )
            ECDF_diff_mean_notail_domain = ECDF_diff_mean_notail[ind_gp_domain]
            ECDF_diff_mean_tail_domain = ECDF_diff_mean_tail[ind_gp_domain]

            # Creating the pie-charts between the ECDF of the obs and nwp rainfall distributions (excluding the tail's distribution)
            fig,ax = plt.subplots()
            a = np.where(ECDF_diff_mean_notail_domain < 0.1)[0].shape[0]
            b = np.where( (ECDF_diff_mean_notail_domain >= 0.1) & (ECDF_diff_mean_notail_domain < 0.3) )[0].shape[0]
            c = np.where( (ECDF_diff_mean_notail_domain >= 0.3) & (ECDF_diff_mean_notail_domain < 0.5) )[0].shape[0]
            d = np.where( (ECDF_diff_mean_notail_domain >= 0.5) & (ECDF_diff_mean_notail_domain < 1) )[0].shape[0]
            e = np.where(ECDF_diff_mean_notail_domain >= 1)[0].shape[0]
            sizes = [a, b, c, d, e]
            colors = ["#000000", "#f9df4d", "#6b6bf7", "#ff007f", "#7fff00"]
            ax.pie(sizes, colors=colors, startangle=0)
            plt.axis("equal")

            # Print on screen the area difference between the ECDF of the obs and nwp rainfall distributions (excluding the tail's distribution)
            print(" - Percentage of mean ECDF separation between obs and nwp rainfall distributions for " + Domain_Name)
            print("     a: " + str(a/ECDF_diff_mean_notail.shape[0] * 100))
            print("     b: " + str(b/ECDF_diff_mean_notail.shape[0] * 100))
            print("     c: " + str(c/ECDF_diff_mean_notail.shape[0] * 100))
            print("     d: " + str(d/ECDF_diff_mean_notail.shape[0] * 100))
            print("     e: " + str(e/ECDF_diff_mean_notail.shape[0] * 100))

            # Saving the pie-charts between the ECDF of the obs and nwp rainfall distributions (excluding the tail's distribution)
            MainDirOUT = Git_Repo + "/" + DirOUT + "/MinDays_Perc_" + str(MinDays_Perc*100) + "/MaxPerc_" + str(MaxPerc) + "/" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF) + "/" + SystemNWP
            if not os.path.exists(MainDirOUT):
                  os.makedirs(MainDirOUT)
            FileOUT = "ECDF_Diff_NoTail_" + Domain_Name + ".png"
            fig.savefig(MainDirOUT + "/" + FileOUT)
            plt.close()

            # Creating the pie-charts between the ECDF of the obs and nwp rainfall distributions (only the tail's distribution)
            fig,ax = plt.subplots()
            a = np.where(ECDF_diff_mean_tail_domain < 0.1)[0].shape[0]
            b = np.where( (ECDF_diff_mean_tail_domain >= 0.1) & (ECDF_diff_mean_tail_domain < 0.3) )[0].shape[0]
            c = np.where( (ECDF_diff_mean_tail_domain >= 0.3) & (ECDF_diff_mean_tail_domain < 0.5) )[0].shape[0]
            d = np.where( (ECDF_diff_mean_tail_domain >= 0.5) & (ECDF_diff_mean_tail_domain < 1) )[0].shape[0]
            e = np.where( (ECDF_diff_mean_tail_domain >= 1) & (ECDF_diff_mean_tail_domain < 3) )[0].shape[0]
            f = np.where( (ECDF_diff_mean_tail_domain >= 3) & (ECDF_diff_mean_tail_domain < 7) )[0].shape[0]
            g = np.where(ECDF_diff_mean_tail_domain >= 7)[0].shape[0]
            sizes = [a, b, c, d, e, f, g]
            colors = ["#000000", "#f9df4d", "#6b6bf7", "#ff007f", "#7fff00", "#00734b", "#996400"]
            ax.pie(sizes, colors=colors, startangle=0)
            plt.axis("equal")

            # Print on screen the area difference between the ECDF of the obs and nwp rainfall distributions (only the tail's distribution)
            print(" - Percentage of mean ECDF separation between obs and nwp rainfall distributions for " + Domain_Name)
            print("     a: " + str(a/ECDF_diff_mean_tail.shape[0] * 100))
            print("     b: " + str(b/ECDF_diff_mean_tail.shape[0] * 100))
            print("     c: " + str(c/ECDF_diff_mean_tail.shape[0] * 100))
            print("     d: " + str(d/ECDF_diff_mean_tail.shape[0] * 100))
            print("     e: " + str(e/ECDF_diff_mean_tail.shape[0] * 100))
            print("     f: " + str(f/ECDF_diff_mean_tail.shape[0] * 100))
            print("     g: " + str(g/ECDF_diff_mean_tail.shape[0] * 100))

            # Saving the pie-charts between the ECDF of the obs and nwp rainfall distributions (only the tail's distribution)
            MainDirOUT = Git_Repo + "/" + DirOUT + "/MinDays_Perc_" + str(MinDays_Perc*100) + "/MaxPerc_" + str(MaxPerc) + "/" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF) + "/" + SystemNWP
            if not os.path.exists(MainDirOUT):
                  os.makedirs(MainDirOUT)
            FileOUT = "ECDF_Diff_Tail_" + Domain_Name + ".png"
            fig.savefig(MainDirOUT + "/" + FileOUT)
            plt.close()