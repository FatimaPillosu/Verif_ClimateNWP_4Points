import os
import metview as mv

#################################################################################################
# COD
#E DESCRIPTION
# 25_Plot_Blank_Map.py plots a blank global map.
# Code runtime: ~ negligible.

# DESCRIPTION OF INPUT PARAMETERS
# Git_Repo (string): path of local GitHub repository.
# DirOUT (string): relative path for the directory containing the map plots for the observed and modelled rainfall totals.

# INPUT PARAMETERS
Git_Repo = "/ec/vol/ecpoint_dev/mofp/papers_2_write/Verif_ClimateNWP_4Points"
DirOUT = "Data/Plot/25_Blank_Map"
#################################################################################################

print("Creating a blank global map...")

lsm = mv.retrieve(
    class_ = "od",
    date = "2024-09-28",
    expver = 1,
    levtype = "sfc",
    param = "172.128",
    step = 0,
    stream = "oper",
    time = "00:00:00",
    type = "fc")

coastlines = mv.mcoast(
    map_coastline_colour = "charcoal",
    map_coastline_thickness = 5,
    map_coastline_resolution = "low",
    map_coastline_land_shade = "on",
    map_coastline_land_shade_colour = "rgb(0.9372,0.9098,0.8589)",
    map_coastline_sea_shade = "on",
    map_coastline_sea_shade_colour = "rgb(0.8415,0.9389,0.9389)",
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

contouring = mv.mcont(
    legend = "on",
    contour = "off",
    contour_level_selection_type = "level_list",
    contour_level_list = [0, 1],
    contour_label = "off",
    contour_shade = "on",
    contour_shade_colour_method = "list",
    contour_shade_method = "area_fill",
    contour_shade_colour_list = ["white"]
    )

# Saving the plot of the modelled climatology
DirOUT_temp = Git_Repo + "/" + DirOUT
if not os.path.exists(DirOUT_temp):
      os.makedirs(DirOUT_temp)
png = mv.png_output(output_width = 5000, output_name = DirOUT_temp + "/Blank_Map")
mv.setoutput(png)
mv.plot(lsm, coastlines, contouring)