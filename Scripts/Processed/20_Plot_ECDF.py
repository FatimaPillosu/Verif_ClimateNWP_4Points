import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator

###################################################################################################
# CODE DESCRIPTION
# 20_Plot_ECDF.py plots the obs and nwp ECDFs, real and in logarithmic scale.
# Code runtime: ~ 2 hours.

# DESCRIPTION OF INPUT PARAMETERS
# YearS (number, in YYYY format): start year to consider.
# YearF (number, in YYYY format): final year to consider.
# Acc (number, in hours): rainfall accumulation period.
# MinDays_Perc (float, from 0 to 1): % of min n. of days with valid obs at each location.
# SystemNWP_list (list of strings): list of NWP models.
# SystemNWP_Colour_list (list of strings): list of colours to associate to each NWP model.
# Git_Repo (string): path of local github repository.
# DirIN_OBS (string): relative path for the directory containing the observed rainfall realizations.
# DirIN_NWP (string): relative path for the directory containing the NWP rainfall realizations.
# DirOUT (string): relative path for the directory containing the ECDFs.

# INPUT PARAMETERS
YearS = 2000
YearF = 2019
Acc = 24
MinDays_Perc = 0.75
SystemNWP_list = ["Reanalysis/ERA5_EDA", "Reanalysis/ERA5", "Reforecasts/ECMWF_46r1", "Reanalysis/ERA5_ecPoint"]
SystemNWP_Colour_list = ["#CBE676", "#CDA590", "#6EB0C6", "#E25862"]
Git_Repo = "/ec/vol/ecpoint_dev/mofp/papers_2_write/Verif_ClimateNWP_4Points"
DirIN_OBS = "Data/Compute/10_AlignOBS_CleanSTVL/Coeff_Grid2Point_1000"
DirIN_NWP = "Data/Compute/19_Merged_tp_NWP"
DirOUT = "Data/Plot/20_ECDF"
###################################################################################################


# Defining percentiles to use in the sampling of the rainfall distributions
percs = np.arange(1,100,1)

# Reading the observational rainfall realizations
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

# Sampling the the observational rainfall distributions 
print("Sampling the the observational rainfall distributions...")
perc_obs = np.nanpercentile(tp_obs_MinNumDays, percs, axis = 1).T

# Reading the NWP modelled rainfall realizations, and sampling them
print()
print("Reading the NWP modelled rainfall realizations, and sampling them...")
perc_nwp_all = []
for SystemNWP in SystemNWP_list:
      FileIN = Git_Repo + "/" + DirIN_NWP + "/MinDays_Perc_" + str(MinDays_Perc*100) + "/" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF) + "/" +  SystemNWP + "/tp.npy"
      perc_nwp_all.append(np.nanpercentile(np.load(FileIN), percs, axis = 1).T)
      
# Plotting the obs and nwp ECDFs (i.e. sampled rainfall distributions)
print()
print("Plotting the obs and nwp ECDFs (i.e. sampled rainfall distributions) for...")
for ind_stn in range(num_stn_MinNumDays):

      print(" - Rain gauge n." + str(ind_stn) + "/" + str(num_stn_MinNumDays))
      
      fig_real, ax_real = plt.subplots(figsize=(8, 6)) # initialize the figure containing the real ECDFs from observations and NWP models
      fig_log, ax_log = plt.subplots(figsize=(8, 6)) # initialize the figure containing the log ECDFs from observations and NWP models

      for ind_nwp in range(len(SystemNWP_list)):
            
            SystemNWP = SystemNWP_list[ind_nwp]
            SystemNWP_Colour = SystemNWP_Colour_list[ind_nwp]
            perc_nwp = perc_nwp_all[ind_nwp]
            
            ax_real.plot(perc_nwp[ind_stn,:], percs, marker = "o", markersize = 3, color = SystemNWP_Colour, label = SystemNWP)
            ax_log.plot(perc_nwp[ind_stn,:], percs, marker = "o", markersize = 3, color = SystemNWP_Colour, label = SystemNWP)

      # Completing the nwp ECDF plots with the obs ECDF and metadata
      ax_real.plot(perc_obs[ind_stn,:], percs, marker = "o", markersize = 3, color = "black", label = "obs")
      ax_real.set_xlabel("Rainfall [mm/" + str(Acc) + "h]", fontsize="14")
      ax_real.set_ylabel("Percentiles", fontsize="14")
      ax_real.xaxis.set_tick_params(labelsize=14)
      ax_real.yaxis.set_tick_params(labelsize=14)
      ax_real.grid(True, which='both', axis='y')
      ax_real.spines['top'].set_visible(False)
      ax_real.spines['right'].set_visible(False)
      
      linthresh = 0.1
      ax_log.plot(perc_obs[ind_stn,:], percs, marker = "o", markersize = 3, color = "black", label = "obs")
      ax_log.set_xlabel("Rainfall [mm/" + str(Acc) + "h]", fontsize="14")
      ax_log.set_ylabel("Percentiles", fontsize="14")
      ax_log.set_xscale('symlog', linthresh=linthresh, linscale=0.03)
      ax_log.set_xlim([-0.1,101])
      ax_log.set_ylim([0,101])
      ax_log.xaxis.set_tick_params(labelsize=14)
      ax_log.yaxis.set_tick_params(labelsize=14)
      ax_log.xaxis.set_major_locator(plt.FixedLocator([0, 0.1, 1, 10, 100]))
      ax_log.xaxis.set_major_formatter(plt.FuncFormatter(lambda value, _: f'{value:.0f}'))
      log_locator = LogLocator(base=10.0, subs=np.arange(2, 10)*0.1, numticks=100)
      def apply_log_minor_ticks(ax):
            xlim = ax.get_xlim()
            log_start_pos = linthresh
            log_start_neg = -linthresh if xlim[0] < 0 else None
            ax.xaxis.set_minor_locator(log_locator)
            minor_ticks = [t for t in ax.get_xaxis().get_minor_locator().tick_values(0, 10)
                  if (t > log_start_pos or (log_start_neg is not None and t < log_start_neg))]
            ax.set_xticks(minor_ticks, minor=True)
      apply_log_minor_ticks(ax_log)
      ax_log.grid(True, which='both', axis='y')
      ax_log.spines['top'].set_visible(False)
      ax_log.spines['right'].set_visible(False)

      # Saving the ECDF plots
      MainDirOUT_real = Git_Repo + "/" + DirOUT + "/Real/MinDays_Perc_" + str(MinDays_Perc*100) + "/" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF)
      if not os.path.exists(MainDirOUT_real):
            os.makedirs(MainDirOUT_real)
      FileOUT_real = "ECDF_" + str(lats_obs_MinNumDays[ind_stn]) + "_" + str(lons_obs_MinNumDays[ind_stn]) + ".png"
      fig_real.savefig(MainDirOUT_real + "/" + FileOUT_real)
      
      MainDirOUT_log = Git_Repo + "/" + DirOUT + "/Log/MinDays_Perc_" + str(MinDays_Perc*100) + "/" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF)
      if not os.path.exists(MainDirOUT_log):
            os.makedirs(MainDirOUT_log)
      FileOUT_log = "ECDF_" + str(lats_obs_MinNumDays[ind_stn]) + "_" + str(lons_obs_MinNumDays[ind_stn]) + ".png"
      fig_log.savefig(MainDirOUT_log + "/" + FileOUT_log)
      
      plt.close()