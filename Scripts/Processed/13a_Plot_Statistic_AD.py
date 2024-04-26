import os
from os.path import exists
import numpy as np
import metview as mv

#############################################################################################################################################################################
# CODE DESCRIPTION
# 13a_Plot_Statistic_AD.py plots the locations where the Anderson-Darling test statistic asseses that the modelled climatologies are representative of the observational 
# climatologies. The script generates the map plots as static svg figures or in a Metview interactive window.
# Code runtime: negligible.

# DESCRIPTION OF INPUT PARAMETERS
# Acc (number, in hours): rainfall accumulation period.
# RunType (string): type of run. Valid values are:
#                                   - "Interactive": to open the plot on an interacive Metview window.
#                                   - "Static": to save the plot on a static svg map.
# SystemFC_list (list of string): list of forecasting systems to consider. Valid values are:
#                                   - Reforecasts_46r1
#                                   - ERA5_ShortRange
#                                   - ERA5_EDA_ShortRange
#                                   - ERA5_LongRange
#                                   - ERA5_EDA_LongRange
#                                   - ERA5_ecPoint/Grid_BC_VALS
#                                   - ERA5_ecPoint/Pt_BC_PERC
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
SystemFC_list = ["ERA5_EDA_ShortRange"] # "Reforecasts_46r1", "ERA5_ShortRange", "ERA5_EDA_ShortRange", "ERA5_LongRange", "ERA5_EDA_LongRange", "ERA5_ecPoint/Grid_BC_VALS", "ERA5_ecPoint/Pt_BC_PERC"
MinDays_Perc_list = [0.75]
NameOBS_list = ["08_AlignOBS_CleanSTVL"]
Coeff_Grid2Point_list = [20]
Season_list = ["Year", "DJF", "MAM", "JJA", "SON"]
Git_repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_GridClimate_4Points"
DirIN = "Data/Compute/13_Statistic_AD"
DirOUT= "Data/Plot/13a_Statistic_AD" 
#############################################################################################################################################################################

# Costum functions

def plot_statisticAD(RunType, Season, Title_text_line_1, Title_text_line_2, DirIN, DirOUT):

      # Reading the considered climatology and the correspondent percentiles, and the rainfall stations coordinates
      StatisticAD_array = np.load(DirIN + "/StatisticAD_" + Season + ".npy")
      CriticalVal_array = np.load(DirIN + "/CriticalVal_" + Season + ".npy")
      lats = np.load(DirIN + "/" + "Stn_lats_" + Season + ".npy")
      lons = np.load(DirIN + "/" + "Stn_lons_" + Season + ".npy")
    
      # Define when to reject or not-reject the null hypothesis of the Anderson-Darling test
      # Note: when statistic_AD > critical_AD then the null hypothesis that the two random samples come from the same distribution can be rejected at the 0.1% level of confidence.
      test_AD = (StatisticAD_array < CriticalVal_array) * 1 # the value of 1 is given to those locations where the modelled climatology is representative of the observational climatology
      
      # Converting the climatology to geopoint
      test_AD_geo = mv.create_geo(
            type = 'xyv',
            latitudes =  lats,
            longitudes = lons,
            values = test_AD
            )

      # Plotting the A-D statistic
      coastlines = mv.mcoast(
            map_coastline_thickness = 1,
            map_coastline_colour = "rgb(0.4902,0.4902,0.4902)",
            map_coastline_resolution = "low",
            map_boundaries = "on",
            map_boundaries_colour = "grey",
            map_boundaries_thickness = 1,
            map_grid = "on",
            map_grid_colour              = "rgb(0.7686,0.7686,0.7686)",
            map_grid_latitude_increment  = 30,
            map_grid_longitude_increment = 60,
            map_label = "on"
            )

      markers = mv.psymb(
            symbol_type = "MARKER",
            symbol_table_mode = "ON",
            legend = "off",
            symbol_quality = "HIGH",
            symbol_min_table = [-0.5,0.5], #only the 1s are plotted in the map
            symbol_max_table = [0.5,1.5],
            symbol_marker_table = [15,15],
            symbol_colour_table = ["rgb(0.9182,0.5387,0.007263)","rgb(0.2525,0.2525,0.9789)"], 
            symbol_height_table = [0.075,0.075]
            )
      
      title = mv.mtext(
            text_line_count = 4,
            text_line_1 = Title_text_line_1,
            text_line_2 =  Title_text_line_2,
            text_line_3 =  Title_text_line_3,
            text_line_4 = " ",
            text_colou ="charcoal",
            text_font ="courier",
            text_font_size = 0.4
            )

      # Create plots
      if RunType == "Interactive":
            
            mv.plot(test_AD_geo, coastlines, markers, title)
      
      else:
            
            svg = mv.svg_output(output_name = DirOUT + "/" + Season)
            mv.setoutput(svg)
            mv.plot(test_AD_geo, coastlines, markers, title)

#######################################################################################################################


# Setting plot title
Title_text_line_1 = "Locations where the FC climatology represents the OBS climatology according to Anderson-Darling test"
                                    
# Plotting the locations where the modelled climatology represents the observational climatology
for SystemFC in SystemFC_list:

      for MinDays_Perc in MinDays_Perc_list:

            for NameOBS in NameOBS_list:

                  if (NameOBS == "06_AlignOBS_Combine_Years_RawSTVL") or (NameOBS == "07_AlignOBS_Extract_GridCPC"):

                        print(" ")
                        print("Plotting the Anderson-Darling statistic for " + SystemFC + " for " + NameOBS + " with a minimum of " + str(int(MinDays_Perc*100)) + "% of days over the considered period with valid observations to compute the climatologies")
                        Dataset_temp = NameOBS.split("_")[-1]     
                        Title_text_line_3 = Dataset_temp + " - Minum of " + str(int(MinDays_Perc*100)) + "% of days with valid observations" 
                        
                        # Setting main input/output directories
                        MainDirIN = Git_repo + "/" + DirIN + "/" + SystemFC + "/MinDays_Perc" + str(int(MinDays_Perc*100)) + "/" + NameOBS
                        MainDirOUT = Git_repo + "/" + DirOUT + "/" + SystemFC + "/MinDays_Perc" + str(int(MinDays_Perc*100)) + "/" + NameOBS
                        if not exists(MainDirOUT):
                              os.makedirs(MainDirOUT)

                        # Plotting climatologies
                        for Season in Season_list:               
                              print(" - " + Season)
                              Title_text_line_2 = SystemFC + " - " + Season + " climatology"
                              plot_statisticAD(RunType, Season, Title_text_line_1, Title_text_line_2, MainDirIN, MainDirOUT)

                  elif NameOBS == "08_AlignOBS_CleanSTVL":

                        for Coeff_Grid2Point in Coeff_Grid2Point_list:
                                    
                              print(" ")
                              print("Plotting the Anderson-Darling statistic for " + SystemFC + " for " + NameOBS + " (Coeff_Grid2Point=" + str(Coeff_Grid2Point) + ") with a minimum of " + str(int(MinDays_Perc*100)) + "% of days over the considered period with valid observations to compute the climatologies")
                              Dataset_temp = NameOBS.split("_")[-1] + " (Coeff_Grid2Point=" + str(Coeff_Grid2Point) + ")"
                              Title_text_line_3 = Dataset_temp + " - Minum of " + str(int(MinDays_Perc*100)) + "% of days with valid observations" 

                              # Setting main input/output directories
                              MainDirIN = Git_repo + "/" + DirIN + "/" + SystemFC + "/MinDays_Perc" + str(int(MinDays_Perc*100)) + "/" + NameOBS + "/Coeff_Grid2Point_" + str(Coeff_Grid2Point)
                              MainDirOUT = Git_repo + "/" + DirOUT + "/" + SystemFC + "/MinDays_Perc" + str(int(MinDays_Perc*100)) + "/" + NameOBS + "/Coeff_Grid2Point_" + str(Coeff_Grid2Point)
                              if not exists(MainDirOUT):
                                    os.makedirs(MainDirOUT)

                              # Plotting climatologies
                              for Season in Season_list:               
                                    print(" - " + Season)
                                    Title_text_line_2 = SystemFC + " - " + Season + " climatology"
                                    plot_statisticAD(RunType, Season, Title_text_line_1, Title_text_line_2, MainDirIN, MainDirOUT)