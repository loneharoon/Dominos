#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
In this script, I will show variation in Production zone AND MAKELINE temeperature on different days
Created on Tue Aug 14 11:42:03 2018

@author: haroonr
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#sys.path.append('/volumes/MacintoshHD2/Users/haroonr/Dropbox/Zenatix/Dominos/experimental_py/')
#import AD_support as ads
#%%
dirs = "/Volumes/MacintoshHD2/Users/haroonr/Detailed_datasets/Dominos/Dominos-25/production_temperature.csv"
df = pd.read_csv(dirs,header=None)
df.columns = ['timestamp','temperature']
df.index = pd.to_datetime(df.timestamp) + pd.Timedelta('5 hours 30 minutes')
df.drop(['timestamp'],inplace=True,axis=1)
#%%
df_sel = df['2018-02-01':'2018-06-28']
df_samp = df_sel.resample('1H',label = 'right', closed ='right').mean()
df_samp = df_samp.between_time('9:00','23:00')
df_samp['hour'] =  df_samp.index.hour
df_samp.boxplot(by='hour',grid=False, figsize=(6,3),fontsize=8)
plt.xlabel('Day Hour')
plt.ylabel('Temperature (Celsius)')
plt.title('')
#plt.show()
savepath = "/Volumes/MacintoshHD2/Users/haroonr/Dropbox/zenatix/paper/pics/"
plt.savefig(savepath+'production_temperature_D25.pdf')
plt.close()

#%% NOW LET US PLOT MAKELINE TEMPEATURE OF SOME STORE
dirs = "/Volumes/MacintoshHD2/Users/haroonr/Detailed_datasets/Dominos/Dominos-25/temp_makeline.csv"
df = pd.read_csv(dirs)
df.columns = ['timestamp','temperature']
df.index = pd.to_datetime(df.timestamp) 
df.drop(['timestamp'],inplace=True,axis=1)
#%%
df_sel = df['2018-06-01':'2018-06-28']
df_samp = df_sel.resample('1H',label = 'right', closed ='right').mean()
df_samp = df_samp.between_time('9:00','23:00')
df_samp['hour'] =  df_samp.index.hour
df_samp.boxplot(by='hour',grid=False, figsize=(6,3),fontsize=8)
plt.xlabel('Day Hour')
plt.ylabel('Temperature (Celsius)')
plt.title('')
#plt.show()
savepath = "/Volumes/MacintoshHD2/Users/haroonr/Dropbox/zenatix/paper/pics/"
plt.savefig(savepath+'makeline_temperature_D25.pdf')
plt.close()