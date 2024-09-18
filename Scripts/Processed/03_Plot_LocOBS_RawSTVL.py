import os
from os.path import exists
from datetime import date
import metview as mv

######################################################################
# CODE DESCRIPTION
# 03_Plot_LocOBS_RawSTVL.py plots a map with an example of the location of rainfall 
# stations reporting observations at different times of  the day.
# Code runtime: negligible.

# DESCRIPTION OF INPUT PARAMETERS
# YearS (integer, in YYYY format): start year to consider.
# YearF (integer, in YYYY format): final year to consider.
# Acc (integer, in hours): rainfall accumulation period.
# Date (date, in YYYY-MM-DDformat): date to plot.
# Dataset_list (list of strings): names of the considered datasets from stvl.
# Git_Repo (string): path of local GitHub repository.
# DirIN (string): relative path for the input directory.
# DirOUT (string): relative path for the output directory.

# INPUT PARAMETERS
YearS = 2000
YearF = 2019
Acc = 24
Date_2_Plot = date(2000,1,1)
Dataset_list = ["synop", "hdobs", "bom", "india", "efas", "vnm"]
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_ClimateNWP_4Points"
DirIN = "Data/Compute/01_UniqueOBS_Extract_FromReference_RawSTVL"
DirOUT = "Data/Plot/03_LocOBS_RawSTVL"
######################################################################


# Initializing the variables that will contain the rainfall observations at different reporting times
geo_00 = None
geo_01 = None
geo_03 = None
geo_04 = None
geo_05 = None
geo_06 = None
geo_12 = None

# Reading the rainfall observations at different reporting times
for Dataset in Dataset_list:

    TempFile = Git_Repo + "/" + DirIN + "/" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF) + "/" + Dataset + "/" + Date_2_Plot.strftime("%Y%m%d") + "/tp" + str(Acc) + "_obs_" + Date_2_Plot.strftime("%Y%m%d")
    FileIN_00 = TempFile + "00.geo"
    FileIN_01 = TempFile + "01.geo"
    FileIN_03 = TempFile +  "03.geo"
    FileIN_04 = TempFile + "04.geo"
    FileIN_05 = TempFile + "05.geo"
    FileIN_06 = TempFile + "06.geo"
    FileIN_12 = TempFile + "12.geo"

    if exists(FileIN_00):
        geo_00 = mv.merge(geo_00, mv.read(FileIN_00))

    if exists(FileIN_01):
        geo_01 = mv.merge(geo_01, mv.read(FileIN_01))

    if exists(FileIN_03):
        geo_03 = mv.merge(geo_03, mv.read(FileIN_03))

    if exists(FileIN_04):
        geo_04 = mv.merge(geo_04, mv.read(FileIN_04))

    if exists(FileIN_05):
        geo_05 = mv.merge(geo_05, mv.read(FileIN_05))

    if exists(FileIN_06):
        geo_06 = mv.merge(geo_06, mv.read(FileIN_06))

    if exists(FileIN_12):
        geo_12 = mv.merge(geo_12, mv.read(FileIN_12))

# Plotting the location of rainfall observations at different reporting times
coastlines = mv.mcoast(
    map_coastline_thickness = 2,
    map_coastline_resolution = "medium",
    map_boundaries = "on",
    map_boundaries_colour = "charcoal",
    map_boundaries_thickness = 1,
    map_grid_colour = "grey",
    map_label_right = "off",
    map_label_top = "off",
    map_label_height = 2,
    map_grid_latitude_increment = 30,
    map_grid_longitude_increment = 60
    )

legend = mv.mlegend(
    legend_title = "on",
    legend_title_text = "Reporting times at end of the accumulation period",
    legend_title_orientation = "horizontal",
    legend_title_font_size = 2,
    legend_title_font_colour = "black",
    legend_title_position = "top",
    legend_display_type = "disjoint",
    legend_text_colour = "black",
    legend_text_font_size = 2,
    legend_text_composition = "user_text_only",
    legend_user_lines = ["00 UTC","01 UTC","03 UTC","04 UTC","05 UTC","06 UTC","12 UTC"],
    legend_symbol_height_factor=5,
    )

title = mv.mtext(
    text_line_count = 1,
    text_line_1 = "Example of the location of " + str(Acc) + "-hourly rainfall observations for " + Date_2_Plot.strftime("%Y-%m-%d"),
    text_colour = "charcoal",
    text_font_style = "bold",
    text_font_size  = 3
    )

markers_00 = mv.psymb(
    symbol_type = "MARKER",
    symbol_table_mode = "ON",
    legend = "ON",
    symbol_quality = "HIGH",
    symbol_min_table = [ 0],
    symbol_max_table = [ 10000],
    symbol_marker_table = [ 15],
    symbol_colour_table = ["grey"],
    symbol_height_table = [ 0.15]
    )

markers_01 = mv.psymb(
    symbol_type = "MARKER",
    symbol_table_mode = "ON",
    legend = "ON",
    symbol_quality = "HIGH",
    symbol_min_table = [ 0],
    symbol_max_table = [ 10000],
    symbol_marker_table = [ 15],
    symbol_colour_table = ["blue"],
    symbol_height_table = [ 0.15]
    )

markers_03 = mv.psymb(
    symbol_type = "MARKER",
    symbol_table_mode = "ON",
    legend = "ON",
    symbol_quality = "HIGH",
    symbol_min_table = [ 0],
    symbol_max_table = [ 10000],
    symbol_marker_table = [ 15],
    symbol_colour_table = ["red"],
    symbol_height_table = [ 0.15]
    )

markers_04 = mv.psymb(
    symbol_type = "MARKER",
    symbol_table_mode = "ON",
    legend = "ON",
    symbol_quality = "HIGH",
    symbol_min_table = [ 0],
    symbol_max_table = [ 10000],
    symbol_marker_table = [ 15],
    symbol_colour_table = ["green"],
    symbol_height_table = [ 0.15]
    )

markers_05 = mv.psymb(
    symbol_type = "MARKER",
    symbol_table_mode = "ON",
    legend = "ON",
    symbol_quality = "HIGH",
    symbol_min_table = [ 0],
    symbol_max_table = [ 10000],
    symbol_marker_table = [ 15],
    symbol_colour_table = ["orange"],
    symbol_height_table = [ 0.15]
    )

markers_06 = mv.psymb(
    symbol_type = "MARKER",
    symbol_table_mode = "ON",
    legend = "ON",
    symbol_quality = "HIGH",
    symbol_min_table = [ 0],
    symbol_max_table = [ 10000],
    symbol_marker_table = [ 15],
    symbol_colour_table = ["purple"],
    symbol_height_table = [ 0.15]
    )

markers_12 = mv.psymb(
    symbol_type = "MARKER",
    symbol_table_mode = "ON",
    legend = "ON",
    symbol_quality = "HIGH",
    symbol_min_table = [ 0],
    symbol_max_table = [ 10000],
    symbol_marker_table = [ 15],
    symbol_colour_table = ["black"],
    symbol_height_table = [ 0.15]
    )

# Saving the plot
MainDirOUT = Git_Repo + "/" + DirOUT + "/" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF)
if not exists(MainDirOUT):
    os.makedirs(MainDirOUT)
png = mv.png_output(output_width = 5000, output_name = MainDirOUT + "/LocOBS_" + Date_2_Plot.strftime("%Y%m%d"))
mv.setoutput(png)
mv.plot(geo_00, markers_00, geo_01, markers_01, geo_03, markers_03, geo_04, markers_04, geo_05, markers_05, geo_06, markers_06, geo_12, markers_12, coastlines, legend, title)