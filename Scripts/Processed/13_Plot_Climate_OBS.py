import os
import numpy as np
import metview as mv

######################################################################
# CODE DESCRIPTION
# 02_Plot_Climate_OBS.py plots the observational (point) rainfall climatologies.
# Code runtime: negligible.

# DESCRIPTION OF INPUT PARAMETERS
# YearS (integer, in YYYY format): start year to consider.
# YearF (integer, in YYYY format): final year to consider.
# Acc (integer, in hours): rainfall accumulation period.
# MinDays_Perc (float, from 0 to 1): % of min n. of days with valid obs at each location.
# RP_2_Plot_list (list of integers, in years): list of return periods to plot.
# Git_Repo (string): path of local GitHub repository.
# DirIN (string): relative path for the input directory.
# DirOUT (string): relative path for the output directory.

# INPUT PARAMETERS
YearS = 2000
YearF = 2019
Acc = 24
MinDays_Perc = 0.5
RP_2_Plot_list = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_ClimateNWP_4Points"
DirIN = "Data/Compute/12_Climate_OBS/Coeff_Grid2Point_20"
DirOUT= "Data/Plot/13_Climate_OBS"
######################################################################


# Setting the main input/output directories
MainDirIN = Git_Repo + "/" + DirIN + "/MinDays_Perc_" + str(MinDays_Perc*100) + "/" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF)
MainDirOUT = Git_Repo + "/" + DirOUT + "/MinDays_Perc_" + str(MinDays_Perc*100) + "/" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF)
if not os.path.exists(MainDirOUT):
    os.makedirs(MainDirOUT)

# Reading the considered climatology and the correspondent percentiles, and the rainfall stations coordinates
climate_array = np.load(MainDirIN + "/Climate.npy")
lats = np.load(MainDirIN + "/Stn_lats.npy")
lons = np.load(MainDirIN + "/Stn_lons.npy")
RP_list = np.load(MainDirIN + "/RP.npy")
RP_list = (np.round(RP_list, decimals = 5)).astype('float64')

# Plotting the observational climatologies 
for ind_RP in range(len(RP_2_Plot_list)):

    RP = RP_2_Plot_list[ind_RP]
    index = np.where(RP_list == RP)[0]

    if len(index) == 0: 
                  
        print("     - The " + str(RP) + "-year return period is not available") 

    else:
                  
        print("     - For the " + str(RP) + "-year return period")
        climate_RP = climate_array[:,index]

        # Converting the climatology to geopoint
        climate_RP_geo = mv.create_geo(
            type = 'xyv',
            latitudes =  lats,
            longitudes = lons,
            values = climate_RP
            )

        # Plotting the climatology
        coastlines = mv.mcoast(
            map_coastline_colour = "charcoal",
            map_coastline_thickness = 5,
            map_coastline_resolution = "low",
            map_coastline_sea_shade = "on", # comments this line to see the rainfall totals over the sea
            map_coastline_sea_shade_colour = "white", # # comments this line to see the rainfall totals over the sea
            map_boundaries = "on",
            map_boundaries_colour = "charcoal",
            map_boundaries_thickness = 5,
            map_administrative_boundaries = "of",
            map_grid_latitude_increment = 30,
            map_grid_longitude_increment = 60,
            map_label_right = "off",
            map_label_top = "off",
            map_label_colour = "charcoal",
            map_grid_thickness = 5,
            map_grid_colour = "charcoal",
            map_label_height = 3
            )

        markers = mv.psymb(
            symbol_type = "MARKER",
            symbol_table_mode = "ON",
            legend = "ON",
            symbol_quality = "HIGH",
            symbol_min_table = [ 0,0.5,2,5,10,20,30,40,50,60,80,100,125,150,200,300,500, 1000],
            symbol_max_table = [ 0.5,2,5,10,20,30,40,50,60,80,100,125,150,200,300,500,1000, 50000],
            symbol_marker_table = [ 15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15],
            symbol_colour_table = ["black","RGB(0.75,0.95,0.93)","RGB(0.45,0.93,0.78)","RGB(0.07,0.85,0.61)","RGB(0.53,0.8,0.13)","RGB(0.6,0.91,0.057)","RGB(0.9,1,0.4)","RGB(0.89,0.89,0.066)","RGB(1,0.73,0.0039)","RGB(1,0.49,0.0039)","red","RGB(0.85,0.0039,1)","RGB(0.63,0.0073,0.92)","RGB(0.37,0.29,0.91)","RGB(0.04,0.04,0.84)","RGB(0.042,0.042,0.43)","RGB(0.8,0.8,0.8)","RGB(0.4,0.4,0.4)"],
            symbol_height_table = [ 0.1,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2]
            )

        legend = mv.mlegend(
            legend_text_colour = "charcoal",
            legend_text_font = "arial",
            legend_text_font_size = 3,
            legend_entry_plot_direction = "row",
            legend_automatic_poistion = "top",
            )

        title = mv.mtext(
            text_line_count = 2,
            text_line_1 = f'{Acc:02d}' + " rainfall climatology (" + str(RP) + " year return period, with minimum " + str(MinDays_Perc*100) + "% of valid obs) - Period: " + str(YearS) + " to " + str(YearF),
            text_line_2 = " ",
            text_colour = "charcoal",
            text_font = "arial",
            text_font_size = 4
            )

        # Create plots
        png = mv.png_output(output_width = 5000, output_name = MainDirOUT + "/Climate_" + str(RP) + "RP")
        mv.setoutput(png)
        mv.plot(climate_RP_geo, coastlines, markers, legend, title)
