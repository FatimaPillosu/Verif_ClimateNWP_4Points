import os
import numpy as np
import metview as mv
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.ticker import LogLocator

###################################################################################################
# CODE DESCRIPTION
# 06_Plot_CDF.py plots the CDFs for the observational and the NWP modelled climatology distributions at specific locations.
# Code runtime: ~ 30 minutes.

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
SystemNWP_Colour_list = ["royalblue","goldenrod", "brown", "limegreen"]
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_ClimateNWP_4Points"
DirIN_OBS = "Data/Raw/Climate_OBS"
DirIN_NWP = "Data/Raw/Climate_NWP"
DirOUT = "Data/Plot/06_CDF"
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

# Setting all the small negative values to 0 mm of rain
climate_NWP_all[(climate_NWP_all > 0) & (climate_NWP_all < 0.1)] = 0.1

# Creating the CDFs plots
print()
print("Plotting the CDF")
for ind_stn in range(num_stn):

      print(" - n. " + str(ind_stn) + "/" + str(num_stn))

      fig, ax = plt.subplots(figsize=(10, 6))

      for ind_NWP in range(num_NWP):
            
            SystemNWP = SystemNWP_list[ind_NWP]
            SystemNWP_Colour = SystemNWP_Colour_list[ind_NWP]
            if SystemNWP == "Reanalysis/ERA5_ecPoint":
                  LineWidth = 6
            else:
                  LineWidth = 4
            ax.plot(climate_NWP_all[ind_stn, :, ind_NWP], percentiles_OBS, SystemNWP_Colour, linewidth=LineWidth, label=SystemNWP)

      # Completing the plot
      linthresh = 0.1
      ax.plot(climate_OBS[ind_stn, :], percentiles_OBS, "k.", label="Climate_OBS", markersize = 10)
      ax.set_xlabel("Rainfall [mm/" + str(Acc) + "h]", fontsize="14")
      ax.set_ylabel("Percentiles", fontsize="14")
      ax.set_xscale('symlog', linthresh=linthresh, linscale=0.03)
      ax.set_xlim([-0.1,101])
      ax.set_ylim([0,101])
      ax.xaxis.set_tick_params(labelsize=14)
      ax.yaxis.set_tick_params(labelsize=14)
      ax.xaxis.set_major_locator(plt.FixedLocator([0, 0.1, 1, 10, 100]))
      ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda value, _: f'{value:.0f}'))
      log_locator = LogLocator(base=10.0, subs=np.arange(2, 10)*0.1, numticks=100)
      def apply_log_minor_ticks(ax):
            xlim = ax.get_xlim()
            log_start_pos = linthresh
            log_start_neg = -linthresh if xlim[0] < 0 else None
            ax.xaxis.set_minor_locator(log_locator)
            minor_ticks = [t for t in ax.get_xaxis().get_minor_locator().tick_values(0, 10)
                  if (t > log_start_pos or (log_start_neg is not None and t < log_start_neg))]
            ax.set_xticks(minor_ticks, minor=True)
      apply_log_minor_ticks(ax)
      ax.grid(True, which='both', axis='y')
      ax.spines['top'].set_visible(False)
      ax.spines['right'].set_visible(False)

      # Save the plot
      MainDirOUT = Git_Repo + "/" + DirOUT + "/tp_" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF)
      print(MainDirOUT)
      if not os.path.exists(MainDirOUT):
            os.makedirs(MainDirOUT)
      FileOUT = "cdf_" + str(lats_OBS[ind_stn]) + "_" + str(lons_OBS[ind_stn]) + ".png"
      fig.savefig(MainDirOUT + "/" + FileOUT)
      plt.close()