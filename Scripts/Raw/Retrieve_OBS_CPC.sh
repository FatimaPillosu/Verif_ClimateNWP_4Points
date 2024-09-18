#!/bin/bash

######################################################################
# CODE DESCRIPTION
# Retrieve_OBS_CPC.sh retrieves 24-hourly rainfall observations from the "CPC Global  
# Unified Gauge-Based Analysis of Daily Precipitation" dataset from NOAA. The data is 
# downloaded and saved manually and stored in the relevant directory.
# Code runtime: up to 1 hour.

# DESCRIPTION OF INPUT PARAMETERS
# YearS (integer): start year to retrieve.
# YearF (integer): final year to retrieve.
# Git_Repo (string): path of local GitHub repository.
# DirOUT (string): relative path for the output directory.

# INPUT PARAMETERS
YearS=2000
YearF=2019
Git_Repo="/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_ClimateNWP_4Points"
DirOUT="Data/Raw/OBS/CPC_24h"
######################################################################

# GENERAL

# The official website of the "CPC Global Unified Gauge-Based Analysis of Daily Precipitation" dataset can be found here:
# https://psl.noaa.gov/data/gridded/data.cpc.globalprecip.html

# A general guide for the "NetCDF Climate and Forecast (CF) Metadata Conventions"can be found here:
# https://cfconventions.org/Data/cf-conventions/cf-conventions-1.10/cf-conventions.html#_data_types

##############################################################
# The raw data was downloaded manually here:
# https://downloads.psl.noaa.gov/Datasets/cpc_global_precip/

# The data is stored in the following directory:
MainDirOUT = Git_Repo + "/" + DirOUT + "_" + str(Acc) + "h"