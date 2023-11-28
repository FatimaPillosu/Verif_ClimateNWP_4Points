import os
from os.path import exists
import numpy as np
from matplotlib import pyplot as plt

###############################################################################################################################
# CODE DESCRIPTION
# 14_Plot_CDF.py plots the rainfall climatologies (observational and modelled) as CDFs.
# Code runtime: negligible.

# DESCRIPTION OF INPUT PARAMETERS
# Loc_Coord (list of two floats): latitude and longitude of the location to consider.
# MaxPerc2Plot (float): maximum percentile to plot.
# NameOBS (string): name of the observation dataset to plot.
# Coeff_Grid2Point (integer): coefficient used to compare CPC's gridded rainfall values with STVL's point rainfall observations. 
# MinDays_Perc_list (float, from 0 to 1): percentage of minimum n. of days over the considered period with valid observations to compute the climatologies.
# Season (string): season to plot. Valid values are:
#                                         - "Year": for the year climatology
#                                         - "DJF": for the seasonal climatology, winter months (December, January, February)
#                                         - "MAM": for the seasonal climatology, spring months (March, April, May)
#                                         - "JJA": for the seasonal climatology, summer months (June, July, August)
#                                         - "SON": for the seasonal climatology, autumn months (September, October, November)
# SystemFC_list (list of strings): list of forecasting systems to consider. Valid values are:
#                                   - Reforecasts_46r1
#                                   - ERA5_ShortRange
#                                   - ERA5_EDA_ShortRange
#                                   - ERA5_LongRange
#                                   - ERA5_EDA_LongRange
#                                   - ERA5_ecPoint/Grid_BC_VALS
#                                   - ERA5_ecPoint/Pt_BC_PERC
# SystemFC_Colour_list (list of strings): list of colours to assign to each forecasting system.
# Git_repo (string): path of local github repository.
# DirIN (string): relative path for the input directory.
# DirOUT (string): relative path for the output directory.

# INPUT PARAMETERS
Acc = 24
Loc_Coord = [-15.45,145.18]
MaxPer2Plot = 99.98
NameOBS = "08_AlignOBS_CleanSTVL"
Coeff_Grid2Point = 20
MinDays_Perc = 0.75
Season = "Year"
SystemFC_list = ["ERA5_ecPoint/Pt_BC_PERC", "Reforecasts_46r1", "ERA5_EDA_ShortRange", "ERA5_ShortRange"]
SystemFC_Colour_list = ["orange", "cyan", "magenta", "lime"]
Git_repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/ecPoint_Climate"
NameFileOUT = "Australia"
DirIN = "Data/Compute"
DirOUT= "Data/Plot/14_CDF"
###############################################################################################################################


# Setting main output directory
MainDirOUT = Git_repo + "/" + DirOUT
if not exists(MainDirOUT):
      os.makedirs(MainDirOUT)

# Select the percentiles computed for the considered season
if Season == "Year":
      Perc_Dataset = "Year"
else:
      Perc_Dataset = "Season"

# Setting up the figure where the CDFs will be plot
plt.rcParams["figure.figsize"] = (15,8)

# Indexing the location from where to extract the observational and modelled climatologies
File_lats = Git_repo + "/" + DirIN + "/09_Climate_OBS/MinDays_Perc" + str(int(MinDays_Perc*100)) + "/" + NameOBS + "/Coeff_Grid2Point_" +  str(Coeff_Grid2Point) + "/Stn_lats_" + Season + ".npy"
File_lons = Git_repo + "/" + DirIN + "/09_Climate_OBS/MinDays_Perc" + str(int(MinDays_Perc*100)) + "/" + NameOBS + "/Coeff_Grid2Point_" +  str(Coeff_Grid2Point) + "/Stn_lons_" + Season + ".npy"
lats = np.load(File_lats)
lons = np.load(File_lons)
ind_point = np.where(((lats == Loc_Coord[0]) & (lons==Loc_Coord[1])))[0][0]

# Plotting the modelled climatologies as CDFs
for ind_SystemFC in range(len(SystemFC_list)):

      SystemFC = SystemFC_list[ind_SystemFC]
      SystemFC_Colour = SystemFC_Colour_list[ind_SystemFC]

      File_Climate_FC = Git_repo + "/" + DirIN + "/11_ClimateFC_atOBS/" + SystemFC + "/MinDays_Perc" + str(int(MinDays_Perc*100)) + "/" + NameOBS + "/Coeff_Grid2Point_" +  str(Coeff_Grid2Point) + "/Climate_" + Season + ".npy"
      File_Perc_FC = Git_repo + "/" + DirIN + "/11_ClimateFC_atOBS/ERA5_ecPoint/Pt_BC_PERC/MinDays_Perc" + str(int(MinDays_Perc*100)) + "/" + NameOBS + "/Coeff_Grid2Point_" +  str(Coeff_Grid2Point) + "/Percentiles_" + Perc_Dataset + ".npy"
      climate_FC = np.load(File_Climate_FC)[ind_point,:]
      perc_FC = np.load(File_Perc_FC)
      maxPerc = np.where(perc_FC <= MaxPer2Plot)[0]
      plt.plot(climate_FC[maxPerc], perc_FC[maxPerc], SystemFC_Colour, linewidth=2, label=SystemFC)

# Plotting the observational climatology as a CDF
File_Climate_OBS = Git_repo + "/" + DirIN + "/09_Climate_OBS/MinDays_Perc" + str(int(MinDays_Perc*100)) + "/" + NameOBS + "/Coeff_Grid2Point_" +  str(Coeff_Grid2Point) + "/Climate_" + Season + ".npy"
File_Perc_OBS = Git_repo + "/" + DirIN + "/09_Climate_OBS/MinDays_Perc" + str(int(MinDays_Perc*100)) + "/" + NameOBS + "/Coeff_Grid2Point_" +  str(Coeff_Grid2Point) + "/Percentiles_" + Perc_Dataset + ".npy"
climate_OBS = np.load(File_Climate_OBS)[ind_point,:]
perc_OBS = np.load(File_Perc_OBS)
maxPerc = np.where(perc_OBS <= MaxPer2Plot)[0]
plt.plot(climate_OBS[maxPerc], perc_OBS[maxPerc], "k.", linewidth=2, label="Climate_OBS")

# Completing the plot
plt.title("Observational and Modelled Climatologies\n " + NameFileOUT + " (lat=" + str(Loc_Coord[0]) + ", lon=" + str(Loc_Coord[1]) + "), Max Percentile = " + str(MaxPer2Plot) + "th", fontsize="24")
plt.xlabel("Rainfall [mm/" + str(Acc) + "h]", fontsize="18")
plt.ylabel("Percentiles", fontsize="18")
plt.xticks(fontsize="14")
plt.yticks(fontsize="14")
plt.legend(fontsize="14")
plt.xlim([-10,40])
plt.ylim([40,100])
plt.show()

#plt.savefig(DirOUT + "/Distr_tp" + str(Acc) + "h_" +str(a) + "mm_" + str(b) + "mm.png")
#plt.close()


