import os
import numpy as np
import metview as mv

###########################################################################################################
# CODE DESCRIPTION
# 22_Plot_ECDF_Diff_Map.py plots maps of the mean areal separation between obs & nwp ECDFs.
# Code runtime: up to 1 minute.

# DESCRIPTION OF INPUT PARAMETERS
# YearS (number, in YYYY format): start year to consider.
# YearF (number, in YYYY format): final year to consider.
# Acc (number, in hours): rainfall accumulation period.
# MinDays_Perc (float, from 0 to 1): % of min n. of days with valid obs at each location.
# MaxPerc (integer or float, from 0 to 100 - not included): max percentile considered when sampling the obs & nwp ECDFs. 
# SystemNWP_list (list of string): list of NWP model climatologies.
# Git_Repo (string): path of local github repository.
# DirIN (string): relative path for the directory containing the differences between obs & nwp ECDFs.
# DirOUT (string): relative path for the directory containing the map plots for the mean areal separation between obs & nwp ECDFs.

# INPUT PARAMETERS
YearS = 2000
YearF = 2019
Acc = 24
MinDays_Perc = 0.75
MaxPerc = 99
SystemNWP_list = ["Reanalysis/ERA5_ecPoint", "Reanalysis/ERA5_EDA", "Reanalysis/ERA5", "Reforecasts/ECMWF_46r1"]
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_ClimateNWP_4Points"
DirIN = "Data/Compute/21_ECDF_diff"
DirOUT = "Data/Plot/22_ECDF_Diff_Map"
###########################################################################################################


# Plotting the maps of the mean areal separation between obs & nwp ECDFs
print()
print("Plotting the maps of the mean areal separation between obs & nwp ECDFs for: ")
for SystemNWP in SystemNWP_list:
      
      print(" - " + SystemNWP)

      # Reading the ECDF differences for specific nwp models
      MainDirIN = Git_Repo + "/" + DirIN + "/MinDays_Perc_" + str(MinDays_Perc*100) + "/MaxPerc_" + str(MaxPerc) + "/" +f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF) + "/" + SystemNWP
      tp_obs_mean = np.load(MainDirIN + "/tp_obs_mean.npy")
      perc_diff = np.load(MainDirIN + "/ECDF_Diff.npy")
      perc_list = np.load(MainDirIN + "/Perc_List.npy")
      lats = np.load(MainDirIN + "/" + "Stn_lats.npy")
      lons = np.load(MainDirIN + "/" + "Stn_lons.npy")

      # Computing the mean areal separation between obs & nwp ECDFs expressed as percentage of the mean obs rainfall
      ECDF_diff_mean = ( np.nanmean( np.absolute(perc_diff), axis=1 ) / tp_obs_mean ) * 100
      
      # Converting into geopoints the mean areal separation between obs & nwp ECDFs
      ECDF_diff_mean_geo = mv.create_geo(
            type = "xyv",
            latitudes =  lats,
            longitudes = lons,
            values = ECDF_diff_mean
            )
          
      # Plotting the mean areal separation between obs & nwp ECDFs
      coastlines = mv.mcoast(
            map_coastline_thickness = 3,
            map_coastline_colour = "charcoal",
            map_coastline_resolution = "low",
            map_boundaries = "on",
            map_boundaries_colour = "charcoal",
            map_boundaries_thickness = 3,
            map_grid = "on",
            map_grid_thickness = 3,
            map_grid_colour = "charcoal",
            map_grid_latitude_increment  = 30,
            map_grid_longitude_increment = 60,
            map_label = "on",
            map_label_height = 0.3,
            map_label_top = "off",
            map_label_right = "off"
            )

      markers = mv.psymb(
            legend = "on",
            symbol_type = "marker",
            symbol_table_mode = "on",
            symbol_quality = "high",
            symbol_min_table = [0, 10, 30, 50, 100], 
            symbol_max_table = [10, 30, 50, 100, 10000],
            symbol_marker_table = [15, 15, 15, 15, 15],
            symbol_colour_table = [
                  "rgb(0,0,0)", # 0 - 10
                  "rgb(0.5199,0.5199,0.9624)", # 10 - 30
                  "rgb(0.5333,0.7658,0.3009)",  # 30 - 50 
                  "rgb(0.9774,0.8647,0.3011)", # 50 - 100
                  "rgb(1,0,0.498)"], # 100 - 10000
            symbol_height_table = [0.2, 0.2, 0.2, 0.2, 0.2]
            )
      
      title = mv.mtext(
            text_line_count = 2,
            text_line_1 = "Average areal separation between obs & nwp ECDFs expressed as percentage [%] of the mean obs rainfall - " + SystemNWP,
            text_line_2 = " ",
            text_colour ="charcoal",
            text_font ="arial",
            text_font_size = 3
            )

      legend = mv.mlegend(
            legend_text_colour = "charcoal",
            legend_text_font = "arial",
            legend_text_font_size = 3,
            legend_entry_plot_direction = "row",
            legend_automatic_poistion = "top",
            )

      # Saving the map plots of the mean areal separation between obs & nwp ECDFs
      MainDirOUT = Git_Repo + "/" + DirOUT + "/MinDays_Perc_" + str(MinDays_Perc*100) + "/MaxPerc_" + str(MaxPerc) + "/" f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF) + "/" + SystemNWP
      if not os.path.exists(MainDirOUT):
            os.makedirs(MainDirOUT)
      mv.setoutput(mv.png_output(output_width = 5000, output_name = MainDirOUT + "/ECDF_Diff"))
      mv.plot(coastlines, ECDF_diff_mean_geo, markers, title, legend)