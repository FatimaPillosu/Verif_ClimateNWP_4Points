import os
import numpy as np
import metview as mv
import matplotlib.pyplot as plt

##############################################################################################################
# CODE DESCRIPTION
# 27_Plot_Diff_OBS_NWP_Climate_Piechart.py plots piecharts to represent the difference (in percentage) between observational and 
# modelled climatologies. 
# Code runtime: negligible

# DESCRIPTION OF INPUT PARAMETERS
# RP (integer, in years): return period to plot.
# Domain_Coord_list (list of floats): list of coordinates of the domain of interest.
# Domain_Name_list (list of strings): list of the names of the domain of interest.
# SystemNWP_list (string): list containing the names of the considered forecasting systems.
# Git_Repo (string): path of local GitHub repository.
# DirIN_obs (string): relative path for the directory containing the observational climatology.
# DirIN_nwp (string): relative path for the directory containing the NWP modelled climatology.
# DirOUT (string): relative path for the directory containing the piecharts.  

# INPUT PARAMETERS
RP = 10
Domain_Coord_list = [ [90,-170,15,-50], [15, -100, -60, -30], [90, -30, 30, 60], [30,-30,-40,60], [90, 60, 5, 180], [5, 60, -60, 180] ]
Domain_Name_list = ["North_America", "South_America", "Europe_Mediterranean", "Africa", "Asia", "Oceania"]
SystemNWP_list = ["Reanalysis/ERA5_EDA", "Reanalysis/ERA5", "Reforecasts/ECMWF_46r1", "Reanalysis/ERA5_ecPoint"]
Git_Repo = "/ec/vol/ecpoint_dev/mofp/papers_2_write/Verif_ClimateNWP_4Points"
DirIN_obs = "Data/Compute/12_Climate_OBS/08_AlignOBS_Combine_Years_RawSTVL/MinDays_Perc_75.0/24h_2000_2019"
DirIN_nwp = "Data/Compute/16_Climate_G/24h_2000_2019"
DirOUT = "Data/Plot/27_Diff_OBS_NWP_Climate_Piechart/08_AlignOBS_Combine_Years_RawSTVL/MinDays_Perc_75.0/24h_2000_2019"
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

        print(SystemNWP)

        # Reading the computed climate field and correspondent return period values
        climate = mv.read(Git_Repo + "/" + DirIN_nwp + "/" + SystemNWP + "/Climate.grib")
        RP_list = np.load(Git_Repo + "/" + DirIN_nwp + "/" + SystemNWP + "/RP.npy")
        ind_RP = np.where(RP_list == RP)[0]
        climate_nwp_RP = mv.nearest_gridpoint( climate[ind_RP], lats, lons)

        # Computing the difference between the observed and the modelled climatologies
        diff = climate_nwp_RP - climate_obs_RP
        
        # Computing the percentage of nwp climatologies exceeding the observed climatologies
        for ind_domain in np.arange(len(Domain_Name_list)):

                Domain_Name = Domain_Name_list[ind_domain]
                Domain_Coord = Domain_Coord_list[ind_domain]
            
                # Selecting the domain to consider
                ind_gp_domain = np.where( (lats < Domain_Coord[0]) & (lats > Domain_Coord[2]) & (lons > Domain_Coord[1]) & (lons < Domain_Coord[3]) )
                diff_domain = diff[ind_gp_domain]
                
                # Creating the piecharts
                fig,ax = plt.subplots()
                nwp_above_obs = np.sum(diff_domain>0) / diff_domain.shape[0] * 100
                nwp_below_obs = 100 - nwp_above_obs
                print(" - % of NWP above OBS climate in " + Domain_Name + ": " + str(np.round(nwp_above_obs, decimals = 2)))
                sizes = [nwp_above_obs, nwp_below_obs]
                colors = ["#00008B", "gainsboro"]
                ax.pie(sizes, colors=colors, startangle=0)
                plt.axis("equal")

                # Saving the piecharts
                MainDirOUT = Git_Repo + "/" + DirOUT + "/" + SystemNWP
                if not os.path.exists(MainDirOUT):
                        os.makedirs(MainDirOUT)
                FileOUT = "Climate_Diff_" + Domain_Name + ".png"
                fig.savefig(MainDirOUT + "/" + FileOUT)
                plt.close()