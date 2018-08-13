#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 12 10:50:34 2018

@author: haroonr
"""

#%%
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
result = apply_CUSUM_method(train_data,test_data)
gps = result.groupby(result.index.date)
keys = np.unique(result.index.date)
positive = []
negative = []
for k in keys:
  data = gps.get_group(k)
  negative_anom = sum(data['below_s'] < data['lower_limit'])
  positive_anom = sum(data['above_s'] > data['upper_limit'])
  positive.append(positive_anom)
  negative.append(negative_anom)
  
resframe = pd.DataFrame({'day':keys,'positive_anom':positive,'negative_anom':negative})
#%%
def apply_CUSUM_method(train_data,test_data):
  
  row = np.mean(train_data)
  sigma = np.std(train_data)
  
  #full_series = list(test_data['2018-03-01':'2018-03-03'].values)
  full_series = list(test_data.values)
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
  df =  pd.DataFrame({'upper_limit':control_above,'lower_limit': control_below,'above_s':s_above,'below_s': s_below})
  df.index = test_data.index
  return df

sum(data['below_s'] < data['lower_limit'])
sum(data['above_s'] > data['upper_limit'])