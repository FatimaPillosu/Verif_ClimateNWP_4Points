import os
from datetime import datetime, timedelta
import numpy as np
import metview as mv

#################################################################################################
# CODE DESCRIPTION
# 25_Plot_Case_Study_Scatter_MapPlot.py plots a scatter plot on a map of the difference between rainfall totals (from 
# observations and NWP models).
# Code runtime: ~ negligible.

# DESCRIPTION OF INPUT PARAMETERS
# BaseDate (date, in YYYYMMDD format): date to consider.
# Acc (integer, in hours): rainfall accumulation period.
# SystemNWP (list of string): considered NWP models. Valid values are:
#                                                   - "Reanalysis/ERA5_EDA"
#                                                   - "Reanalysis/ERA5"
#                                                   - "Reforecasts/ECMWF_46r1"
#                                                   - "Reanalysis/ERA5_ecPoint"
# Git_Repo (string): path of local GitHub repository.
# DirIN_OBS (string): relative path for the directory containing the observed rainfall totals.
# DirIN (string): relative path for the directory containing the NWP modelled rainfall totals.
# DirOUT (string): relative path for the directory containing the map plots for the observed and modelled rainfall totals.

# INPUT PARAMETERS
BaseDate = datetime(2018, 10, 28)
Acc = 24
#Domain = [47, 5, 44.2, 15]
Domain = [47, 5.3, 35.1, 20.6]
SystemNWP = "Reanalysis/ERA5_ecPoint"
Git_Repo = "/ec/vol/ecpoint_dev/mofp/papers_2_write/Verif_ClimateNWP_4Points"
DirIN_OBS = "Data/Raw/OBS"
DirIN_NWP = "Data/Raw/NWP"
DirOUT = "Data/Plot/25_Case_Study_Scatter_MapPlot"
#################################################################################################


# CUSTOM FUNCTIONS

########################################################
# Rainfall realizations (for multiple accumulations) from Reforecasts #
########################################################

def tp_Reforecast(Acc, BaseDateTime, DirIN):

      tp = None
      DirIN = DirIN + "/" + BaseDateTime.strftime("%Y") + "/" + BaseDateTime.strftime("%Y%m%d%H")
      if os.path.exists(DirIN):
            for StepS in range(0, 240+1-Acc, Acc):
                  StepF = StepS + Acc
                  FileIN1 =  "tp_" + BaseDateTime.strftime("%Y%m%d") + "_" + BaseDateTime.strftime("%H") + "_" + f'{StepS:03d}' + ".grib"
                  FileIN2 =  "tp_" + BaseDateTime.strftime("%Y%m%d") + "_" + BaseDateTime.strftime("%H") + "_" + f'{StepF:03d}' + ".grib"
                  tp1 = mv.read(DirIN + "/" + FileIN1)
                  tp2 = mv.read(DirIN + "/" + FileIN2)
                  tp = mv.merge(tp, (tp2-tp1)*1000 )
      else:
            tp = np.array([])
      return tp


#############################################
# 24-hourly rainfall realizations from short-range ERA5 #
#############################################

def tp_ShortRange_ERA5_24h(BaseDateTime, DirIN):

      # Computing the accumulated rainfall totals
      BaseDateTime_0 = BaseDateTime + timedelta(hours=6)
      BaseDateTime_1 = BaseDateTime - timedelta(days=1) + timedelta(hours=18)
      count_steps = 0 # to make sure that both required dates are available in the datebase
      tp = 0
      
      for Step in range(7,(12+1)):
            DirIN_1 = DirIN + "/" + BaseDateTime_1.strftime("%Y") + "/" + BaseDateTime_1.strftime("%Y%m%d%H")
            FileIN_1 =  "tp_" + BaseDateTime_1.strftime("%Y%m%d") + "_" + BaseDateTime_1.strftime("%H") + "_" + f'{Step:03d}' + ".grib"
            if os.path.exists(DirIN_1 + "/" + FileIN_1):
                  count_steps = count_steps + 1
                  tp = tp + mv.read(DirIN_1 + "/" + FileIN_1)

      for Step in range(1,(18+1)):  
            DirIN_0 = DirIN + "/" + BaseDateTime_0.strftime("%Y") + "/" + BaseDateTime_0.strftime("%Y%m%d%H")
            FileIN_0 =  "tp_" + BaseDateTime_0.strftime("%Y%m%d") + "_" + BaseDateTime_0.strftime("%H") + "_" + f'{Step:03d}' + ".grib"
            if os.path.exists(DirIN_0 + "/" + FileIN_0):
                  count_steps = count_steps + 1
                  tp = tp + mv.read(DirIN_0 + "/" + FileIN_0)

      # Converting the accumulated rainfall totals from m to mm, and converting the fieldset into a 16-byte float numpy array (to reduce memory consumption)
      if count_steps == 24:
            tp = tp * 1000
      else:
            tp = np.array([])
      
      return tp

##################################################
# 24-hourly rainfall realizations from short-range ERA5-EDA #
##################################################

def tp_ShortRange_ERA5_EDA_24h(BaseDateTime, DirIN):

      # Computing the accumulated rainfall totals
      BaseDateTime_0 = BaseDateTime + timedelta(hours=6)
      BaseDateTime_1 = BaseDateTime - timedelta(days=1) + timedelta(hours=18)
      count_steps = 0 # to make sure that both required dates are available in the datebase
      tp = 0
      
      for Step in range(9, (12+1), 3):
            DirIN_1 = DirIN + "/" + BaseDateTime_1.strftime("%Y") + "/" + BaseDateTime_1.strftime("%Y%m%d%H")
            FileIN_1 =  "tp_" + BaseDateTime_1.strftime("%Y%m%d") + "_" + BaseDateTime_1.strftime("%H") + "_" + f'{Step:03d}' + ".grib"
            if os.path.exists(DirIN_1 + "/" + FileIN_1):
                  count_steps = count_steps + 1
                  tp = tp + mv.read(DirIN_1 + "/" + FileIN_1)

      for Step in range(3, (18+1), 3):  
            DirIN_0 = DirIN + "/" + BaseDateTime_0.strftime("%Y") + "/" + BaseDateTime_0.strftime("%Y%m%d%H")
            FileIN_0 =  "tp_" + BaseDateTime_0.strftime("%Y%m%d") + "_" + BaseDateTime_0.strftime("%H") + "_" + f'{Step:03d}' + ".grib"
            if os.path.exists(DirIN_0 + "/" + FileIN_0):
                  count_steps = count_steps + 1
                  tp = tp + mv.read(DirIN_0 + "/" + FileIN_0)

      # Converting the accumulated rainfall totals from m to mm, and converting the fieldset into a 16-byte float numpy array (to reduce memory consumption)
      if count_steps == 8:
            tp = tp * 1000
      else:
            tp = np.array([])
      
      return tp

###########################################
# 24-hourly rainfall realizations from ERA5_ecPoint #
###########################################

# Note: the rainfall values are already in mm and are valid for the period 00-00 UTC
def tp_ERA5_ecPoint_24h(BaseDateTime, DirIN):

      # Reading the accumulated rainfall values, and converting the fieldset into a 16-byte float numpy array (to reduce memory consumption)
      DirIN = DirIN + "/" + BaseDateTime.strftime("%Y%m")
      FileIN =  "Pt_BC_PERC_" + BaseDateTime.strftime("%Y%m%d") + ".grib2"

      if os.path.exists(DirIN + "/" + FileIN):
            tp = mv.read(DirIN + "/" + FileIN)
      else:
            tp = np.array([])
      
      return tp

###############################################################################################################


# Reading the rainfall observations for the considered date
BaseDate_obs = BaseDate + timedelta(days=1)
dataset_obs_list = ["synop", "hdobs", "bom", "efas", "india", "vnm"]
tp_obs = None
for dataset_obs in dataset_obs_list:
    FileIN = Git_Repo + "/" + DirIN_OBS + "/STVL_" + f'{Acc:02d}' + "h/" + dataset_obs + "/" + BaseDate_obs.strftime("%Y%m%d") + "/tp" + f'{Acc:02d}' + "_obs_" + BaseDate_obs.strftime("%Y%m%d") + "00.geo"
    if os.path.exists(FileIN):
            tp_obs = mv.merge(tp_obs, mv.read(FileIN))
            tp_obs_mask = mv.mask(tp_obs, Domain)
            tp_obs_domain = mv.filter(tp_obs_mask * tp_obs, tp_obs_mask > 0) 

# Extracting the rainfall realizations from the NWP models
DirIN_temp = Git_Repo + "/" + DirIN_NWP + "/" + SystemNWP
if SystemNWP == "Reanalysis/ERA5_ecPoint":
      DirIN_temp = DirIN_temp + "_" + str(Acc) + "h"

if SystemNWP == "Reforecasts/ECMWF_46r1":  
      tp_nwp_grib = []
      day = 0
      while len(tp_nwp_grib) == 0:
            BaseDate_reforecasts = BaseDate - timedelta(days = day)
            tp_nwp_grib = tp_Reforecast(Acc, BaseDate_reforecasts, DirIN_temp)
            day = day + 1
      tp_fc = tp_nwp_grib[day-1]
elif SystemNWP == "Reanalysis/ERA5_EDA" and Acc == 24:
      tp_nwp_grib = tp_ShortRange_ERA5_EDA_24h(BaseDate, DirIN_temp) 
      tp_fc = tp_nwp_grib[0]
elif SystemNWP == "Reanalysis/ERA5" and Acc == 24:
      tp_nwp_grib = tp_ShortRange_ERA5_24h(BaseDate, DirIN_temp)
      tp_fc = tp_nwp_grib
elif SystemNWP == "Reanalysis/ERA5_ecPoint" and Acc == 24:
      tp_nwp_grib = tp_ERA5_ecPoint_24h(BaseDate, DirIN_temp)
      tp_fc = tp_nwp_grib[98]
else:
      print("ERROR! Considered dataset not valid.")

tp_fc_domain = mv.nearest_gridpoint(tp_fc, tp_obs_domain)

# Computing the differences betweeen fc and obs
diff = tp_obs_domain - tp_fc_domain

print(np.sum(mv.values(diff>0)))
print(mv.count(tp_fc_domain))
print(np.sum(mv.values(diff>0)) / mv.count(tp_fc_domain) * 100)


# Plotting observations
print("Plotting the rainfall realizations from observations...")

coastlines = mv.mcoast(
      map_coastline_colour = "charcoal",
      map_coastline_thickness = 5,
      map_coastline_resolution = "full",
      map_coastline_sea_shade = "on", # comments this line to see the rainfall totals over the sea
      map_coastline_sea_shade_colour = "white", # # comments this line to see the rainfall totals over the sea
      map_boundaries = "on",
      map_boundaries_colour = "charcoal",
      map_boundaries_thickness = 5,
      map_administrative_boundaries = "on",
      map_administrative_boundaries_countries_list = "ita",
      map_administrative_boundaries_style = "solid",
      map_administrative_boundaries_colour = "charcoal",
      map_administrative_boundaries_thickness = 5,
      map_grid = "off"
      )

geo_view = mv.geoview(
    map_projection       = "epsg:3857",
    map_area_definition  = "corners",
    area                 = [35.1,5.3,47.33,20.58],
    )

markers = mv.psymb(
      symbol_type = "MARKER",
      symbol_table_mode = "ON",
      legend = "off",
      symbol_quality = "HIGH",
      symbol_min_table = [-0.1,0.1],
      symbol_max_table = [0.1,1.1],
      symbol_marker_table = [15, 20],
      symbol_colour_table = ["grey","red"],
    symbol_height_table = [ 0.1, 0.2]
      )
      
title = mv.mtext(
      text_line_count = 3,
      text_line_1 = str(Acc) + "-hourly rainfall observations",
      text_line_2 = "VT: " + BaseDate.strftime("%Y%m%d") + " at 00 UTC to " + BaseDate_obs.strftime("%Y%m%d") + " at 00 UTC",
      text_line_3 = " ",
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

# Saving the map plot for the observed rainfall totals
DirOUT_temp = Git_Repo + "/" + DirOUT + "/OBS"
if not os.path.exists(DirOUT_temp):
      os.makedirs(DirOUT_temp)
png = mv.png_output(output_width = 5000, output_name = DirOUT_temp + "/tp")
mv.setoutput(png)
mv.plot(geo_view, markers, coastlines, legend, title, diff>0)