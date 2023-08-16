import os
from os.path import exists
from datetime import date
import numpy as np
import metview as mv

#############################################################
# CODE DESCRIPTION
# 07a_Plot_AlignOBS-GridCPC.py plots a map with the aligned gridded CPC  
# rainfall observations.
# Code runtime: negligible.

# DESCRIPTION OF INPUT PARAMETERS
# Date (date, in YYYY-MM-DDformat): date to plot
# Git_repo (string): path of local github repository
# DirIN (string): relative path for the input directory
# DirOUT (string): relative path for the output directory

# INPUT PARAMETERS
Date = date(2019,9,19)
Git_repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/ecPoint_Climate"
DirIN = "Data/Compute/07_AlignedOBS-Extract-GridCPC"
DirOUT = "Data/Plot/07a_AlignOBS-GridCPC"
#############################################################


# Reading the aligned gridded CPC rainfall observations
print(" ")
print("Reading the aligned gridded CPC point rainfall observations and the correspondent metadata (i.e., lats/lons/dates)")
MainDirIN = Git_repo + "/" + DirIN
lats = np.load(MainDirIN + "/stn_lats.npy")
lons = np.load(MainDirIN + "/stn_lons.npy")
dates = np.load(MainDirIN + "/dates.npy")
obs = np.load(MainDirIN + "/obs.npy")

# Extracting the observations for the considered date
DateSTR = Date.strftime("%Y%m%d")
ind_date = np.where(dates == DateSTR)[0][0]
obs_date = obs[:,ind_date]

# Creating the geopoint file to plot
geo = mv.create_geo(
      type = 'xyv',
      latitudes = lats,
      longitudes = lons,
      values = obs_date,
      )

# Plotting the observations
coastlines = mv.mcoast(
    map_coastline_thickness = 1,
    map_coastline_resolution = "medium",
    map_boundaries = "on",
    map_boundaries_colour = "charcoal",
    map_boundaries_thickness = 1,
    map_grid_colour = "grey",
    map_label_right = "off",
    map_label_top = "off",
    map_label_height = 0.75,
    map_grid_latitude_increment = 30,
    map_grid_longitude_increment = 60
    )

legend = mv.mlegend(
    legend_text_colour = "charcoal",
    legend_text_font = "arial",
    legend_text_font_size = 0.3,
    legend_entry_plot_direction = "row",
    legend_box_blanking = "on",
    legend_entry_text_width = 20
    )

symbol_plotting = mv.msymb(
    legend = "on",
    symbol_type = "marker",
    symbol_table_mode = "on",
    symbol_min_table = [0,0.5,2,5,10,20,30,40,50,60,80,100,125,150,200,300,500],
    symbol_max_table = [0.5,2,5,10,20,30,40,50,60,80,100,125,150,200,300,500,5000],
    symbol_marker_table = [15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,20],
    symbol_colour_table = ["charcoal","RGB(0.75,0.95,0.93)","RGB(0.45,0.93,0.78)","RGB(0.07,0.85,0.61)","RGB(0.53,0.8,0.13)","RGB(0.6,0.91,0.057)","RGB(0.9,1,0.4)","RGB(0.89,0.89,0.066)","RGB(1,0.73,0.0039)","RGB(1,0.49,0.0039)","red","RGB(0.85,0.0039,1)","RGB(0.63,0.0073,0.92)","RGB(0.37,0.29,0.91)","RGB(0.04,0.04,0.84)","RGB(0.042,0.042,0.43)","RGB(0.7,0.7,0.7)"],
    symbol_height_table = [ 0.1,0.2,0.2,0.2,0.2,0.2,0.3,0.3,0.3,0.3,0.4,0.4,0.4,0.4,0.4,0.6]
    )

# Saving the plot
MainDirOUT = Git_repo + "/" + DirOUT
if not exists(MainDirOUT):
      os.makedirs(MainDirOUT)
png = mv.png_output(output_name = MainDirOUT + "/AligOBS_GridCPC_" + Date.strftime("%Y%m%d"))
mv.setoutput(png)
mv.plot(coastlines, symbol_plotting, legend, geo)