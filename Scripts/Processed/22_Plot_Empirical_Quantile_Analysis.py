import os
import numpy as np
import metview as mv

###################################################################################################
# CODE DESCRIPTION
# 22_Plot_Empirical_Quantile_Analysis.py plots the outcomes of the empirical quantile analysis for all the considered
# nwp models.
# Code runtime: up to 1 minute.

# DESCRIPTION OF INPUT PARAMETERS
# YearS (number, in YYYY format): start year to consider.
# YearF (number, in YYYY format): final year to consider.
# Acc (number, in hours): rainfall accumulation period.
# MinDays_Perc (float, from 0 to 1): % of min n. of days with valid obs at each location.
# MaxPerc (integer or float, from 0 to 100 - not included): max percentile considered when sampling the obs and nwp rainfall realizations. 
# SystemNWP_list (list of string): list of NWP model climatologies.
# Git_Repo (string): path of local github repository.
# DirIN (string): relative path for the directory containing the quantile differences for the NWP modelled rainfall realizations.
# DirOUT (string): relative path for the directory containing the map plots for the quantile differences.

# INPUT PARAMETERS
YearS = 2000
YearF = 2019
Acc = 24
MinDays_Perc = 0.75
MaxPerc = 99.97
SystemNWP_list = ["Reanalysis/ERA5_ecPoint", "Reanalysis/ERA5_EDA", "Reanalysis/ERA5", "Reforecasts/ECMWF_46r1"]
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_ClimateNWP_4Points"
DirIN = "Data/Compute/21_Empirical_Quantile_Analysis"
DirOUT = "Data/Plot/22_Empirical_Quantile_Analysis"
###################################################################################################


# Plotting the outcomes of the empirical quantile analysis for the nwp models
print()
print("Plotting the outcomes of the empirical quantile analysis for the nwp models: ")
for SystemNWP in SystemNWP_list:
      
      print(" - " + SystemNWP)

      # Reading the quantile differences for a specific nwp model
      MainDirIN = Git_Repo + "/" + DirIN + "/MinDays_Perc_" + str(MinDays_Perc*100) + "/MaxPerc_" + str(MaxPerc) + "/" +f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF) + "/" + SystemNWP
      perc_diff = np.load(MainDirIN + "/Perc_Diff.npy")
      perc_list = np.load(MainDirIN + "/Perc_List.npy")
      lats = np.load(MainDirIN + "/" + "Stn_lats.npy")
      lons = np.load(MainDirIN + "/" + "Stn_lons.npy")

      # Computing the median for the whole quantile difference distribution
      perc_diff_median = np.nanmedian(perc_diff, axis=1)
      
      # Computing the median for the quantile difference in the tail's distribution
      perc_diff_tail = perc_diff[:, np.where(perc_list>90)[0]]
      perc_diff_tail_median = np.median(perc_diff_tail, axis=1)

      # Converting into geopoints the median of the quantile differences in the whole distribution, and the median of the quantile differences in the tail
      perc_diff_median_geo = mv.create_geo(
            type = "xyv",
            latitudes =  lats,
            longitudes = lons,
            values = perc_diff_median
            )
      
      perr_diff_tail_median_geo = mv.create_geo(
            type = "xyv",
            latitudes =  lats,
            longitudes = lons,
            values = perc_diff_tail_median
            )
      
      # Plotting the median of the quantile differences in the whole distribution, and the median of the quantile differences in the tail
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

      Thr_zero = 0.1
      markers = mv.psymb(
            symbol_type = "marker",
            symbol_table_mode = "on",
            symbol_quality = "high",
            symbol_min_table = [-15, -Thr_zero, Thr_zero], 
            symbol_max_table = [-Thr_zero, Thr_zero, 15],
            symbol_marker_table = [15, 15, 15],
            symbol_colour_table = [
                  "rgb(0.1339,0.03998,0.7443)", # -15, -0.01
                  "rgb(0.7,0.7,0.7)", # -0.01, 0.01 
                  "rgb(1,0,0.498)"], # 0.01, 15
            symbol_height_table = [0.2, 0.2, 0.2]
            )
      
      title_diff_median = mv.mtext(
            text_line_count = 1,
            text_line_1 = "Median of quantile differences for " + SystemNWP,
            text_colou ="charcoal",
            text_font ="arial",
            text_font_size = 4
            )
      
      title_diff_tail_mean = mv.mtext(
            text_line_count = 1,
            text_line_1 = "Mean of quantile differences in the tail of the distribution (>98th percentile) for " + SystemNWP,
            text_colou ="charcoal",
            text_font ="arial",
            text_font_size = 4
            )

      legend = mv.mlegend(
            legend_text_colour = "charcoal",
            legend_text_font = "arial",
            legend_text_font_size = 2,
            legend_entry_plot_direction = "row",
            legend_automatic_poistion = "top",
            )

      # Saving the map plots
      MainDirOUT = Git_Repo + "/" + DirOUT + "/MinDays_Perc_" + str(MinDays_Perc*100) + "/MaxPerc_" + str(MaxPerc) + "/" f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF) + "/" + SystemNWP
      if not os.path.exists(MainDirOUT):
            os.makedirs(MainDirOUT)
      
      png = mv.png_output(output_width = 5000, output_name = MainDirOUT + "/Perc_Diff_Median")
      mv.setoutput(png)
      mv.plot(coastlines, perc_diff_median_geo, markers, title_diff_median, legend)

      png = mv.png_output(output_width = 5000, output_name = MainDirOUT + "/perc_diff_tail_median")
      mv.setoutput(png)
      mv.plot(coastlines, perr_diff_tail_median_geo, markers, title_diff_tail_mean, legend)