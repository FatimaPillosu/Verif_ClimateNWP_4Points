import os
from os.path import exists
import numpy as np
import matplotlib.pyplot as plt
import metview as mv

######################################################################################################################################
# CODE DESCRIPTION
# 11_Plot_QC_AlignOBS_RawSTVL_CleanSTVL.py plots the results of the quality checks carried out on the raw STVL point rainfall observations within the 20-year 
# period of interest, and compares them with the results for the cleaned STVL rainfall observations.
# Code runtime: ~ 20 minutes.

# DESCRIPTION OF INPUT PARAMETERS
# YearS (integer, in YYYY format): start year to consider.
# YearF (integer, in YYYY format): final year to consider.
# Acc (integer, in hours): rainfall accumulation period.
# DatasetSTVL_list (string): list of STVL's datasets considered to build the aligned observations.
# ReportingTimeSTVL_list (string): list of observations' reporting times considered for each dataset to build the aligned observations.
# NameOBS_list (list of strings): list of the observational datasets to quality check.
# Coeff_Grid2Point_list (list of integer numbers): list of coefficients that make the CPC's gridded rainfall values comparable with the STVL's point observations. 
# Git_Repo (string): path of local GitHub repository.
# DirIN (string): relative path for the input directory.
# DirOUT (string): relative path for the output directory.

# INPUT PARAMETERS
YearS = 2000
YearF = 2019
Acc = 24
DatasetSTVL_list = "The aligned observations have been built considering the following STVL datasets: 'synop', 'bom', 'india', 'vnm', and, 'efas'."
ReportingTimeSTVL_list = "The aligned observations have been built considering, for each dataset, reporting times from 00 to 23 UTC at hourly steps when available."
NameOBS_list = ["08_AlignOBS_Combine_Years_RawSTVL", "10_AlignOBS_CleanSTVL"]
Coeff_Grid2Point_list = [2, 5, 10, 20, 50, 100, 200, 500, 1000]
Git_Repo = "/ec/vol/ecpoint_dev/mofp/papers_2_write/Verif_ClimateNWP_4Points"
DirIN = "Data/Compute"
DirOUT= "Data/Plot/11_QC_AlignOBS_RawSTVL_CleanSTVL"
######################################################################################################################################

# Costum function for quality checks

def quality_check(DirIN, DirOUT):
      
      # Reading the rainfall observations over the period of interest and the correspondent metadata (i.e., ids/lats/lons/dates)
      print(" ")
      print("Reading the rainfall observations over the period of interest and the correspondent metadata (i.e., ids/lats/lons/dates)")
      stnids_unique = np.load(DirIN + "/stn_ids.npy")
      lats_unique = np.load(DirIN + "/stn_lats.npy")
      lons_unique = np.load(DirIN + "/stn_lons.npy")
      dates = np.load(DirIN + "/dates.npy")
      align_obs = np.load(DirIN + "/obs.npy")
      NumStns = align_obs.shape[0]
      NumDays = align_obs.shape[1]
      print(" - Considering " + str(NumStns) + " rainfall stations each day over the period of interest.")
      print(" - Considering " + str(NumDays) + " days over the period of interest.")

      # Flattening all the observations over the considered period
      obs_all = align_obs.flatten()
      num_obs_all =  len(obs_all)
      print(" - Therefore, there are a total number of " + str(num_obs_all) + " observation instances over the period of interest." )

      # Defining the minimum and maximum values for the whole period
      print(" ")
      print("Printing some statistics:")
      min_tp = np.nanmin(obs_all)
      max_tp = np.nanmax(obs_all)
      print(" - Minimum rainfall value found: " + str(min_tp) + " mm")
      print(" - Maximum rainfall value found: " + str(max_tp) + " mm")

      # Defining the percentage of negative and zero values
      print(" ")
      print("Computing the distribution of observation instances <= 0 mm")
      temp_neg = np.where( align_obs < 0 ) 
      freq_abs_neg = temp_neg[0].size
      freq_rel_neg = freq_abs_neg / num_obs_all
      print( " - N. of instances for tp < 0 mm : " + str(freq_abs_neg) + " (" + str(np.round_(freq_rel_neg, decimals=6)) + "%)" )

      temp_0 = np.where( align_obs == 0 ) 
      freq_abs_0 = temp_0[0].size
      freq_rel_0 = freq_abs_0 / num_obs_all
      print( " - N. of instances for tp = 0 mm : " + str(freq_abs_0) + " (" + str(np.round_(freq_rel_0,decimals=2)) + "%)" )


      ##############################################
      # Plotting distributions of different sets of rainfall values

      a = 0.1
      b = 0.9
      c = 0.1
      print(" ")
      print("Computing and plotting the distribution of observation instances between " + str(a) + " and " + str(b) + " mm ...")
      bins = np.arange(a-c, b+c, c) + 0.01
      hist, edges = np.histogram(obs_all,bins)
      freq = hist / num_obs_all * 100
      plt.rcParams["figure.figsize"] = (10,5)
      plt.bar(edges[1:], freq, width=np.diff(edges)/2, align="center", color=(0, 0, 1))
      plt.title("Distribution of rainfall values between " + str(a) + " and " + str(b) + " mm", fontsize="14")
      plt.xlabel("Rainfall [mm/" + f'{Acc:02d}' + "h]", fontsize="12")
      plt.ylabel("Relative Frequency [%]", fontsize="12")
      plt.xticks(np.arange(a,b+c,0.1))
      plt.xlim((a-c,b+c))
      plt.ylim((0, np.amax(freq) + 0.01))
      plt.savefig(DirOUT + "/Distr_tp" + f'{Acc:02d}' + "h_" +str(a) + "mm_" + str(b) + "mm.png")
      plt.close()
      [print( " - N. of instances for tp = " + str(np.round_(bins[i+1],decimals=1)) + " mm : " + str(hist[i]) ) for i in range(len(hist))]

      a = 1.0
      b = 9.9
      c = 0.1
      print(" ")
      print("Computing and plotting the distribution of observation instances between " + str(a) + " and " + str(b) + " mm ...")
      bins = np.arange(a-c, b+c, c) + 0.01
      hist, edges = np.histogram(obs_all,bins)
      freq = hist / num_obs_all * 100
      plt.rcParams["figure.figsize"] = (10,5)
      plt.bar(edges[1:], freq, width=np.diff(edges)/2, align="center", color=(0, 0, 1))
      plt.title("Distribution of rainfall values between " + str(a) + " and " + str(b) + " mm", fontsize="14")
      plt.xlabel("Rainfall [mm/" + f'{Acc:02d}' + "h]", fontsize="12")
      plt.ylabel("Relative Frequency [%]", fontsize="12")
      plt.xticks(np.arange(a,b+c,1))
      plt.xlim((a-c,b+c))
      plt.ylim((0, np.amax(freq)+0.01))
      plt.savefig(DirOUT + "/Distr_tp" + f'{Acc:02d}' + "h_" + str(a) + "mm_" + str(b) + "mm.png")
      plt.close()
      [print( " - N. of instances for tp = " + str(np.round_(bins[i+1],decimals=1)) + " mm : " + str(hist[i]) ) for i in range(len(hist))]

      a = 10.0
      b = 19.9
      c = 0.1
      print(" ")
      print("Computing and plotting the distribution of observation instances between " + str(a) + " and " + str(b) + " mm ...")
      bins = np.arange(a-c, b+c, c) + 0.01
      hist, edges = np.histogram(obs_all,bins)
      freq = hist / num_obs_all * 100
      plt.rcParams["figure.figsize"] = (10,5)
      plt.bar(edges[1:], freq, width=np.diff(edges)/2, align="center", color=(0, 0, 1))
      plt.title("Distribution of rainfall values between " + str(a) + " and " + str(b) + " mm", fontsize="14")
      plt.xlabel("Rainfall [mm/" + f'{Acc:02d}' + "h]", fontsize="12")
      plt.ylabel("Relative Frequency [%]", fontsize="12")
      plt.xticks(np.arange(a,b+c,1))
      plt.xlim((a-c,b+c))
      plt.ylim((0, np.amax(freq)+0.01))
      plt.savefig(DirOUT + "/Distr_tp" + f'{Acc:02d}' + "h_" + str(a) + "mm_" + str(b) + "mm.png")
      plt.close()
      [print( " - N. of instances for tp = " + str(np.round_(bins[i+1],decimals=1)) + " mm : " + str(hist[i]) ) for i in range(len(hist))]

      a = 20.0
      b = 29.9
      c = 0.1
      print(" ")
      print("Computing and plotting the distribution of observation instances between " + str(a) + " and " + str(b) + " mm ...")
      bins = np.arange(a-c, b+c, c) + 0.01
      hist, edges = np.histogram(obs_all,bins)
      freq = hist / num_obs_all * 100
      plt.rcParams["figure.figsize"] = (10,5)
      plt.bar(edges[1:], freq, width=np.diff(edges)/2, align="center", color=(0, 0, 1))
      plt.title("Distribution of rainfall values between " + str(a) + " and " + str(b) + " mm", fontsize="14")
      plt.xlabel("Rainfall [mm/" + f'{Acc:02d}' + "h]", fontsize="12")
      plt.ylabel("Relative Frequency [%]", fontsize="12")
      plt.xticks(np.arange(a,b+c,1))
      plt.xlim((a-c,b+c))
      plt.ylim((0, np.amax(freq)+0.01))
      plt.savefig(DirOUT + "/Distr_tp" + f'{Acc:02d}' + "h_" + str(a) + "mm_" + str(b) + "mm.png")
      plt.close()
      [print( " - N. of instances for tp = " + str(np.round_(bins[i+1],decimals=1)) + " mm : " + str(hist[i]) ) for i in range(len(hist))]

      a = 30.0
      b = 39.9
      c = 0.1
      print(" ")
      print("Computing and plotting the distribution of observation instances between " + str(a) + " and " + str(b) + " mm ...")
      bins = np.arange(a-c, b+c, c) + 0.01
      bins = bins[:(len(bins)-1)] # for some reason, from the value 300, Python is adding one more value at the end of the numpy array (i.e. 400), which should not be there. Since we don't know the reason for this change compared to previous arrays, we just eliminate the last element of the array.
      hist, edges = np.histogram(obs_all,bins)
      freq = hist / num_obs_all * 100
      plt.rcParams["figure.figsize"] = (10,5)
      plt.bar(edges[1:], freq, width=np.diff(edges)/2, align="center", color=(0, 0, 1))
      plt.title("Distribution of rainfall values between " + str(a) + " and " + str(b) + " mm", fontsize="14")
      plt.xlabel("Rainfall [mm/" + f'{Acc:02d}' + "h]", fontsize="12")
      plt.ylabel("Relative Frequency [%]", fontsize="12")
      plt.xticks(np.arange(a,b+c,1))
      plt.xlim((a-c,b+c))
      plt.ylim((0, np.amax(freq)+0.001))
      plt.savefig(DirOUT + "/Distr_tp" + f'{Acc:02d}' + "h_" + str(a) + "mm_" + str(b) + "mm.png")
      plt.close()
      [print( " - N. of instances for tp = " + str(np.round_(bins[i+1],decimals=1)) + " mm : " + str(hist[i]) ) for i in range(len(hist))]

      a = 40.0
      b = 49.9
      c = 0.1
      print(" ")
      print("Computing and plotting the distribution of observation instances between " + str(a) + " and " + str(b) + " mm ...")
      bins = np.arange(a-c, b+c, c) + 0.01
      bins = bins[:(len(bins)-1)] # for some reason, from the value 300, Python is adding one more value at the end of the numpy array (i.e. 400), which should not be there. Since we don't know the reason for this change compared to previous arrays, we just eliminate the last element of the array.
      hist, edges = np.histogram(obs_all,bins)
      freq = hist / num_obs_all * 100
      plt.rcParams["figure.figsize"] = (10,5)
      plt.bar(edges[1:], freq, width=np.diff(edges)/2, align="center", color=(0, 0, 1))
      plt.title("Distribution of rainfall values between " + str(a) + " and " + str(b) + " mm", fontsize="14")
      plt.xlabel("Rainfall [mm/" + f'{Acc:02d}' + "h]", fontsize="12")
      plt.ylabel("Relative Frequency [%]", fontsize="12")
      plt.xticks(np.arange(a,b+c,1))
      plt.xlim((a-c,b+c))
      plt.ylim((0, np.amax(freq)+0.001))
      plt.savefig(DirOUT + "/Distr_tp" + f'{Acc:02d}' + "h_" + str(a) + "mm_" + str(b) + "mm.png")
      plt.close()
      [print( " - N. of instances for tp = " + str(np.round_(bins[i+1],decimals=1)) + " mm : " + str(hist[i]) ) for i in range(len(hist))]

      a = 50.0
      b = 59.9
      c = 0.1
      print(" ")
      print("Computing and plotting the distribution of observation instances between " + str(a) + " and " + str(b) + " mm ...")
      bins = np.arange(a-c, b+c, c) + 0.01
      bins = bins[:(len(bins)-1)] # for some reason, from the value 300, Python is adding one more value at the end of the numpy array (i.e. 400), which should not be there. Since we don't know the reason for this change compared to previous arrays, we just eliminate the last element of the array.
      hist, edges = np.histogram(obs_all,bins)
      freq = hist / num_obs_all * 100
      plt.rcParams["figure.figsize"] = (10,5)
      plt.bar(edges[1:], freq, width=np.diff(edges)/2, align="center", color=(0, 0, 1))
      plt.title("Distribution of rainfall values between " + str(a) + " and " + str(b) + " mm", fontsize="14")
      plt.xlabel("Rainfall [mm/" + f'{Acc:02d}' + "h]", fontsize="12")
      plt.ylabel("Relative Frequency [%]", fontsize="12")
      plt.xticks(np.arange(a,b+c,1))
      plt.xlim((a-c,b+c))
      plt.ylim((0, np.amax(freq)+0.001))
      plt.savefig(DirOUT + "/Distr_tp" + f'{Acc:02d}' + "h_" + str(a) + "mm_" + str(b) + "mm.png")
      plt.close()
      [print( " - N. of instances for tp = " + str(np.round_(bins[i+1],decimals=1)) + " mm : " + str(hist[i]) ) for i in range(len(hist))]

      a = 60.0
      b = 69.9
      c = 0.1
      print(" ")
      print("Computing and plotting the distribution of observation instances between " + str(a) + " and " + str(b) + " mm ...")
      bins = np.arange(a-c, b+c, c) + 0.01
      bins = bins[:(len(bins)-1)] # for some reason, from the value 300, Python is adding one more value at the end of the numpy array (i.e. 400), which should not be there. Since we don't know the reason for this change compared to previous arrays, we just eliminate the last element of the array.
      hist, edges = np.histogram(obs_all,bins)
      freq = hist / num_obs_all * 100
      plt.rcParams["figure.figsize"] = (10,5)
      plt.bar(edges[1:], freq, width=np.diff(edges)/2, align="center", color=(0, 0, 1))
      plt.title("Distribution of rainfall values between " + str(a) + " and " + str(b) + " mm", fontsize="14")
      plt.xlabel("Rainfall [mm/" + f'{Acc:02d}' + "h]", fontsize="12")
      plt.ylabel("Relative Frequency [%]", fontsize="12")
      plt.xticks(np.arange(a,b+c,1))
      plt.xlim((a-c,b+c))
      plt.ylim((0, np.amax(freq)+0.001))
      plt.savefig(DirOUT + "/Distr_tp" + f'{Acc:02d}' + "h_" + str(a) + "mm_" + str(b) + "mm.png")
      plt.close()
      [print( " - N. of instances for tp = " + str(np.round_(bins[i+1],decimals=1)) + " mm : " + str(hist[i]) ) for i in range(len(hist))]

      a = 70.0
      b = 79.9
      c = 0.1
      print(" ")
      print("Computing and plotting the distribution of observation instances between " + str(a) + " and " + str(b) + " mm ...")
      bins = np.arange(a-c, b+c, c) + 0.01
      hist, edges = np.histogram(obs_all,bins)
      freq = hist / num_obs_all * 100
      plt.rcParams["figure.figsize"] = (10,5)
      plt.bar(edges[1:], freq, width=np.diff(edges)/2, align="center", color=(0, 0, 1))
      plt.title("Distribution of rainfall values between " + str(a) + " and " + str(b) + " mm", fontsize="14")
      plt.xlabel("Rainfall [mm/" + f'{Acc:02d}' + "h]", fontsize="12")
      plt.ylabel("Relative Frequency [%]", fontsize="12")
      plt.xticks(np.arange(a,b+c,1))
      plt.xlim((a-c,b+c))
      plt.ylim((0, np.amax(freq)+0.0001))
      plt.savefig(DirOUT + "/Distr_tp" + f'{Acc:02d}' + "h_" + str(a) + "mm_" + str(b) + "mm.png")
      plt.close()
      [print( " - N. of instances for tp = " + str(np.round_(bins[i+1],decimals=1)) + " mm : " + str(hist[i]) ) for i in range(len(hist))]

      a = 80.0
      b = 89.9
      c = 0.1
      print(" ")
      print("Computing and plotting the distribution of observation instances between " + str(a) + " and " + str(b) + " mm ...")
      bins = np.arange(a-c, b+c, c) + 0.01
      hist, edges = np.histogram(obs_all,bins)
      freq = hist / num_obs_all * 100
      plt.rcParams["figure.figsize"] = (10,5)
      plt.bar(edges[1:], freq, width=np.diff(edges)/2, align="center", color=(0, 0, 1))
      plt.title("Distribution of rainfall values between " + str(a) + " and " + str(b) + " mm", fontsize="14")
      plt.xlabel("Rainfall [mm/" + f'{Acc:02d}' + "h]", fontsize="12")
      plt.ylabel("Relative Frequency [%]", fontsize="12")
      plt.xticks(np.arange(a,b+c,1))
      plt.xlim((a-c,b+c))
      plt.ylim((0, np.amax(freq)+0.0001))
      plt.savefig(DirOUT + "/Distr_tp" + f'{Acc:02d}' + "h_" + str(a) + "mm_" + str(b) + "mm.png")
      plt.close()
      [print( " - N. of instances for tp = " + str(np.round_(bins[i+1],decimals=1)) + " mm : " + str(hist[i]) ) for i in range(len(hist))]

      a = 90.0
      b = 99.9
      c = 0.1
      print(" ")
      print("Computing and plotting the distribution of observation instances between " + str(a) + " and " + str(b) + " mm ...")
      bins = np.arange(a-c, b+c, c) + 0.01
      hist, edges = np.histogram(obs_all,bins)
      freq = hist / num_obs_all * 100
      plt.rcParams["figure.figsize"] = (10,5)
      plt.bar(edges[1:], freq, width=np.diff(edges)/2, align="center", color=(0, 0, 1))
      plt.title("Distribution of rainfall values between " + str(a) + " and " + str(b) + " mm", fontsize="14")
      plt.xlabel("Rainfall [mm/" + f'{Acc:02d}' + "h]", fontsize="12")
      plt.ylabel("Relative Frequency [%]", fontsize="12")
      plt.xticks(np.arange(a,b+c,1))
      plt.xlim((a-c,b+c))
      plt.ylim((0, np.amax(freq)+0.0001))
      plt.savefig(DirOUT + "/Distr_tp" + f'{Acc:02d}' + "h_" + str(a) + "mm_" + str(b) + "mm.png")
      plt.close()
      [print( " - N. of instances for tp = " + str(np.round_(bins[i+1],decimals=1)) + " mm : " + str(hist[i]) ) for i in range(len(hist))]

      a = 100.0
      b = 199.9
      c = 0.1
      print(" ")
      print("Computing and plotting the distribution of observation instances between " + str(a) + " and " + str(b) + " mm ...")
      bins = np.arange(a-c, b+c, c) + 0.01
      print(bins)
      hist, edges = np.histogram(obs_all,bins)
      freq = hist / num_obs_all * 100
      plt.rcParams["figure.figsize"] = (30,10)
      plt.bar(edges[1:], freq, width=np.diff(edges)/2, align="center", color=(0, 0, 1))
      plt.title("Distribution of rainfall values between " + str(a) + " and " + str(b) + " mm", fontsize="40")
      plt.xlabel("Rainfall [mm/" + f'{Acc:02d}' + "h]", fontsize="30")
      plt.ylabel("Relative Frequency [%]", fontsize="30")
      plt.xticks(np.arange(a,b+c,10), fontsize="25")
      plt.yticks(fontsize="25")
      plt.xlim((a-1,b+1))
      plt.ylim((0, np.amax(freq) + 0.00001))
      plt.savefig(DirOUT + "/Distr_tp" + f'{Acc:02d}' + "h_" + str(a) + "mm_" + str(b) + "mm.png")
      plt.close()
      [print( " - N. of instances for tp = " + str(np.round_(bins[i+1],decimals=1)) + " mm : " + str(hist[i]) ) for i in range(len(hist))]

      a = 200.0
      b = 299.9
      c = 0.1
      print(" ")
      print("Computing and plotting the distribution of observation instances between " + str(a) + " and " + str(b) + " mm ...")
      bins = np.arange(a-c, b+c, c) + 0.01
      hist, edges = np.histogram(obs_all,bins)
      freq = hist / num_obs_all * 100
      plt.rcParams["figure.figsize"] = (30,10)
      plt.bar(edges[1:], freq, width=np.diff(edges)/2, align="center", color=(0, 0, 1))
      plt.title("Distribution of rainfall values between " + str(a) + " and " + str(b) + " mm", fontsize="40")
      plt.xlabel("Rainfall [mm/" + f'{Acc:02d}' + "h]", fontsize="30")
      plt.ylabel("Relative Frequency [%]", fontsize="30")
      plt.xticks(np.arange(a,b+c,10), fontsize="25")
      plt.yticks(fontsize="25")
      plt.xlim((a-1,b+1))
      plt.ylim((0, np.amax(freq) + 0.00001))
      plt.savefig(DirOUT + "/Distr_tp" + f'{Acc:02d}' + "h_" + str(a) + "mm_" + str(b) + "mm.png")
      plt.close()
      [print( " - N. of instances for tp = " + str(np.round_(bins[i+1],decimals=1)) + " mm : " + str(hist[i]) ) for i in range(len(hist))]

      a = 250.0
      b = 349.9
      c = 0.1
      print(" ")
      print("Computing and plotting the distribution of observation instances between " + str(a) + " and " + str(b) + " mm ...")
      bins = np.arange(a-c, b+c, c) + 0.01
      bins = bins[:(len(bins)-1)]
      hist, edges = np.histogram(obs_all,bins)
      freq = hist / num_obs_all * 100
      plt.rcParams["figure.figsize"] = (30,10)
      plt.bar(edges[1:], freq, width=np.diff(edges)/2, align="center", color=(0, 0, 1))
      plt.title("Distribution of rainfall values between " + str(a) + " and " + str(b) + " mm", fontsize="40")
      plt.xlabel("Rainfall [mm/" + f'{Acc:02d}' + "h]", fontsize="30")
      plt.ylabel("Relative Frequency [%]", fontsize="30")
      plt.xticks(np.arange(a,b+c,10), fontsize="25")
      plt.yticks(fontsize="25")
      plt.xlim((a-1,b+1))
      plt.ylim((0, np.amax(freq) + 0.00001))
      plt.savefig(DirOUT + "/Distr_tp" + f'{Acc:02d}' + "h_" + str(a) + "mm_" + str(b) + "mm.png")
      plt.close()

      a = 300.0
      b = 399.9
      c = 0.1
      print(" ")
      print("Computing and plotting the distribution of observation instances between " + str(a) + " and " + str(b) + " mm ...")
      bins = np.arange(a-c, b+c, c) + 0.01
      bins = bins[:(len(bins)-1)] # for some reason, from the value 300, Python is adding one more value at the end of the numpy array (i.e. 400), which should not be there. Since we don't know the reason for this change compared to previous arrays, we just eliminate the last element of the array.
      hist, edges = np.histogram(obs_all,bins)
      freq = hist / num_obs_all * 100
      plt.rcParams["figure.figsize"] = (30,10)
      plt.bar(edges[1:], freq, width=np.diff(edges)/2, align="center", color=(0, 0, 1))
      plt.title("Distribution of rainfall values between " + str(a) + " and " + str(b) + " mm", fontsize="40")
      plt.xlabel("Rainfall [mm/" + f'{Acc:02d}' + "h]", fontsize="30")
      plt.ylabel("Relative Frequency [%]", fontsize="30")
      plt.xticks(np.arange(a,b+c,10), fontsize="25")
      plt.yticks(fontsize="25")
      plt.xlim((a-1,b+1))
      plt.ylim((0, np.amax(freq) + 0.00001))
      plt.savefig(DirOUT + "/Distr_tp" + f'{Acc:02d}' + "h_" + str(a) + "mm_" + str(b) + "mm.png")
      plt.close()
      [print( " - N. of instances for tp = " + str(np.round_(bins[i+1],decimals=1)) + " mm : " + str(hist[i]) ) for i in range(len(hist))]

      a = 400.0
      b = 499.9
      c = 0.1
      print(" ")
      print("Computing and plotting the distribution of observation instances between " + str(a) + " and " + str(b) + " mm ...")
      bins = np.arange(a-c, b+c, c) + 0.01
      bins = bins[:(len(bins)-1)]
      hist, edges = np.histogram(obs_all,bins)
      freq = hist / num_obs_all * 100
      plt.rcParams["figure.figsize"] = (30,10)
      plt.bar(edges[1:], freq, width=np.diff(edges)/2, align="center", color=(0, 0, 1))
      plt.title("Distribution of rainfall values between " + str(a) + " and " + str(b) + " mm", fontsize="40")
      plt.xlabel("Rainfall [mm/" + f'{Acc:02d}' + "h]", fontsize="30")
      plt.ylabel("Relative Frequency [%]", fontsize="30")
      plt.xticks(np.arange(a,b+c,10), fontsize="25")
      plt.yticks(fontsize="25")
      plt.xlim((a-1,b+1))
      plt.ylim((0, np.amax(freq) + 0.00001))
      plt.savefig(DirOUT + "/Distr_tp" + f'{Acc:02d}' + "h_" + str(a) + "mm_" + str(b) + "mm.png")
      plt.close()
      [print( " - N. of instances for tp = " + str(np.round_(bins[i+1],decimals=1)) + " mm : " + str(hist[i]) ) for i in range(len(hist))]

      a = 500.0
      b = 599.9
      c = 0.1
      print(" ")
      print("Computing and plotting the distribution of observation instances between " + str(a) + " and " + str(b) + " mm ...")
      bins = np.arange(a-c, b+c, c) + 0.01
      bins = bins[:(len(bins)-1)]
      hist, edges = np.histogram(obs_all,bins)
      freq = hist / num_obs_all * 100
      plt.rcParams["figure.figsize"] = (30,10)
      plt.bar(edges[1:], freq, width=np.diff(edges)/2, align="center", color=(0, 0, 1))
      plt.title("Distribution of rainfall values between " + str(a) + " and " + str(b) + " mm", fontsize="40")
      plt.xlabel("Rainfall [mm/" + f'{Acc:02d}' + "h]", fontsize="30")
      plt.ylabel("Relative Frequency [%]", fontsize="30")
      plt.xticks(np.arange(a,b+c,10), fontsize="25")
      plt.yticks(fontsize="25")
      plt.xlim((a-1,b+1))
      plt.ylim((0, np.amax(freq) + 0.00001))
      plt.savefig(DirOUT + "/Distr_tp" + f'{Acc:02d}' + "h_" + str(a) + "mm_" + str(b) + "mm.png")
      plt.close()
      [print( " - N. of instances for tp = " + str(np.round_(bins[i+1],decimals=1)) + " mm : " + str(hist[i]) ) for i in range(len(hist))]

      a = 600.0
      b = 699.9
      c = 0.1
      print(" ")
      print("Computing and plotting the distribution of observation instances between " + str(a) + " and " + str(b) + " mm ...")
      bins = np.arange(a-c, b+c, c) + 0.01
      bins = bins[:(len(bins)-1)]
      hist, edges = np.histogram(obs_all,bins)
      freq = hist / num_obs_all * 100
      plt.rcParams["figure.figsize"] = (30,10)
      plt.bar(edges[1:], freq, width=np.diff(edges)/2, align="center", color=(0, 0, 1))
      plt.title("Distribution of rainfall values between " + str(a) + " and " + str(b) + " mm", fontsize="40")
      plt.xlabel("Rainfall [mm/" + f'{Acc:02d}' + "h]", fontsize="30")
      plt.ylabel("Relative Frequency [%]", fontsize="30")
      plt.xticks(np.arange(a,b+c,10), fontsize="25")
      plt.yticks(fontsize="25")
      plt.xlim((a-1,b+1))
      plt.ylim((0, np.amax(freq) + 0.00001))
      plt.savefig(DirOUT + "/Distr_tp" + f'{Acc:02d}' + "h_" + str(a) + "mm_" + str(b) + "mm.png")
      plt.close()
      [print( " - N. of instances for tp = " + str(np.round_(bins[i+1],decimals=1)) + " mm : " + str(hist[i]) ) for i in range(len(hist))]

      a = 700.0
      b = 799.9
      c = 0.1
      print(" ")
      print("Computing and plotting the distribution of observation instances between " + str(a) + " and " + str(b) + " mm ...")
      bins = np.arange(a-c, b+c, c) + 0.01
      bins = bins[:(len(bins)-1)]
      hist, edges = np.histogram(obs_all,bins)
      freq = hist / num_obs_all * 100
      plt.rcParams["figure.figsize"] = (30,10)
      plt.bar(edges[1:], freq, width=np.diff(edges)/2, align="center", color=(0, 0, 1))
      plt.title("Distribution of rainfall values between " + str(a) + " and " + str(b) + " mm", fontsize="40")
      plt.xlabel("Rainfall [mm/" + f'{Acc:02d}' + "h]", fontsize="30")
      plt.ylabel("Relative Frequency [%]", fontsize="30")
      plt.xticks(np.arange(a,b+c,10), fontsize="25")
      plt.yticks(fontsize="25")
      plt.xlim((a-1,b+1))
      plt.ylim((0, np.amax(freq) + 0.00001))
      plt.savefig(DirOUT + "/Distr_tp" + f'{Acc:02d}' + "h_" + str(a) + "mm_" + str(b) + "mm.png")
      plt.close()
      [print( " - N. of instances for tp = " + str(np.round_(bins[i+1],decimals=1)) + " mm : " + str(hist[i]) ) for i in range(len(hist))]

      a = 800.0
      b = 899.9
      c = 0.1
      print(" ")
      print("Computing and plotting the distribution of observation instances between " + str(a) + " and " + str(b) + " mm ...")
      bins = np.arange(a-c, b+c, c) + 0.01
      bins = bins[:(len(bins)-1)]
      hist, edges = np.histogram(obs_all,bins)
      freq = hist / num_obs_all * 100
      plt.rcParams["figure.figsize"] = (30,10)
      plt.bar(edges[1:], freq, width=np.diff(edges)/2, align="center", color=(0, 0, 1))
      plt.title("Distribution of rainfall values between " + str(a) + " and " + str(b) + " mm", fontsize="40")
      plt.xlabel("Rainfall [mm/" + f'{Acc:02d}' + "h]", fontsize="30")
      plt.ylabel("Relative Frequency [%]", fontsize="30")
      plt.xticks(np.arange(a,b+c,10), fontsize="25")
      plt.yticks(fontsize="25")
      plt.xlim((a-1,b+1))
      plt.ylim((0, np.amax(freq) + 0.00001))
      plt.savefig(DirOUT + "/Distr_tp" + f'{Acc:02d}' + "h_" + str(a) + "mm_" + str(b) + "mm.png")
      plt.close()
      [print( " - N. of instances for tp = " + str(np.round_(bins[i+1],decimals=1)) + " mm : " + str(hist[i]) ) for i in range(len(hist))]

      a = 900.0
      b = 999.9
      c = 0.1
      print(" ")
      print("Computing and plotting the distribution of observation instances between " + str(a) + " and " + str(b) + " mm ...")
      bins = np.arange(a-c, b+c, c) + 0.01
      bins = bins[:(len(bins)-1)]
      hist, edges = np.histogram(obs_all,bins)
      freq = hist / num_obs_all * 100
      plt.rcParams["figure.figsize"] = (30,10)
      plt.bar(edges[1:], freq, width=np.diff(edges)/2, align="center", color=(0, 0, 1))
      plt.title("Distribution of rainfall values between " + str(a) + " and " + str(b) + " mm", fontsize="40")
      plt.xlabel("Rainfall [mm/" + f'{Acc:02d}' + "h]", fontsize="30")
      plt.ylabel("Relative Frequency [%]", fontsize="30")
      plt.xticks(np.arange(a,b+c,10), fontsize="25")
      plt.yticks(fontsize="25")
      plt.xlim((a-1,b+1))
      plt.ylim((0, np.amax(freq) + 0.00001))
      plt.savefig(DirOUT + "/Distr_tp" + f'{Acc:02d}' + "h_" + str(a) + "mm_" + str(b) + "mm.png")
      plt.close()
      [print( " - N. of instances for tp = " + str(np.round_(bins[i+1],decimals=1)) + " mm : " + str(hist[i]) ) for i in range(len(hist))]

      print(" ")
      print("Computing and plotting the distribution of observation instances between 1000 and 4000 mm ...")
      bins = np.array([1000,1100, 1200,1300,1400,1500,1600, 1700, 1800, 1826, 4000])
      xticks = np.arange(len(bins)-1)
      xticks_labels = ["[1000-1100)","[1100-1200)","[1200-1300)","[1300-1400)","[1400-1500)","[1500-1600)","[1600-1700)","[1700-1800)", "[1800-1826)", "[1826-4000)"]
      hist, edges = np.histogram(obs_all,bins-0.01)
      freq = hist / num_obs_all * 100
      plt.rcParams["figure.figsize"] = (60,30)
      plt.bar(xticks, freq, width=0.2, align="center", color=(0, 0, 1))
      plt.title("Distribution of rainfall values between 1000.0 and 4000.0 mm", fontsize="80")
      plt.xlabel("Rainfall [mm/" + f'{Acc:02d}' + "h]", fontsize="60")
      plt.ylabel("Relative Frequency [%]", fontsize="60")
      plt.xticks(xticks, xticks_labels, rotation=15, fontsize="50")
      plt.yticks(fontsize="50")
      plt.savefig(DirOUT + "/Distr_tp" + f'{Acc:02d}' + "h_1000mm_4000mm.png")
      plt.close()
      [print( " - N. of instances between " + str(np.round_(bins[i],decimals=1)) + " mm (included) and " + str(np.round_(bins[i+1],decimals=1)) + " mm (not included): " + str(hist[i]) ) for i in range(len(hist))]


      ###########################################
      # Plotting the location of "odd" sets of rainfall values

      val = 99.0
      print(" ")
      print("Plotting the location of tp = " + str(val) + " mm ...")
      temp = np.where( align_obs == val )
      len_temp = temp[0].size
      stnids_temp = stnids_unique[temp[0]]
      lats_temp = lats_unique[temp[0]]
      lons_temp = lons_unique[temp[0]]
      dates_temp = []
      [ dates_temp.append(dates[i]) for i in temp[1] ]
      obs_temp = align_obs[temp[0],temp[1]]

      geo = mv.create_geo(
                  type = 'xyv',
                  latitudes = lats_temp,
                  longitudes = lons_temp,
                  values = obs_temp
                  )

      markers = mv.psymb(
                              symbol_type = "marker",
                              symbol_table_mode ="on",
                              legend = "on",
                              symbol_quality = "high",
                              symbol_min_table = [val - 0.01],
                              symbol_max_table = [val + 0.01],
                              symbol_marker_table = [15],
                              symbol_colour_table = ["black"],
                              symbol_height_table = [0.3]
                              )

      png = mv.png_output(output_name = DirOUT + "/Location_" + str(val))
      mv.setoutput(png)
      mv.plot(geo, markers)

      val = 360.0
      print("Plotting the location of tp = " + str(val) + " mm ...")
      temp = np.where( align_obs == val )
      len_temp = temp[0].size
      stnids_temp = stnids_unique[temp[0]]
      lats_temp = lats_unique[temp[0]]
      lons_temp = lons_unique[temp[0]]
      dates_temp = []
      [ dates_temp.append(dates[i]) for i in temp[1] ]
      obs_temp = align_obs[temp[0],temp[1]]

      geo = mv.create_geo(
                  type = 'xyv',
                  latitudes = lats_temp,
                  longitudes = lons_temp,
                  values = obs_temp
                  )

      markers = mv.psymb(
                              symbol_type = "marker",
                              symbol_table_mode ="on",
                              legend = "on",
                              symbol_quality = "high",
                              symbol_min_table = [val - 0.01],
                              symbol_max_table = [val + 0.01],
                              symbol_marker_table = [15],
                              symbol_colour_table = ["black"],
                              symbol_height_table = [0.3]
                              )

      png = mv.png_output(output_name = DirOUT + "/Location_" + str(val))
      mv.setoutput(png)
      mv.plot(geo, markers)

      val = 470.0
      print("Plotting the location of tp = " + str(val) + " mm ...")
      temp = np.where( align_obs == val )
      len_temp = temp[0].size
      stnids_temp = stnids_unique[temp[0]]
      lats_temp = lats_unique[temp[0]]
      lons_temp = lons_unique[temp[0]]
      dates_temp = []
      [ dates_temp.append(dates[i]) for i in temp[1] ]
      obs_temp = align_obs[temp[0],temp[1]]

      geo = mv.create_geo(
                  type = 'xyv',
                  latitudes = lats_temp,
                  longitudes = lons_temp,
                  values = obs_temp
                  )

      markers = mv.psymb(
                              symbol_type = "marker",
                              symbol_table_mode ="on",
                              legend = "on",
                              symbol_quality = "high",
                              symbol_min_table = [val - 0.01],
                              symbol_max_table = [val + 0.01],
                              symbol_marker_table = [15],
                              symbol_colour_table = ["black"],
                              symbol_height_table = [0.3]
                              )

      png = mv.png_output(output_name = DirOUT + "/Location_" + str(val))
      mv.setoutput(png)
      mv.plot(geo, markers)

      val = 475.0
      print("Plotting the location of tp = " + str(val) + " mm ...")
      temp = np.where( align_obs == val )
      len_temp = temp[0].size
      stnids_temp = stnids_unique[temp[0]]
      lats_temp = lats_unique[temp[0]]
      lons_temp = lons_unique[temp[0]]
      dates_temp = []
      [ dates_temp.append(dates[i]) for i in temp[1] ]
      obs_temp = align_obs[temp[0],temp[1]]

      geo = mv.create_geo(
                  type = 'xyv',
                  latitudes = lats_temp,
                  longitudes = lons_temp,
                  values = obs_temp
                  )

      markers = mv.psymb(
                              symbol_type = "marker",
                              symbol_table_mode ="on",
                              legend = "on",
                              symbol_quality = "high",
                              symbol_min_table = [val - 0.01],
                              symbol_max_table = [val + 0.01],
                              symbol_marker_table = [15],
                              symbol_colour_table = ["black"],
                              symbol_height_table = [0.3]
                              )

      png = mv.png_output(output_name = DirOUT + "/Location_" + str(val))
      mv.setoutput(png)
      mv.plot(geo, markers)

      val_min = 600.0
      val_max = 699.9
      print("Plotting the location of " + str(val_min) + " <= tp <= " + str(val_max) + " mm ...")
      temp = np.where( (align_obs >= val_min ) & (align_obs <= val_max) )
      len_temp = temp[0].size
      stnids_temp = stnids_unique[temp[0]]
      lats_temp = lats_unique[temp[0]]
      lons_temp = lons_unique[temp[0]]
      dates_temp = []
      [ dates_temp.append(dates[i]) for i in temp[1] ]
      obs_temp = align_obs[temp[0],temp[1]]

      geo = mv.create_geo(
                  type = 'xyv',
                  latitudes = lats_temp,
                  longitudes = lons_temp,
                  values = obs_temp
                  )

      markers = mv.psymb(
                              symbol_type = "marker",
                              symbol_table_mode ="on",
                              legend = "on",
                              symbol_quality = "high",
                              symbol_min_table = [599.9, 659.99, 669.99, 689.99],
                              symbol_max_table = [659.99, 669.99, 689.99, 699.99],
                              symbol_marker_table = [15],
                              symbol_colour_table = ["black", "blue", "black", "red"],
                              symbol_height_table = [0.3, 0.3, 0.3, 0.3]
                              )

      png = mv.png_output(output_name = DirOUT + "/Location_" + str(val_min) + "_" + str(val_max))
      mv.setoutput(png)
      mv.plot(geo, markers)

      val_min = 700.0
      val_max = 799.9
      print("Plotting the location of " + str(val_min) + " <= tp <= " + str(val_max) + " mm ...")
      temp = np.where( (align_obs >= val_min ) & (align_obs <= val_max) )
      len_temp = temp[0].size
      stnids_temp = stnids_unique[temp[0]]
      lats_temp = lats_unique[temp[0]]
      lons_temp = lons_unique[temp[0]]
      dates_temp = []
      [ dates_temp.append(dates[i]) for i in temp[1] ]
      obs_temp = align_obs[temp[0],temp[1]]

      geo = mv.create_geo(
                  type = 'xyv',
                  latitudes = lats_temp,
                  longitudes = lons_temp,
                  values = obs_temp
                  )

      markers = mv.psymb(
                              symbol_type = "marker",
                              symbol_table_mode ="on",
                              legend = "on",
                              symbol_quality = "high",
                              symbol_min_table = [699.9, 789.99],
                              symbol_max_table = [789.99, 799.99],
                              symbol_marker_table = [15],
                              symbol_colour_table = ["black", "yellowish_orange"],
                              symbol_height_table = [0.3, 0.3]
                              )

      png = mv.png_output(output_name = DirOUT + "/Location_" + str(val_min) + "_" + str(val_max))
      mv.setoutput(png)
      mv.plot(geo, markers)

      val_min = 800.0
      val_max = 899.9
      print("Plotting the location of " + str(val_min) + " <= tp <= " + str(val_max) + " mm ...")
      temp = np.where( (align_obs >= val_min ) & (align_obs <= val_max) )
      len_temp = temp[0].size
      stnids_temp = stnids_unique[temp[0]]
      lats_temp = lats_unique[temp[0]]
      lons_temp = lons_unique[temp[0]]
      dates_temp = []
      [ dates_temp.append(dates[i]) for i in temp[1] ]
      obs_temp = align_obs[temp[0],temp[1]]

      geo = mv.create_geo(
                  type = 'xyv',
                  latitudes = lats_temp,
                  longitudes = lons_temp,
                  values = obs_temp
                  )

      markers = mv.psymb(
                              symbol_type = "marker",
                              symbol_table_mode ="on",
                              legend = "on",
                              symbol_quality = "high",
                              symbol_min_table = [799.9, 879.99],
                              symbol_max_table = [879.99, 899.99],
                              symbol_marker_table = [15],
                              symbol_colour_table = ["black", "green"],
                              symbol_height_table = [0.3, 0.3]
                              )

      png = mv.png_output(output_name = DirOUT + "/Location_" + str(val_min) + "_" + str(val_max))
      mv.setoutput(png)
      mv.plot(geo, markers)

      val = 819.1
      print("Plotting the location of tp = " + str(val) + " mm ...")
      temp = np.where( align_obs == val )
      len_temp = temp[0].size
      stnids_temp = stnids_unique[temp[0]]
      lats_temp = lats_unique[temp[0]]
      lons_temp = lons_unique[temp[0]]
      dates_temp = []
      [ dates_temp.append(dates[i]) for i in temp[1] ]
      obs_temp = align_obs[temp[0],temp[1]]

      geo = mv.create_geo(
                  type = 'xyv',
                  latitudes = lats_temp,
                  longitudes = lons_temp,
                  values = obs_temp
                  )

      markers = mv.psymb(
                              symbol_type = "marker",
                              symbol_table_mode ="on",
                              legend = "on",
                              symbol_quality = "high",
                              symbol_min_table = [val - 0.01],
                              symbol_max_table = [val + 0.01],
                              symbol_marker_table = [15],
                              symbol_colour_table = ["black"],
                              symbol_height_table = [0.3]
                              )

      png = mv.png_output(output_name = DirOUT + "/Location_" + str(val))
      mv.setoutput(png)
      mv.plot(geo, markers)

      val_min = 989.0
      val_max = 989.9
      print("Plotting the location of " + str(val_min) + " <= tp <= " + str(val_max) + " mm ...")
      temp = np.where( (align_obs >= val_min ) & (align_obs <= val_max) )
      len_temp = temp[0].size
      stnids_temp = stnids_unique[temp[0]]
      lats_temp = lats_unique[temp[0]]
      lons_temp = lons_unique[temp[0]]
      dates_temp = []
      [ dates_temp.append(dates[i]) for i in temp[1] ]
      obs_temp = align_obs[temp[0],temp[1]]

      geo = mv.create_geo(
                  type = 'xyv',
                  latitudes = lats_temp,
                  longitudes = lons_temp,
                  values = obs_temp
                  )

      markers = mv.psymb(
                              symbol_type = "marker",
                              symbol_table_mode ="on",
                              legend = "on",
                              symbol_quality = "high",
                              symbol_min_table = [988.99],
                              symbol_max_table = [989.99],
                              symbol_marker_table = [15],
                              symbol_colour_table = ['black'],
                              symbol_height_table = [0.3]
                              )

      png = mv.png_output(output_name = DirOUT + "/Location_" + str(val_min) + "_" + str(val_max))
      mv.setoutput(png)
      mv.plot(geo, markers)

      val_min = 999.0
      val_max = 999.9
      print("Plotting the location of " + str(val_min) + " <= tp <= " + str(val_max) + " mm ...")
      temp = np.where( (align_obs >= val_min ) & (align_obs <= val_max) )
      len_temp = temp[0].size
      stnids_temp = stnids_unique[temp[0]]
      lats_temp = lats_unique[temp[0]]
      lons_temp = lons_unique[temp[0]]
      dates_temp = []
      [ dates_temp.append(dates[i]) for i in temp[1] ]
      obs_temp = align_obs[temp[0],temp[1]]

      geo = mv.create_geo(
                  type = 'xyv',
                  latitudes = lats_temp,
                  longitudes = lons_temp,
                  values = obs_temp
                  )

      markers = mv.psymb(
                              symbol_type = "marker",
                              symbol_table_mode ="on",
                              legend = "on",
                              symbol_quality = "high",
                              symbol_min_table = [998.99, 999.09, 999.89],
                              symbol_max_table = [999.09, 999.89, 999.99],
                              symbol_marker_table = [15],
                              symbol_colour_table = ['black', "magenta", "sky"],
                              symbol_height_table = [0.3, 0.3, 0.3]
                              )

      png = mv.png_output(output_name = DirOUT + "/Location_" + str(val_min) + "_" + str(val_max))
      mv.setoutput(png)
      mv.plot(geo, markers)

      val_min = 1000.0
      val_max = 4000.0
      print("Plotting the location of " + str(val_min) + " <= tp <= " + str(val_max) + " mm ...")
      temp = np.where( (align_obs >= val_min ) & (align_obs <= val_max) )
      len_temp = temp[0].size
      stnids_temp = stnids_unique[temp[0]]
      lats_temp = lats_unique[temp[0]]
      lons_temp = lons_unique[temp[0]]
      dates_temp = []
      [ dates_temp.append(dates[i]) for i in temp[1] ]
      obs_temp = align_obs[temp[0],temp[1]]

      geo = mv.create_geo(
                  type = 'xyv',
                  latitudes = lats_temp,
                  longitudes = lons_temp,
                  values = obs_temp
                  )

      markers = mv.psymb(
                              symbol_type = "marker",
                              symbol_table_mode ="on",
                              legend = "on",
                              symbol_quality = "high",
                              symbol_min_table = [999.99, 1099.99, 1199.99, 1299.99, 1399.99, 1499.99, 1599.99, 1699.99, 1799.99, 1825.99],
                              symbol_max_table = [1099.99, 1199.99, 1299.99, 1399.99, 1499.99, 1599.99, 1699.99, 1799.99, 1825.99, 4000],
                              symbol_marker_table = [15,15,15,15,15,15,15,15,15,15],
                              symbol_colour_table = ["blue", "red", "green", "orange", "yellow", "magenta", "sky", "blue_purple", "gold", "grey"],
                              symbol_height_table = [0.3, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.7]
                              )

      png = mv.png_output(output_name = DirOUT + "/Location_" + str(val_min) + "_" + str(val_max))
      mv.setoutput(png)
      mv.plot(geo, markers)
###############################################################################################################


# Print metadata for final report
print(" ")
print("METADATA")
print("Rainfall observations analysed: " + f'{Acc:02d}' + " hourly")
print("Period analysed: between " + str(YearS) + " and " + str(YearF))
print(DatasetSTVL_list)
print(ReportingTimeSTVL_list)

# Quality checks
for NameOBS in NameOBS_list:

      if NameOBS == "08_AlignOBS_Combine_Years_RawSTVL":
            
            print(" ")
            print("Running quality checks for "+ NameOBS)
            
            # Setting main input/output directories
            MainDirIN = Git_Repo + "/" + DirIN + "/" + NameOBS + "/" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF)
            MainDirOUT = Git_Repo + "/" + DirOUT + "/" + NameOBS + "/" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF)
            if not exists(MainDirOUT):
                  os.makedirs(MainDirOUT)
            
            # Running the quality checks
            quality_check(MainDirIN, MainDirOUT)

      elif NameOBS == "10_AlignOBS_CleanSTVL":

            for Coeff_Grid2Point in Coeff_Grid2Point_list:
                  
                  print(" ")
                  print("Running quality checks for "+ NameOBS + " considering a Coeff_Grid2Point=" + str(Coeff_Grid2Point))
                  
                  # Setting main input/output directories
                  MainDirIN = Git_Repo + "/" + DirIN + "/" + NameOBS + "/Coeff_Grid2Point_" + str(Coeff_Grid2Point) + "/" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF)
                  MainDirOUT = Git_Repo + "/" + DirOUT + "/" + NameOBS + "/Coeff_Grid2Point_" + str(Coeff_Grid2Point) + "/" + f'{Acc:02d}' + "h_" + str(YearS) + "_" + str(YearF)
                  if not exists(MainDirOUT):
                        os.makedirs(MainDirOUT)

                  # Running the quality checks
                  quality_check(MainDirIN, MainDirOUT)