import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator
from statsmodels.distributions.empirical_distribution import ECDF

###################################################################################################
# CODE DESCRIPTION
# 20_Plot_ECDF.py plots the ECDFs for the observational and the NWP modelled rainfall realizations.
# Code runtime: ~ 30 minutes.

# DESCRIPTION OF INPUT PARAMETERS
# YearS (number, in YYYY format): start year to consider.
# YearF (number, in YYYY format): final year to consider.
# Acc (number, in hours): rainfall accumulation period.
# MinDays_Perc (float, from 0 to 1): % of min n. of days with valid obs at each location.
# SystemNWP_list (list of string): list of NWP model climatologies.
# Git_Repo (string): path of local github repository.
# DirIN_OBS (string): relative path for the directory containing the rainfall observational.
# DirIN_NWP (string): relative path for the directory containing the NWP modelled rainfall realizations.
# DirOUT (string): relative path for the directory containing the AD statistic.

# INPUT PARAMETERS
YearS = 2000
YearF = 2019
Acc = 24
MinDays_Perc = 0.75
SystemNWP_list = ["Reanalysis/ERA5_EDA", "Reanalysis/ERA5", "Reforecasts/ECMWF_46r1", "Reanalysis/ERA5_ecPoint"]
SystemNWP_Colour_list = ["brown", "limegreen", "goldenrod", "royalblue"]
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_ClimateNWP_4Points"
DirIN_OBS = "Data/Compute/10_AlignOBS_CleanSTVL/Coeff_Grid2Point_20"
DirIN_NWP = "Data/Compute/19_Merged_tp_NWP"
DirOUT = "Data/Plot/20_ECDF"
###################################################################################################


# Reading the observational climatology
print()
print("Reading the realizations from rainfall observations...")
MainDirIN_OBS = Git_Repo + "/" + DirIN_OBS + "/" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF)
tp_obs = np.load(MainDirIN_OBS + "/obs.npy")
lats_obs = np.load(MainDirIN_OBS + "/stn_lats.npy")
lons_obs = np.load(MainDirIN_OBS + "/stn_lons.npy")
num_stn = tp_obs.shape[0]

# Selecting the stations with the required minimum number of days with valid observations
print("Selecting the stations with the considered minimum number of days with valid observations...")
MinNumDays = round(tp_obs.shape[1] * MinDays_Perc)
NumDays_NotNaN = np.sum(~np.isnan(tp_obs), axis=1) # array containing the n. of days with observations for each rain gauge
ind_stns_MinNumDays = np.where(NumDays_NotNaN >= MinNumDays)[0]
tp_obs_MinNumDays = tp_obs[ind_stns_MinNumDays]
lats_obs_MinNumDays = lats_obs[ind_stns_MinNumDays]
lons_obs_MinNumDays = lons_obs[ind_stns_MinNumDays]
num_stn_MinNumDays = tp_obs_MinNumDays.shape[0]
print(" - Total number of days between " + str(YearS) + " and " + str(YearF) + ": " + str(tp_obs.shape[1]))
print(" - Totals number of stations with at least " + str(int(MinDays_Perc*100)) + "% of days (= " + str(int(MinNumDays)) + ") with valid observations: " + str(num_stn_MinNumDays) + "/" + str(num_stn))

# Reading the NWP modelled rainfall realizations
print()
print("Reading the rainfall realizations from NWP models...")
tp_nwp_all = []
for SystemNWP in SystemNWP_list:
      FileIN = Git_Repo + "/" + DirIN_NWP + "/MinDays_Perc_" + str(MinDays_Perc*100) + "/" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF) + "/" +  SystemNWP + "/tp.npy"
      tp_nwp_all.append(np.load(FileIN))

# Plotting the ECDFs for the rainfall distribution from observations and NWP models
print()
print("Plotting the ECDFs for the rainfall distribution from observations and NWP models")
for ind_stn in range(num_stn_MinNumDays):

      print(" - Creating the ECDF plots for the rain gauge n." + str(ind_stn) + "/" + str(num_stn_MinNumDays))
      tp_obs = tp_obs_MinNumDays[ind_stn,:]
      tp_obs_nonan = tp_obs[~np.isnan(tp_obs)] # eliminate all nan values from the calculation of the ECDF
      ecdf_obs = ECDF(tp_obs_nonan)
      
      fig, ax = plt.subplots(figsize=(8, 6)) # initialize the figure containing the ECDFs from observations and NWP models

      for ind_nwp in range(len(SystemNWP_list)):
            
            SystemNWP = SystemNWP_list[ind_nwp]
            SystemNWP_Colour = SystemNWP_Colour_list[ind_nwp]
            tp_nwp = tp_nwp_all[ind_nwp]
            ecdf_nwp = ECDF(tp_nwp[ind_stn,:])

            plt.plot(ecdf_nwp.x, ecdf_nwp.y * 100, marker = ".", color = SystemNWP_Colour, label = SystemNWP)
            
      # Completing the plot with the ECDF from the distribution of observations
      linthresh = 0.1
      plt.plot(ecdf_obs.x, ecdf_obs.y * 100, marker = ".", color = "black", label = "obs")
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
      MainDirOUT = Git_Repo + "/" + DirOUT + "/MinDays_Perc_" + str(MinDays_Perc*100) + "/" +f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF)
      if not os.path.exists(MainDirOUT):
            os.makedirs(MainDirOUT)
      FileOUT = "ecdf_" + str(lats_obs_MinNumDays[ind_stn]) + "_" + str(lons_obs_MinNumDays[ind_stn]) + ".png"
      fig.savefig(MainDirOUT + "/" + FileOUT)
      plt.close()