#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
In this experiment I understand how CUSUM statistical method works.
I have tested it on real data. Please check bottom part of the script too.
Following e.g., is taken from https://www.measurementlab.net/publications/CUSUMAnomalyDetection.pdf for learning purposes
Created on Fri Aug  3 08:34:30 2018

@author: haroonr
"""
%matplotlib inline
import pandas as pd
import matplotlib.pyplot as plt
#%%
random.seed(123)
ser1 = list(np.random.normal(50, 3, 100))
ser2 = list(np.random.normal(54, 3, 40))
ser3 = list(np.random.normal(50, 3, 100))

full_series = [ser1,ser2,ser3]
full_series = [item for ser in full_series for item in ser]

row = 50 # row means arithematic mean of the series
sigma = 3 # sigma means standard deviation of the series
s_above = []
s_above.append(0)
s_below = []
s_below.append(0)
control_above = [5*sigma] * len(full_series)
control_below = [-5*sigma] * len(full_series)
for i in range(1,len(full_series)):
    #print(i)
    s_above.append( max(0, s_above[i-1] + full_series[i] - row - sigma ) )
    s_below.append( min(0, s_below[i-1] + full_series[i] - row + sigma ) )
#%%
   df =  pd.DataFrame({'upper_limit':control_above,'lower_limit': control_below,'above_s':s_above,'below_s': s_below})
   df.plot()
#%% Now let's run CUSUM model on actal data and see how it works
dir = "/Volumes/MacintoshHD2/Users/haroonr/Detailed_datasets/Dominos/"
store = 'Dominos-25'
power = "meter_makeline.csv"
df = pd.read_csv(dir + store + '/' + power,index_col="Datetime")
df.index = pd.to_datetime(df.index)
df_samp = df.resample('1T',label = 'right', closed ='right').mean()
df_sel = df_samp.current
df_sel = df_sel.between_time('10:00','23:00')

dates = ads.get_train_test_dates(store)
train_data = df_sel[dates['train_duration']['start']:dates['train_duration']['end']]
test_data  = df_sel[dates['test_duration']['start']:dates['test_duration']['end']]
#%%
row = np.mean(train_data)
sigma = np.std(train_data)

full_series = list(test_data['2018-03-01':'2018-03-03'].values)
s_above = []
s_above.append(0)
s_below = []
s_below.append(0)
control_above = [5*sigma] * len(full_series)
control_below = [-5*sigma] * len(full_series)
for i in range(1,len(full_series)):
    #print(i)
    s_above.append( max(0, s_above[i-1] + full_series[i] - row - sigma ) )
    s_below.append( min(0, s_below[i-1] + full_series[i] - row + sigma ) )
#%%
df =  pd.DataFrame({'upper_limit':control_above,'lower_limit': control_below,'above_s':s_above,'below_s': s_below})
df.plot()
plt.plot(full_series)