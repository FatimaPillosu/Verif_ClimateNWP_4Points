import os
import numpy as np
import metview as mv

#####################################################################
# CODE DESCRIPTION
# 03_Compute_Climate_G.py merges the climatology for all sub-areas to create a 
# global field.
# Code runtime: the code takes up to 1 minute to run in serial.

# DESCRIPTION OF INPUT PARAMETERS
# NumSA (integer): number of total considered sub-areas.
# Dataset_SystemFC (string): name of the dataset and forecasting system to consider.
# Git_Repo (string): path of local github repository.
# DirIN (string): relative path for the input directory containing ERA5.
# DirOUT (string): relative path for the output directory containing the climatology.

# INPUT PARAMETERS
NumSA = 220
Dataset_SystemFC = "Reanalysis/ERA5_ecPoint"
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Compute/Climate_NWP_tp"
DirIN = "Data/Compute/02_Climate_SA/24h_2000_2019"
DirOUT = "Data/Compute/03_Climate_G/24h_2000_2019"
#####################################################################


# Reading the global field for the sample grib
File_Template = Git_Repo + "/" + DirOUT + "/" + Dataset_SystemFC + "/Template_Global.grib"
template_global = mv.read(File_Template)

# Merging the climatologies for all the sub-areas to create global fields
print("Merging the climatologies for all the sub-areas to create global fields")
for ind_SA in range(0,NumSA):
      print(" - Reading the sub-area n." + str(ind_SA) + "/" + str(NumSA-1))
      DirIN_temp = Git_Repo + "/" + DirIN + "/" + Dataset_SystemFC
      FileIN_temp = "Climate_SA_" + f'{ind_SA:03d}' + ".npy"
      climate_SA = np.load(DirIN_temp + "/" + FileIN_temp)
      if ind_SA == 0:
            climate_G = climate_SA
      else:
            climate_G = np.concatenate((climate_G, climate_SA), axis=0) 

#  Storing the percentiles as grib
print("Converting the numpy array into grib")
Num_Perc = climate_G.shape[1]
percs_tot_global = None
for ind_perc in range(Num_Perc):
      percs_tot_global = mv.merge(percs_tot_global, mv.set_values(template_global, climate_G[:,ind_perc]))

# Saving the output file
print("Storing the grib file containing the global field of the climatology")
FileOUT = Git_Repo + "/" + DirOUT  + "/" + Dataset_SystemFC + "/Climate.grib"
mv.write(FileOUT, percs_tot_global)

# Deleting the template file
os.remove(File_Template)