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
# RP_2_Plot_list (list of integers, in years): list of return periods to compute.
# Coeff_Grid2Point_list (list of integers): list of coefficients that make the CPC's gridded rainfall values comparable with STVL's point rainfall observations.
# MinDays_Perc_list (list of floats, from 0 to 1): percentage of min n. of days with valid obs at each location.
# NameOBS_list (list of strings): list of the observational datasets to quality check.
# Git_Repo (string): path of local GitHub repository.
# DirIN (string): relative path for the input directory.
# DirOUT (string): relative path for the output directory.

# INPUT PARAMETERS
YearS = 2000
YearF = 2019
Acc = 24
RP_2_Plot_list = [1, 2, 5, 10, 20]
Coeff_Grid2Point_list = [2, 5, 10, 20, 50, 100, 200, 500, 1000]
MinDays_Perc_list = [0.5, 0.75]
NameOBS_list = ["08_AlignOBS_Combine_Years_RawSTVL", "10_AlignOBS_CleanSTVL"]
Git_Repo = "/ec/vol/ecpoint_dev/mofp/papers_2_write/Verif_ClimateNWP_4Points"
DirIN = "Data/Compute/12_Climate_OBS"
DirOUT= "Data/Plot/13_Climate_OBS"
######################################################################


# PLOT THE CLIMATOLOGY FROM OBSERVATIONS
def plot_climate_obs(MinDays_Perc, RP_list, DirIN, DirOUT):

    # Reading the considered climatology and the correspondent percentiles, and the rainfall stations coordinates
    climate_array = np.load(DirIN + "/Climate.npy")
    lats = np.load(DirIN + "/Stn_lats.npy")
    lons = np.load(DirIN + "/Stn_lons.npy")
    RP_list = np.load(DirIN + "/RP.npy")
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
                map_coastline_resolution = "medium",
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

            markers_small = mv.psymb(
                symbol_type = "MARKER",
                symbol_table_mode = "ON",
                legend = "ON",
                symbol_quality = "HIGH",
                symbol_min_table = [0,0.5,2,5,10,20,30,40],
                symbol_max_table = [0.5,2,5,10,20,30,40,50],
                symbol_marker_table = [15,15,15,15,15,15,15,15],
                symbol_colour_table = ["black","RGB(0.75,0.95,0.93)","RGB(0.45,0.93,0.78)","RGB(0.07,0.85,0.61)","RGB(0.53,0.8,0.13)","RGB(0.6,0.91,0.057)","RGB(0.9,1,0.4)","RGB(0.89,0.89,0.066)"],
                symbol_height_table = [ 0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3]
                )
            
            markers_50 = mv.psymb( # we want to make sure that the biggest totals are plot on top
                symbol_type = "MARKER",
                symbol_table_mode = "ON",
                legend = "ON",
                symbol_quality = "HIGH",
                symbol_min_table = [50],
                symbol_max_table = [60],
                symbol_marker_table = [15],
                symbol_colour_table = ["RGB(1,0.73,0.0039)"],
                symbol_height_table = [0.3]
                )
            
            markers_60 = mv.psymb(
                symbol_type = "MARKER",
                symbol_table_mode = "ON",
                legend = "ON",
                symbol_quality = "HIGH",
                symbol_min_table = [60],
                symbol_max_table = [80],
                symbol_marker_table = [15],
                symbol_colour_table = ["RGB(1,0.49,0.0039)"],
                symbol_height_table = [0.3]
                )
            
            markers_80 = mv.psymb(
                symbol_type = "MARKER",
                symbol_table_mode = "ON",
                legend = "ON",
                symbol_quality = "HIGH",
                symbol_min_table = [80],
                symbol_max_table = [100],
                symbol_marker_table = [15],
                symbol_colour_table = ["red"],
                symbol_height_table = [0.3]
                )
            
            markers_100 = mv.psymb(
                symbol_type = "MARKER",
                symbol_table_mode = "ON",
                legend = "ON",
                symbol_quality = "HIGH",
                symbol_min_table = [100],
                symbol_max_table = [125],
                symbol_marker_table = [15],
                symbol_colour_table = ["RGB(0.85,0.0039,1)"],
                symbol_height_table = [0.3]
                )
            
            markers_125 = mv.psymb(
                symbol_type = "MARKER",
                symbol_table_mode = "ON",
                legend = "ON",
                symbol_quality = "HIGH",
                symbol_min_table = [125],
                symbol_max_table = [150],
                symbol_marker_table = [15],
                symbol_colour_table = ["RGB(0.63,0.0073,0.92)"],
                symbol_height_table = [0.3]
                )
            
            markers_150 = mv.psymb(
                symbol_type = "MARKER",
                symbol_table_mode = "ON",
                legend = "ON",
                symbol_quality = "HIGH",
                symbol_min_table = [150],
                symbol_max_table = [200],
                symbol_marker_table = [15],
                symbol_colour_table = ["RGB(0.37,0.29,0.91)"],
                symbol_height_table = [0.3]
                )
            
            markers_200 = mv.psymb(
                symbol_type = "MARKER",
                symbol_table_mode = "ON",
                legend = "ON",
                symbol_quality = "HIGH",
                symbol_min_table = [200],
                symbol_max_table = [300],
                symbol_marker_table = [15],
                symbol_colour_table = ["RGB(0.04,0.04,0.84)"],
                symbol_height_table = [0.3]
                )
            
            markers_300 = mv.psymb(
                symbol_type = "MARKER",
                symbol_table_mode = "ON",
                legend = "ON",
                symbol_quality = "HIGH",
                symbol_min_table = [300],
                symbol_max_table = [500],
                symbol_marker_table = [15],
                symbol_colour_table = ["RGB(0.042,0.042,0.43)"],
                symbol_height_table = [0.3]
                )
            
            markers_500 = mv.psymb(
                symbol_type = "MARKER",
                symbol_table_mode = "ON",
                legend = "ON",
                symbol_quality = "HIGH",
                symbol_min_table = [500],
                symbol_max_table = [1000],
                symbol_marker_table = [15],
                symbol_colour_table = ["RGB(0.8,0.8,0.8)"],
                symbol_height_table = [0.3]
                )
            
            markers_1000 = mv.psymb(
                symbol_type = "MARKER",
                symbol_table_mode = "ON",
                legend = "ON",
                symbol_quality = "HIGH",
                symbol_min_table = [1000],
                symbol_max_table = [50000],
                symbol_marker_table = [15],
                symbol_colour_table = ["RGB(0.4,0.4,0.4)"],
                symbol_height_table = [0.3]
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
            if not os.path.exists(DirOUT):
                os.makedirs(DirOUT)
            png = mv.png_output(output_width = 5000, output_name = DirOUT + "/Climate_" + str(RP) + "RP")
            mv.setoutput(png)
            mv.plot(climate_RP_geo, coastlines, markers_small, markers_50, markers_60,markers_80, markers_100, markers_125,  markers_150, markers_200, markers_300, markers_500, markers_1000, legend, title)


###########################################################################

# Plot the climatologies for a different number of minimum days with valid observations 
for MinDays_Perc in MinDays_Perc_list:

    # Plot the climatologies from raw or clean point observations
    for NameOBS in NameOBS_list:

        if NameOBS == "08_AlignOBS_Combine_Years_RawSTVL": # raw

            MainDirIN = Git_Repo + "/" + DirIN + "/" + NameOBS + "/MinDays_Perc_" + str(MinDays_Perc*100) + "/" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF)
            MainDirOUT = Git_Repo + "/" + DirOUT + "/" + NameOBS + "/MinDays_Perc_" + str(MinDays_Perc*100) + "/" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF)
            plot_climate_obs(MinDays_Perc, RP_2_Plot_list, MainDirIN, MainDirOUT)
        
        if NameOBS == "10_AlignOBS_CleanSTVL": # clean
                
            for Coeff_Grid2Point in Coeff_Grid2Point_list:
                
                MainDirIN = Git_Repo + "/" + DirIN + "/" + NameOBS + "/Coeff_Grid2Point_" + str(Coeff_Grid2Point) + "/MinDays_Perc_" + str(MinDays_Perc*100)  + "/" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF)
                MainDirOUT = Git_Repo + "/" + DirOUT + "/" + NameOBS + "/Coeff_Grid2Point_" + str(Coeff_Grid2Point) + "/MinDays_Perc_" + str(MinDays_Perc*100)  + "/" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF)
                plot_climate_obs(MinDays_Perc, RP_2_Plot_list, MainDirIN, MainDirOUT)