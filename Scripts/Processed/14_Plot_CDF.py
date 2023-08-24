import numpy as np
from matplotlib import pyplot as plt

lat = 51.55
lon = -0.42
MaxPer2Plot = 99.98
NameOBS = "08_AlignOBS_CleanSTVL"
Coeff_Grid2Point = 20
MinDays_Perc = 0.75
Climate_Dataset = "Year"
Git_repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/ecPoint_Climate"
DirIN = "Data/Compute"
DirOUT= "Data/Plot"
DirOUT = "Data/Figures"
#############################################################

if Climate_Dataset == "Year":
      Perc_Dataset = "Year"
else:
      Perc_Dataset = "Season"

File_lats = Git_repo + "/" + DirIN + "/09_Climate_OBS/MinDays_Perc" + str(int(MinDays_Perc*100)) + "/" + NameOBS + "/Coeff_Grid2Point_" +  str(Coeff_Grid2Point) + "/Stn_lats_" + Climate_Dataset + ".npy"
File_lons = Git_repo + "/" + DirIN + "/09_Climate_OBS/MinDays_Perc" + str(int(MinDays_Perc*100)) + "/" + NameOBS + "/Coeff_Grid2Point_" +  str(Coeff_Grid2Point) + "/Stn_lons_" + Climate_Dataset + ".npy"
lats = np.load(File_lats)
lons = np.load(File_lons)
ind_point = np.where(((lats == lat) & (lons==lon)))[0][0]

File_Climate_ecPoint = Git_repo + "/" + DirIN + "/11_ClimateFC_atOBS/ERA5_ecPoint/Pt_BC_PERC/MinDays_Perc" + str(int(MinDays_Perc*100)) + "/" + NameOBS + "/Coeff_Grid2Point_" +  str(Coeff_Grid2Point) + "/Climate_" + Climate_Dataset + ".npy"
File_Perc_ecPoint = Git_repo + "/" + DirIN + "/11_ClimateFC_atOBS/ERA5_ecPoint/Pt_BC_PERC/MinDays_Perc" + str(int(MinDays_Perc*100)) + "/" + NameOBS + "/Coeff_Grid2Point_" +  str(Coeff_Grid2Point) + "/Percentiles_" + Perc_Dataset + ".npy"
climate_ecPoint = np.load(File_Climate_ecPoint)[ind_point,:]
perc_ecPoint = np.load(File_Perc_ecPoint)
maxPerc = np.where(perc_ecPoint <= MaxPer2Plot)[0]
plt.plot(climate_ecPoint[maxPerc], perc_ecPoint[maxPerc], "b-", linewidth=2, label="Climate_ecPoint")

File_Climate_ecPoint = Git_repo + "/" + DirIN + "/11_ClimateFC_atOBS/ERA5_EDA_ShortRange/MinDays_Perc" + str(int(MinDays_Perc*100)) + "/" + NameOBS + "/Coeff_Grid2Point_" +  str(Coeff_Grid2Point) + "/Climate_" + Climate_Dataset + ".npy"
File_Perc_ecPoint = Git_repo + "/" + DirIN + "/11_ClimateFC_atOBS/ERA5_EDA_ShortRange/MinDays_Perc" + str(int(MinDays_Perc*100)) + "/" + NameOBS + "/Coeff_Grid2Point_" +  str(Coeff_Grid2Point) + "/Percentiles_" + Perc_Dataset + ".npy"
climate_ecPoint = np.load(File_Climate_ecPoint)[ind_point,:]
perc_ecPoint = np.load(File_Perc_ecPoint)
maxPerc = np.where(perc_ecPoint <= MaxPer2Plot)[0]
plt.plot(climate_ecPoint[maxPerc], perc_ecPoint[maxPerc], "r-", linewidth=2, label="Climate_ecPoint")

File_Climate_OBS = Git_repo + "/" + DirIN + "/09_Climate_OBS/MinDays_Perc" + str(int(MinDays_Perc*100)) + "/" + NameOBS + "/Coeff_Grid2Point_" +  str(Coeff_Grid2Point) + "/Climate_" + Climate_Dataset + ".npy"
File_Perc_OBS = Git_repo + "/" + DirIN + "/09_Climate_OBS/MinDays_Perc" + str(int(MinDays_Perc*100)) + "/" + NameOBS + "/Coeff_Grid2Point_" +  str(Coeff_Grid2Point) + "/Percentiles_" + Perc_Dataset + ".npy"
climate_OBS = np.load(File_Climate_OBS)[ind_point,:]
perc_OBS = np.load(File_Perc_OBS)
maxPerc = np.where(perc_OBS <= MaxPer2Plot)[0]
plt.plot(climate_OBS[maxPerc], perc_OBS[maxPerc], "k-", linewidth=2, label="Climate_OBS")

plt.show()
exit()


File_Climate_ERA5_EDA = Git_repo + "/" + DirIN + "/10_Climate_FC/ERA5_EDA_LongRange/MinDays_Perc" + str(int(MinDays_Perc*100)) + "/" + NameOBS + "_24h_2000_2019/Coeff_Grid2Point_" +  str(Coeff_Grid2Point) + "/Climate_" + Climate_Dataset + ".npy"
File_Perc_ERA5_EDA = Git_repo + "/" + DirIN + "/10_Climate_FC/ERA5_EDA_LongRange/MinDays_Perc" + str(int(MinDays_Perc*100)) + "/" + NameOBS + "_24h_2000_2019/Coeff_Grid2Point_" +  str(Coeff_Grid2Point) + "/Percentiles_" + Perc_Dataset + ".npy"
climate_ERA5_EDA = np.load(File_Climate_ERA5_EDA)[0,:]
perc_ERA5_EDA = np.load(File_Perc_ERA5_EDA)
maxPerc = np.where(perc_ERA5_EDA <= MaxPer2Plot)[0]
plt.plot(climate_ERA5_EDA[maxPerc], perc_ERA5_EDA[maxPerc], "m-", linewidth=2, label="Climate_ERA5_EDA")

File_Climate_ERA5 = Git_repo + "/" + DirIN + "/10_Climate_FC/ERA5_LongRange/MinDays_Perc" + str(int(MinDays_Perc*100)) + "/" + NameOBS + "_24h_2000_2019/Coeff_Grid2Point_" +  str(Coeff_Grid2Point) + "/Climate_" + Climate_Dataset + ".npy"
File_Perc_ERA5 = Git_repo + "/" + DirIN + "/10_Climate_FC/ERA5_LongRange/MinDays_Perc" + str(int(MinDays_Perc*100)) + "/" + NameOBS + "_24h_2000_2019/Coeff_Grid2Point_" +  str(Coeff_Grid2Point) + "/Percentiles_" + Perc_Dataset + ".npy"
climate_ERA5 = np.load(File_Climate_ERA5)[ind_point,:]
perc_ERA5 = np.load(File_Perc_ERA5)
maxPerc = np.where(perc_ERA5 <= MaxPer2Plot)[0]
plt.plot(climate_ERA5[maxPerc], perc_ERA5[maxPerc], "c-", linewidth=2, label="Climate_ERA5")

File_Climate_Reforecasts = Git_repo + "/" + DirIN + "/10_Climate_FC/Reforecasts_46r1/MinDays_Perc" + str(int(MinDays_Perc*100)) + "/" + NameOBS + "_24h_2000_2019/Coeff_Grid2Point_" +  str(Coeff_Grid2Point) + "/Climate_" + Climate_Dataset + ".npy"
File_Perc_Reforecasts = Git_repo + "/" + DirIN + "/10_Climate_FC/Reforecasts_46r1/MinDays_Perc" + str(int(MinDays_Perc*100)) + "/" + NameOBS + "_24h_2000_2019/Coeff_Grid2Point_" +  str(Coeff_Grid2Point) + "/Percentiles_" + Perc_Dataset + ".npy"
climate_Reforecasts = np.load(File_Climate_Reforecasts)[ind_point,:]
perc_Reforecasts = np.load(File_Perc_Reforecasts)
maxPerc = np.where(perc_Reforecasts <= MaxPer2Plot)[0]
plt.plot(climate_Reforecasts[maxPerc], perc_Reforecasts[maxPerc], "r-", linewidth=2, label="Climate_Reforecasts_46r1")



plt.legend()
plt.show()