#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script creatd to process weather data
Created on Sun Mar 11 08:24:46 2018

@author: haroonr
"""
#%%
import pandas as pd
import numpy as np

#%% Here i read downloaded data along with missing days data, and then process (remvoe duplicates and wrong values, create unix timestamp)

rootdir = "/Volumes/MacintoshHD2/Users/haroonr/Detailed_datasets/IIIT_dataset/weather/"
branchdir = rootdir+"missing_days/"
files = ['year2013_VIDP_station.csv','year2014_VIDP_station.csv','year2015_VIDP_station.csv','year2016_VIDP_station.csv','year2017_VIDP_station.csv']
for file in files:
  #file = "year2013_VIDP_station.csv"
  fl = pd.read_csv(rootdir+ file,index_col='date')
  fl.index = pd.to_datetime(fl.index)
  missing_days = pd.read_csv(branchdir+ file,index_col='date')
  missing_days.index = pd.to_datetime(missing_days.index)
  concated = pd.concat([fl,missing_days],axis=0)
  sortorder = sorted(concated.index)
  concated = concated.loc[sortorder]
  fl = concated # bad habit, laziness
  #identify wrong obs and replace them with nan
  ind = fl.loc[:,'temperature'] < 0 
  fl.loc[ind,'temperature']  = float('nan')
  # remove duplicates
  fl['timestamp'] = fl.index
  fl.drop_duplicates(subset=['timestamp'],inplace=True)
  fl.drop('timestamp',axis=1,inplace=True)
  # set timezone and convert to unix format
  fl.index = fl.index.tz_localize('Asia/Kolkata')
  unix_index = [ind.timestamp() for ind in fl.index]
  fl.index = unix_index
  save_dir = rootdir +'processed/'
  fl.to_csv(save_dir+file) 
#%%
