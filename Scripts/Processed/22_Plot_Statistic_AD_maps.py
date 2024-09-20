import os
import numpy as np
import metview as mv

###################################################################################################
# CODE DESCRIPTION
# 20_Plot_Statistic_AD_maps.py plots the Anderson-Darling statistic between the observational and the NWP modelled
# rainfall distributions.
# Note:
# The Anderson-Darling test for k-samples tests the null hypothesis that k-samples are drawn from the same population 
# without having to specify the distribution function of that population. 
#     1. If the Anderson-Darling statistic is bigger than the critical values, this means that the test results are significant at 
#         every significance level. Therefore, we would reject the null hypothesis of the test no matter which significance 
#         level we choose to use. Thus, we have sufficient evidence to say that the samples are not drawn from the same
#         population.
#     2. If the Anderson-Darling statistic is smaller than the critical values, this means that the test results are not 
#         significant at any significance level. Therefore, we would not reject the null hypothesis of the test. Thus, we don’t 
#         have sufficient evidence to say that the samples are not drawn from the same population.
# Code runtime: ~ 1 minute.

# DESCRIPTION OF INPUT PARAMETERS
# YearS (number, in YYYY format): start year to consider.
# YearF (number, in YYYY format): final year to consider.
# Acc (number, in hours): rainfall accumulation period.
# SystemNWP_list (list of string): list of NWP model climatologies.
# Git_Repo (string): path of local github repository.
# DirIN (string): relative path for the directory containing the values of the AD statistic.
# DirOUT (string): relative path for the directory containing the AD statistic.

# INPUT PARAMETERS
YearS = 2000
YearF = 2019
Acc = 24
MinDays_Perc = 0.75
NumPer = 100
SystemNWP_list = ["Reforecasts/ECMWF_46r1"]
#SystemNWP_list = ["Reforecasts/ECMWF_46r1", "Reanalysis/ERA5_EDA", "Reanalysis/ERA5", "Reanalysis/ERA5_ecPoint"]
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_ClimateNWP_4Points"
DirIN = "Data/Compute/19_Statistic_AD"
DirOUT = "Data/Plot/20_Statistic_AD_maps"
###################################################################################################

# Plotting the Anderson-Darling statistic for different NWP modelled climatologies
print()
print("Plotting the Anderson-Darling statistic for the NWP modelled climatology: ")
for SystemNWP in SystemNWP_list:
      
      print(" - " + SystemNWP)

      # Reading the considered NWP modelled climatology
      MainDirIN = Git_Repo + "/" + DirIN + "/MinDays_Perc_" + str(MinDays_Perc*100) + "/" + "NumPer_" + f'{NumPer:03d}' +  + "/" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF) + "/" + SystemNWP
      #MainDirIN = Git_Repo + "/" + DirIN + "/tp_" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF) + "/" + SystemNWP
      Stat_AD = np.load(MainDirIN + "/StatisticAD.npy")
      Crit_Val = np.load(MainDirIN + "/CriticalVal.npy")
      #Pvalue = np.load(MainDirIN + "/Pvalue.npy")
      lats = np.load(MainDirIN + "/" + "Stn_lats.npy")
      lons = np.load(MainDirIN + "/" + "Stn_lons.npy")

      # Defining when to reject or not-reject the null hypothesis of the Anderson-Darling test
      # ind = np.where(Pvalue < 0.1)
#       test_AD = 0 * Stat_AD
#       test_AD[ind] = 1
      
      test_AD = (Stat_AD < Crit_Val) * 1 # the value of 1 is given to those locations where the modelled climatology is representative of the observational climatology
      
      # Converting the test A-D to geopoint
      test_AD_geo = mv.create_geo(
            type = 'xyv',
            latitudes =  lats,
            longitudes = lons,
            values = test_AD
            )

      # Plotting the A-D statistic
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
            symbol_type = "MARKER",
            symbol_table_mode = "ON",
            legend = "off",
            symbol_quality = "HIGH",
            symbol_min_table = [-0.5,0.5], #only the 1s are plotted in the map
            symbol_max_table = [0.5,1.5],
            symbol_marker_table = [15,15],
            symbol_colour_table = ["rgb(1,0,0.498)","rgb(0,0.498,1)"], 
            symbol_height_table = [0.15,0.15]
            )
      
      Title_text_line_1 = "Anderson-Darling test for " + SystemNWP
      title = mv.mtext(
            text_line_count = 2,
            text_line_1 = Title_text_line_1,
            text_line_2 = " ",
            text_colou ="charcoal",
            text_font ="arial",
            text_font_size = 5
            )

      legend = mv.mlegend(
            legend_text_colour = "charcoal",
            legend_text_font_size = 0.5,
            legend_display_type = "disjoint",
            legend_text_composition = "user_text_only",
            legend_user_lines = ["nwp clim NOT representative of obs clim","nwp clim REPESENTATIVE of obs clim"],
            legend_entry_text_width = 50.00,
            )

      # Saving the map plots
      # MainDirOUT = Git_Repo + "/" + DirOUT + "/tp_" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF) + "/" + SystemNWP
#       if not os.path.exists(MainDirOUT):
#             os.makedirs(MainDirOUT)
#       png = mv.png_output(output_width = 5000, output_name = MainDirOUT + "/TestAD")
#       mv.setoutput(png)
      mv.plot(test_AD_geo, coastlines, markers, legend, title)