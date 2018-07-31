#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Here, in this script, I learn how to fit regresssion line to temperature data.
Created on Sat Jul 28 08:59:58 2018

@author: haroonr
"""

import numpy as np
import pandas as pd
#%%
dir = "/Volumes/MacintoshHD2/Users/haroonr/Detailed_datasets/Dominos/"
store = 'Dominos-22'
power = "temp_makeline.csv"
df = pd.read_csv(dir + store + '/' + power,index_col="Datetime")
df.index = pd.to_datetime(df.index)
df_samp_temp = df.resample('1T',label = 'right', closed ='right').mean()
#%%
df_1 = df_samp['2018-02-01']

datex = '2018-06-25'
df_2 = df_samp['2018-06-25 12:00:00':'2018-06-25 23:00:00']
compute_slope(df_2)
#%%
import copy
from scipy.stats import linregress
def  compute_slope(df_temp):
    df_temp = copy.copy(df_temp)
    df_temp = df_temp.dropna()
    df_temp.columns = ['temp']
    df_temp['num_ind'] = range(1,df_temp.shape[0]+1)
    lf = linregress(df_temp['num_ind'].values, df_temp['temp'].values)
    df_temp['fit'] = [lf.slope*num + lf.intercept for num in df_temp['num_ind'].values]
    df_temp[['temp','fit']].plot()
    return lf.slope
#%%