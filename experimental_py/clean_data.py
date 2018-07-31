#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
In this I format the zenatix data:
  1: Ensure all days have same number of readings
  2: Try to fit the LSTM models
Created on Sat Jul 21 08:48:08 2018

@author: haroonr
"""
import pandas as pd
import datetime
import numpy as np

#%%
dir = "/Volumes/MacintoshHD2/Users/haroonr/Detailed_datasets/Dominos/"
store = 'Dominos-07'
power = "meter_makeline.csv"
df = pd.read_csv(dir + store + '/' + power,index_col="Datetime")
df.index = pd.to_datetime(df.index)
df_samp = df.resample('1T',label = 'right', closed ='right').mean()
df_sel = df_samp.between_time('09:45','23:00')
df_sel = df_sel.current
# create groups and ensure each has same number of readings
df_grp = df_sel.groupby(df_sel.index.date)
day_size = [df_grp.get_group(key).shape[0] for key in df_grp.keys]
if np.unique(day_size).shape[0] != 1:
  print ('Days to not have equal readings so interpolate')
# create matrix of readings or create sequences/episodes
days_obs = pd.DataFrame()
for key,val in df_grp:
  days_obs = days_obs.append(pd.DataFrame(df_grp.get_group(key).values).T)
days_obs.index = np.unique(df_grp.keys)
#%%  
feb_data = days_obs.loc[:datetime.date(2018,2,28)]
train = np.array(feb_data[:datetime.date(2018,2,24)])
train = train.reshape(4,6,160)
test = np.array(feb_data[datetime.date(2018,2,25):datetime.date(2018,2,28)])
test = test.reshape(4,1,160)
#%%  
def create_examples(dff,gp_size):
  X = []
  y = []
  for i in range(0,dff.shape[0], gp_size):
   print (i)
   try:
     X.append(dff.iloc[i:(i+gp_size-1)].values)
     y.append(dff.iloc[i+gp_size].values)
   except:
     print ('exception raised in loop {}'.format(i))
  return X,y
gp_size =  7
X, y = create_examples(feb_data,gp_size) 
#%%
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
#%%
model = Sequential()
model.add(LSTM(10,input_shape = (6,160)))
model.add(Dense(160,activation = 'softmax'))
model.compile(optimizer = 'adam', loss = 'mse')
model.summary()
#%%
model.fit(train,test,nb_epoch=1,verbose=2)
#for i in range(4):
#  model.fit(train[i],test[i],nb_epoch=1,verbose=2)
