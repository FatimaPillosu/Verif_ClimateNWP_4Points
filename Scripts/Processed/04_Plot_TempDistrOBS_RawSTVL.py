import os
from os.path import exists
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import metview as mv

######################################################################
# CODE DESCRIPTION
# 04_Plot_TempDistrOBS_RawSTVL.py plots the temporal distribution of the average 
# number of rainfall observations per day, in a given year, in each considered rainfall 
# dataset in stvl.
# Code runtime: ~ 30 minutes.

# DESCRIPTION OF INPUT PARAMETERS
# YearS (integer, in YYYY format): start year to consider.
# YearF (integer, in YYYY format): final year to consider.
# Acc (integer, in hours): rainfall accumulation period.
# Dataset_list (list of strings): name of the considered datasets.
# Git_Repo (string): path of local github repository.
# DirIN (string): relative path for the input directory.
# DirOUT (string): relative path for the output directory.

# INPUT PARAMETERS
YearS = 2000
YearF = 2019
Acc = 24
Dataset_list = ["synop", "hdobs", "bom", "india", "efas", "vnm"]
Plot_rows = 3
Plot_cols = 2
Plot_row_loc_list = [0,0,1,1,2,2]
Plot_col_loc_list = [0,1,0,1,0,1]
Git_Repo = "/ec/vol/ecpoint_dev/mofp/papers_2_write/Verif_ClimateNWP_4Points"
DirIN = "Data/Compute/01_UniqueOBS_Extract_FromReference_RawSTVL"
DirOUT = "Data/Plot/04_TempDistrOBS_RawSTVL"
######################################################################


# Setting general parameters
Year_list = range(YearS, YearF+1)
YearSTR_list = [str(Year) for Year in Year_list]
ind_Dataset_list = range(0,len(Dataset_list))

# Setting the panels for the distribution plots
fig, axs = plt.subplots(Plot_rows, Plot_cols, figsize=(25,20), constrained_layout = True)
fig.suptitle("Average number of " + str(Acc) + "-hourly rainfall observations per day in a given year\n ", fontsize=24)

# Plot the distribution of number of rainfall observation per day/dataset in a given year
for ind_Dataset in ind_Dataset_list:
      
      Dataset = Dataset_list[ind_Dataset]
      Plot_row_loc = Plot_row_loc_list[ind_Dataset]
      Plot_col_loc = Plot_col_loc_list[ind_Dataset]

      print("Considering:", Dataset)

      # Considering different years
      av_count_obs = [] 
      for Year in Year_list:

            print(" - ", Year)
            DateTime1 = datetime(Year, 1, 1, 0)
            DateTime2 = datetime(Year, 12, 31, 23)
            NumDays_Year = (DateTime2 - DateTime1).days

            count_obs = 0
            TheDateTime = DateTime1
            while TheDateTime <= DateTime2:
                  
                  print(TheDateTime)
                  TheDateSTR = TheDateTime.strftime("%Y%m%d")
                  TheTimeSTR = TheDateTime.strftime("%H")

                  # Reading the rainfall observations and counting how many observation are in each single day, in a given year
                  FileIN_temp = Git_Repo + "/" + DirIN + "/" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF) + "/" + Dataset + "/" + TheDateSTR + "/tp" + str(Acc) + "_obs_" + TheDateSTR + TheTimeSTR + ".geo"
                  if exists(FileIN_temp):
                        geo = mv.read(FileIN_temp)
                        count_obs = count_obs + mv.count(geo)

                  TheDateTime += timedelta(hours=1)

            # Computing average number of rainfall observations per day in a given year
            av_count_obs.append(round(count_obs / NumDays_Year))
      
      # Plotting the distributions
      axs[Plot_row_loc,Plot_col_loc].bar(Year_list, av_count_obs, color = "b")
      axs[Plot_row_loc,Plot_col_loc].set_title(Dataset, fontsize=24)
      axs[Plot_row_loc,Plot_col_loc].set_xlabel(" \nYears", fontsize=20)
      axs[Plot_row_loc,Plot_col_loc].set_ylabel("N. of observations\n ", fontsize=20)
      axs[Plot_row_loc,Plot_col_loc].set_xticks(Year_list)
      axs[Plot_row_loc,Plot_col_loc].set_xticklabels(YearSTR_list, rotation=45)
      axs[Plot_row_loc,Plot_col_loc].set_ylim([0, 8000])
      axs[Plot_row_loc,Plot_col_loc].xaxis.set_tick_params(labelsize=20)
      axs[Plot_row_loc,Plot_col_loc].yaxis.set_tick_params(labelsize=20)
      for ax in axs.flat:
            ax.label_outer()

# Saving the plot
MainDirOUT = Git_Repo + "/" + DirOUT + "/" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF)
if not exists(MainDirOUT):
      os.makedirs(MainDirOUT)
FileOUT = MainDirOUT + "/TemDistrOBS.png"
plt.savefig(FileOUT)