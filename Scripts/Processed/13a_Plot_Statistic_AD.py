import os
from os.path import exists
import numpy as np
import metview as mv

#############################################################################################################################################
# CODE DESCRIPTION
# 13a_Plot_StatisticAD.py plots whether the Anderson-Darling statistic rejects or not that the samples come from the same distribution. 
# The script generates the map plots as static svg figures or in a Metview interactive window.
# Code runtime: negligible.

# DESCRIPTION OF INPUT PARAMETERS
# Acc (number, in hours): rainfall accumulation period.
# RunType (string): type of run. Valid values are:
#                                   - "Interactive": to open the plot on an interacive Metview window.
#                                   - "Static": to save the plot on a static svg map.
# SystemFC_list (list of string): list of forecasting systems to consider.
# MinDays_Perc_list (list of number, from 0 to 1): list of percentages of minimum n. of days over the considered period with valid observations to compute the climatologies.
# NameOBS_list (list of strings): list of the names of the observations to quality check
# Coeff_Grid2Point_list (list of integer number): list of coefficients used to compare CPC's gridded rainfall values with  STVL's point rainfall observations. 
# Season_list (list of strings): seasons for the climatologies to plot. Valid values are:
#                                                               - "Year": for the year climatology
#                                                               - "DJF": for the seasonal climatology, winter months (December, January, February)
#                                                               - "MAM": for the seasonal climatology, spring months (March, April, May)
#                                                               - "JJA": for the seasonal climatology, summer months (June, July, August)
#                                                               - "SON": for the seasonal climatology, autumn months (September, October, November)
# Git_repo (string): path of local github repository.
# DirIN (string): relative path for the input directory.
# DirOUT (string): relative path for the output directory .

# INPUT PARAMETERS
Acc = 24
RunType = "Interactive"
SystemFC_list = ["ERA5_EDA_ShortRange"]
MinDays_Perc_list = [0.75]
NameOBS_list = ["08_AlignOBS_CleanSTVL"]
Coeff_Grid2Point_list = [20]
Season_list = ["Year"]
Git_repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/ecPoint_Climate"
DirIN = "Data/Compute/13_Statistic_AD"
DirOUT= "Data/Plot/13a_Statistic_AD" 
#############################################################################################################################################

# Costum functions

def plot_statisticAD(RunType, Season, Title_text_line_1, Title_text_line_2, DirIN, DirOUT):

      # Reading the considered climatology and the correspondent percentiles, and the rainfall stations coordinates
      StatisticAD_array = np.load(DirIN + "/StatisticAD_" + Season + ".npy")
      CriticalVal_array = np.load(DirIN + "/CriticalVal_" + Season + ".npy")
      lats = np.load(DirIN + "/" + "Stn_lats_" + Season + ".npy")
      lons = np.load(DirIN + "/" + "Stn_lons_" + Season + ".npy")
    
      # Define when to reject or not-reject the null hypothesis of the Anderson-Darling test
      # NOTE: when statistic_AD > critical_AD then the null hypothesis that the two random samples come from the same distribution can be rejected at the 0.1% level of confidence.
      test_AD = (StatisticAD_array < CriticalVal_array) * 1 # values to 1 are given to the locations where the modelled climatology is representative of the observational climatology
      
      # test_AD = np.empty(StatisticAD_array.shape[0]) + np.nan
      # test_AD = np.where(StatisticAD_array[:,0] < CriticalVal_array[0][0], test_AD, 1) # the two samples come from the same distribution
      # test_AD = np.where(StatisticAD_array[:,0] > CriticalVal_array[0][0], test_AD, 0) # the two samples do not come from the same distribution

      # Converting the climatology to geopoint
      not_reject_geo = mv.create_geo(
            type = 'xyv',
            latitudes =  lats,
            longitudes = lons,
            values = test_AD
            )

      # Plotting the A-D statistic
      coastlines = mv.mcoast(
            map_coastline_thickness = 2,
            map_coastline_resolution = "medium",
            map_boundaries = "on",
            map_boundaries_colour = "black",
            map_boundaries_thickness = 1,
            map_grid = "off",
            map_label = "off"
            )
      
      Europe = mv.geoview(
        map_projection      = "lambert",
        map_area_definition = "corners",
        area                = [23.12,-9.55,56.31,87.75]
        )

      if RunType == "Static":
            symbol_height = 0.1
      else:
            symbol_height = 0.2

      markers = mv.psymb(
            symbol_type = "MARKER",
            symbol_table_mode = "ON",
            legend = "ON",
            symbol_quality = "HIGH",
            symbol_min_table = [ -0.5, 0.5], # markers with values between -0.5 and 0.5 (i.e. = 0); markers with values between 0.5 and 1.5 (i.e. = 1)
            symbol_max_table = [0.5,1.5],
            symbol_marker_table = [ 15,15],
            symbol_colour_table = ["magenta","green"], 
            symbol_height_table = [ symbol_height,symbol_height]
            )

      legend = mv.mlegend(
            legend_text_font = "arial",
            legend_text_font_size = 0.30
            )
      
      title = mv.mtext(
            text_line_count = 3,
            text_line_1 = Title_text_line_1,
            text_line_2 =  Title_text_line_2,
            text_line_3 = " ",
            text_colou ="purplish_blue",
            text_font ="courier",
            text_font_size = 0.4
            )

      # Create plots
      if RunType == "Interactive":
            
            mv.plot(not_reject_geo, coastlines, markers, legend, title)
      
      else:
            
            # Global map
            svg = mv.png_output(output_name = DirOUT + "/" + Season)
            mv.setoutput(svg)
            mv.plot(not_reject_geo, coastlines, markers, legend, title)
            
            # Zoom for Europe
            svg = mv.png_output(output_name = DirOUT + "/" + Season + "_Europe")
            mv.setoutput(svg)
            mv.plot(not_reject_geo, Europe, coastlines, markers, legend, title)

#######################################################################################################################

for SystemFC in SystemFC_list:

      for MinDays_Perc in MinDays_Perc_list:

            for NameOBS in NameOBS_list:

                  if (NameOBS == "06_AlignOBS_Combine_Years_RawSTVL") or (NameOBS == "07_AlignOBS_Extract_GridCPC"):

                        print(" ")
                        print("Plotting the Anderson-Darling statistic for " + SystemFC + " for " + NameOBS + " with a minimum of " + str(int(MinDays_Perc*100)) + "% of days over the considered period with valid observations to compute the climatologies")
                        Dataset_temp = NameOBS.split("_")[-1]     
                        Title_text_line_2 = Dataset_temp + " - Minum of " + str(int(MinDays_Perc*100)) + "% of days with valid observations" 
                        
                        # Setting main input/output directories
                        MainDirIN = Git_repo + "/" + DirIN + "/" + SystemFC + "/MinDays_Perc" + str(int(MinDays_Perc*100)) + "/" + NameOBS
                        MainDirOUT = Git_repo + "/" + DirOUT + "/" + SystemFC + "/MinDays_Perc" + str(int(MinDays_Perc*100)) + "/" + NameOBS
                        if not exists(MainDirOUT):
                              os.makedirs(MainDirOUT)

                        # Plotting climatologies
                        for Season in Season_list:               
                              print(" - " + Season)
                              Title_text_line_1 = "Anderson-Darling Statistic for " + SystemFC + " for " + Season + " climatology"
                              plot_statisticAD(RunType, Season, Title_text_line_1, Title_text_line_2, MainDirIN, MainDirOUT)

                  elif NameOBS == "08_AlignOBS_CleanSTVL":

                        for Coeff_Grid2Point in Coeff_Grid2Point_list:
                                    
                              print(" ")
                              print("Plotting the Anderson-Darling statistic for " + SystemFC + " for " + NameOBS + " (Coeff_Grid2Point=" + str(Coeff_Grid2Point) + ") with a minimum of " + str(int(MinDays_Perc*100)) + "% of days over the considered period with valid observations to compute the climatologies")
                              Dataset_temp = NameOBS.split("_")[-1] + " (Coeff_Grid2Point=" + str(Coeff_Grid2Point) + ")"
                              Title_text_line_2 = Dataset_temp + " - Minum of " + str(int(MinDays_Perc*100)) + "% of days with valid observations" 

                              # Setting main input/output directories
                              MainDirIN = Git_repo + "/" + DirIN + "/" + SystemFC + "/MinDays_Perc" + str(int(MinDays_Perc*100)) + "/" + NameOBS + "/Coeff_Grid2Point_" + str(Coeff_Grid2Point)
                              MainDirOUT = Git_repo + "/" + DirOUT + "/" + SystemFC + "/MinDays_Perc" + str(int(MinDays_Perc*100)) + "/" + NameOBS + "/Coeff_Grid2Point_" + str(Coeff_Grid2Point)
                              if not exists(MainDirOUT):
                                    os.makedirs(MainDirOUT)

                              # Plotting climatologies
                              for Season in Season_list:               
                                    print(" - " + Season)
                                    Title_text_line_1 = "Anderson-Darling Statistic for " + SystemFC + " for " + Season + " climatology"
                                    plot_statisticAD(RunType, Season, Title_text_line_1, Title_text_line_2, MainDirIN, MainDirOUT)