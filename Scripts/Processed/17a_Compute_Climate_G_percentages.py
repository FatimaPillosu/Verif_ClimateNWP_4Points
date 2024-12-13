import os
import numpy as np
import metview as mv

##############################################################################################################
# CODE DESCRIPTION
# 17_Plot_Climate.py plots the global fields of the NWP-modelled rainfall climatologies.
# Code runtime: negligible

# DESCRIPTION OF INPUT PARAMETERS
# RP_2_Plot_list (list of integers, in years): list of return periods to plot
# SystemNWP_list (string): list containing the names of the considered forecasting systems.
# Git_Repo (string): path of local GitHub repository.
# DirIN_obs (string): relative path for the directory containing the observational climatology.
# DirIN_nwp (string): relative path for the directory containing the NWP modelled climatology.


# INPUT PARAMETERS
RP = 10
Domain_Coord_list = [ [90,-170,15,-50], [15, -100, -60, -30], [90, -30, 30, 60], [30,-30,-40,60], [90, 60, 5, 180], [5, 60, -60, 180] ]
Domain_Name_list = ["North_America", "South_America", "Europe_Mediterranean", "Africa", "Asia", "Oceania"]
SystemNWP_list = ["Reanalysis/ERA5_EDA", "Reanalysis/ERA5", "Reforecasts/ECMWF_46r1", "Reanalysis/ERA5_ecPoint"]
Git_Repo = "/ec/vol/ecpoint_dev/mofp/papers_2_write/Verif_ClimateNWP_4Points"
DirIN_obs = "Data/Compute/12_Climate_OBS/10_AlignOBS_CleanSTVL/Coeff_Grid2Point_1000/MinDays_Perc_75.0/24h_2000_2019"
DirIN_nwp = "Data/Compute/16_Climate_G/24h_2000_2019"
##############################################################################################################


# Reading the considered observed climatology
MainDirIN_Obs = Git_Repo + "/" + DirIN_obs
climate_array = np.load(MainDirIN_Obs + "/Climate.npy")
lats = np.load(MainDirIN_Obs + "/Stn_lats.npy")
lons = np.load(MainDirIN_Obs + "/Stn_lons.npy")
RP_list = np.load(MainDirIN_Obs + "/RP.npy")
RP_list = (np.round(RP_list, decimals = 5)).astype('float64')
ind_RP = np.where(RP_list == RP)[0]
climate_obs_RP = climate_array[:, ind_RP].flatten()

# Reading the considered modelled climatologies
for SystemNWP in SystemNWP_list:

    print(" ")

    # Reading the computed climate field and correspondent return period values
    climate = mv.read(Git_Repo + "/" + DirIN_nwp + "/" + SystemNWP + "/Climate.grib")
    RP_list = np.load(Git_Repo + "/" + DirIN_nwp + "/" + SystemNWP + "/RP.npy")
    ind_RP = np.where(RP_list == RP)[0]
    climate_nwp_RP = mv.nearest_gridpoint( climate[ind_RP], lats, lons)

    # Computing the difference between the observed and the modelled climatologies
    diff = climate_nwp_RP - climate_obs_RP
    
    # Computing the percentage of nwp climatologies exceeding the observed climatologies
    a = 0
    for ind_domain in np.arange(len(Domain_Name_list)):

            Domain_Name = Domain_Name_list[ind_domain]
            Domain_Coord = Domain_Coord_list[ind_domain]
            
            # Selecting the domain to consider
            ind_gp_domain = np.where( (lats < Domain_Coord[0]) & (lats > Domain_Coord[2]) & (lons > Domain_Coord[1]) & (lons < Domain_Coord[3]) )
            diff_domain = diff[ind_gp_domain]
            a = a + np.sum(diff_domain>1) / diff_domain.shape[0] * 100
            #print(diff_domain.shape)
            #print(np.sum(diff_domain>1) / diff_domain.shape[0] * 100)

    print(a/6)
            