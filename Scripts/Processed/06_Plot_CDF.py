import os
import numpy as np
import metview as mv
import matplotlib.pyplot as plt

###################################################################################################
# CODE DESCRIPTION
# 06_Plot_CDF.py plots the CDFs for the observational and the NWP modelled climatology distributions at specific locations.
# Code runtime: ~ 1 minute.

# DESCRIPTION OF INPUT PARAMETERS
# YearS (number, in YYYY format): start year to consider.
# YearF (number, in YYYY format): final year to consider.
# Acc (number, in hours): rainfall accumulation period.
# SystemNWP_list (list of string): list of NWP model climatologies.
# Git_Repo (string): path of local github repository.
# DirIN_OBS (string): relative path for the directory containing the observational climatologies.
# DirIN_NWP (string): relative path for the directory containing the NWP modelled climatologies.
# DirOUT (string): relative path for the directory containing the AD statistic.

# INPUT PARAMETERS
YearS = 2000
YearF = 2019
Acc = 24
SystemNWP_list = ["Reanalysis/ERA5_ecPoint", "Reforecasts/ECMWF_46r1", "Reanalysis/ERA5_EDA", "Reanalysis/ERA5"]
SystemNWP_Colour_list = ["red","khaki", "skyblue", "pink"]
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_ClimateNWP_4Points"
DirIN_OBS = "Data/Raw/Climate_OBS"
DirIN_NWP = "Data/Raw/Climate_NWP"
DirOUT = "Data/Plot/03_Statistic_AD"
###################################################################################################

# Reading the observational climatology
print()
print("Reading the observational climatology...")
MainDirIN_OBS = Git_Repo + "/" + DirIN_OBS + "/tp_" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF)
climate_OBS = np.load(MainDirIN_OBS + "/Climate.npy")
lats_OBS = np.load(MainDirIN_OBS + "/Stn_lats.npy")
lons_OBS = np.load(MainDirIN_OBS + "/Stn_lons.npy")
rp_OBS = np.load(MainDirIN_OBS + "/RP.npy")
percentiles_OBS = np.load(MainDirIN_OBS + "/Perc.npy")
rp_OBS = (np.round(rp_OBS, decimals = 5)).astype('float64')

# Extracting the values of the different NWP modelled climatologies
print()
print("Extracting the values of the different NWP modelled climatologies: ")
num_stn = climate_OBS.shape[0]
num_RP = climate_OBS.shape[1]
num_NWP = len(SystemNWP_list)
climate_NWP_all = np.empty((num_stn, num_RP, num_NWP)) # initialize the variable that will contain the values for all the modelled climatologies

for ind_NWP in range(num_NWP):
      
      SystemNWP = SystemNWP_list[ind_NWP]
      print(" - " + SystemNWP)

      # Reading the considered NWP modelled climatology
      MainDirIN_NWP = Git_Repo + "/" + DirIN_NWP + "/tp_" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF) + "/" + SystemNWP
      climate_NWP = mv.read(MainDirIN_NWP + "/Climate.grib")
      rp_NWP = np.load(MainDirIN_NWP + "/RP.npy")

      # Select the nearest grid-point to the rain gauge locations
      climate_NWP_OBS = mv.nearest_gridpoint(climate_NWP, lats_OBS, lons_OBS).T

      # Selecting the return-periods that were also computed for the observational climatologies
      ind_rp = np.isin(rp_NWP, rp_OBS)
      climate_NWP_OBS = climate_NWP_OBS[:, ind_rp]

      # Storing the NWP CDFs
      climate_NWP_all[:, :, ind_NWP] = climate_NWP_OBS

# Creating the CDFs plots
fig, ax1 = plt.subplots()
for ind_stn in range(num_stn):

      for ind_NWP in range(num_NWP):
            
            SystemNWP = SystemNWP_list[ind_NWP]
            SystemNWP_Colour = SystemNWP_Colour_list[ind_NWP]
            if SystemNWP == "Reanalysis/ERA5_ecPoint":
                  LineWidth = 4
            else:
                  LineWidth = 2
            ax1.plot(climate_NWP_all[ind_stn, :, ind_NWP], percentiles_OBS, SystemNWP_Colour, linewidth=LineWidth, label=SystemNWP)

      # Completing the plot
      ax1.plot(climate_OBS[ind_stn, :], percentiles_OBS, "k.", label="Climate_OBS", markersize = 7)
      ax1.set_title("Observational and Modelled Climatologies\n " + " (lat=" + str(lats_OBS[ind_stn]) + ", lon=" + str(lons_OBS[ind_stn]) + "), Max RP = " + str(int(rp_OBS[-1])) + "-year", fontsize="24")
      ax1.set_xlabel("Rainfall [mm/" + str(Acc) + "h]", fontsize="18")
      ax1.set_ylabel("Percentiles", fontsize="18")
      ax1.xaxis.set_tick_params(labelsize=14)
      ax1.yaxis.set_tick_params(labelsize=14)
      handles, labels = ax1.get_legend_handles_labels()
      ax1.legend(handles, labels, fontsize="14")
      
      MainDirOUT = Git_Repo + "/" + DirOUT + "/tp_" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF) + "/" + SystemNWP
      if not os.path.exists(MainDirOUT):
            os.makedirs(MainDirOUT)


# Save the plot
FileOUT = NameFileOUT + "_" + str(Loc_Coord[0]) + "_" + str(Loc_Coord[1]) + ".png"
fig.savefig(MainDirOUT + "/" + FileOUT)
