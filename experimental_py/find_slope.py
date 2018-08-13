#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Here, in this script, I learn how to fit regresssion line to temperature data.
Created on Sat Jul 28 08:59:58 2018

@author: haroonr
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#%%
dir = "/Volumes/MacintoshHD2/Users/haroonr/Detailed_datasets/Dominos/"
store = 'Dominos-22'
power = "temp_makeline.csv"
df = pd.read_csv(dir + store + '/' + power,index_col="Datetime")
df.index = pd.to_datetime(df.index)
df_samp_temp = df.resample('1T',label = 'right', closed ='right').mean()
#%%
#df_1 = df_samp['2018-02-01']

#datex = '2018-06-25'
df_2 = df_samp_temp['2018-06-27 10:00:00':'2018-06-27 13:00:00']
#df_2 = df_samp_temp['2018-06-27 13:00:00':'2018-06-27 23:00:00']
savepath = "/Volumes/MacintoshHD2/Users/haroonr/Dropbox/zenatix/paper/pics/"
filename = 'reg-plot-D25-27-06-2018-eve.pdf' # change this name while saving file
compute_slope_diagram(df_2) # this one only plots
#compute_slope_and_save_diagram(df_2,savepath,filename) # it also saves pdf, 
#%%
import copy
from scipy.stats import linregress
def  compute_slope_diagram(df_temp):
    df_temp = copy.copy(df_temp)
    df_temp = df_temp.dropna()
    df_temp.columns = ['Temperature']
    df_temp['num_ind'] = range(1,df_temp.shape[0]+1)
    lf = linregress(df_temp['num_ind'].values, df_temp['Temperature'].values)
    df_temp['Regression line'] = [lf.slope*num + lf.intercept for num in df_temp['num_ind'].values]
    df_temp[['Temperature','Regression line']].plot()
    plt.xlabel('Timestamp')
    plt.ylabel('Temperature (C)')
    plt.show()
    return lf.slope
#%%
def  compute_slope_and_save_diagram(df_temp,savepath, filename):
    df_temp = copy.copy(df_temp)
    df_temp = df_temp.dropna()
    df_temp.columns = ['Temperature']
    df_temp['num_ind'] = range(1,df_temp.shape[0]+1)
    lf = linregress(df_temp['num_ind'].values, df_temp['Temperature'].values)
    df_temp['Regression line'] = [lf.slope*num + lf.intercept for num in df_temp['num_ind'].values]
    df_temp[['Temperature','Regression line']].plot(figsize=(6,4))
    plt.xlabel('Timestamp')
    plt.ylabel('Temperature (C)')
    plt.savefig(savepath+filename)
    plt.close()
    return lf.slope  
#%%
def get_train_test_dates(store_name):
    store_dic = {}
    dic_values = {}
    store_dic['Dominos-22'] = {'train_duration':{'start':'2018-02-10','end': '2018-02-20'},'test_duration':{'start':'2018-03-01','end':'2018-06-30'}}
    store_dic['Dominos-25'] = {'train_duration':{'start':'2018-02-01','end': '2018-02-07'},'test_duration':{'start':'2018-03-01','end':'2018-06-30'}}
    try:
        dic_values = store_dic[store_name]
    except:
        print('the store is not registered in the database: please update this in the method get_train_test_datas method')
    return dic_values
    
    
#%% clustering check
  samp = testdata.to_frame()
  samp =  samp[not samp == 0] # remove intial readings if store started late, otherwise it results in wrong clustering
  # handle nans in data
  nan_obs = int(samp.isnull().sum())
  #rule: if more than 50% are nan then I drop that day from calculcations othewise I drop nan readings only
  if nan_obs:  
    if nan_obs >= 0.50*samp.shape[0]:
      print("More than 50percent missing hence dropping context {}".format(k))
      return (False)
    elif nan_obs < 0.50*samp.shape[0]:
      print("dropping  {} nan observations for total of {} in context {}".format(nan_obs, samp.shape[0], k))
      samp.dropna(inplace=True)
  samp.columns = ['power']
  samp_val =  samp.values
  samp_val = samp_val.reshape(-1,1)
  #FIXME: you can play with clustering options
  if len(samp_val) == 0: # when data is missing  or no data recoreded for the context
      return(False)
#  if np.std(samp_val) <= 0.3:# contains observations with same values, basically forward filled values
#    print("Dropping context {} of day {} from analysis as it contains same readings".format(k,samp.index[0].date()))
#    return (False)
  if np.std(samp_val) <= 0.3: # when applaince reamins ON for full context genuinely
      print("Only one state found in context {} on day {}\n".format(k,samp.index[0].date()))
      if samp_val[2] > 2:
        temp_lab = [1]* (samp_val.shape[0]-1)
        temp_lab.append(0)
        samp['cluster'] = temp_lab
      else:# when applaince reamins OFF for full context genuinely
        temp_lab = [0]* (samp_val.shape[0]-1)
        temp_lab.append(1)
        samp['cluster'] = temp_lab
  else: # normal case, on and off states of appliance
      kobj = perform_clustering(samp_val,clusters=2)
      samp['cluster'] = kobj.labels_
      samp = re_organize_clusterlabels(samp)