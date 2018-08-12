#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
In this script, I compute stats to show that dominos stores have different cycle frequencies to conclude that we can't use only one training model.

This script uses various methods defined in AD_support.py so open that file first and run the file completely to get results.
Apart from that this script is complete and gets results done.

Created on Sat Aug 11 23:38:00 2018

@author: haroonr
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#%%
def compute_cycle_statistics(traindata):
  """ this method computes cycle frequences and durations from the training data
  Input: pandas series of power data in the python groupby object
  Output: Stats computed in form of dictionary """
  dic = OrderedDict()
  #v = traindata.get_group(datetime.date(2018, 2, 1))
  for k, v in traindata:
    #print(k)
    samp = v.to_frame()
    # handle nans in data
    nan_obs = int(samp.isnull().sum())
    #rule: if more than 50% are nan then I drop that day from calculcations othewise I drop nan readings only
    if nan_obs:  
      if nan_obs >= 0.50*samp.shape[0]:
        #print("More than 50percent obs missing hence drop day {} ".format(k))
        continue
      elif nan_obs < 0.50*samp.shape[0]:
        #print("dropping  {} nan observations for day {}".format(nan_obs,k))
        samp.dropna(inplace=True)
    samp.columns = ['power']
    samp_val =  samp.values
    samp_val = samp_val.reshape(-1,1)
    #FIXME: you can play with clustering options
    kobj = perform_clustering(samp_val,clusters=2)
    samp['cluster'] = kobj.labels_
    samp = re_organize_clusterlabels(samp)
    tempval = [(k,sum(1 for i in g)) for k,g in groupby(samp.cluster.values)]
    tempval = pd.DataFrame(tempval,columns=['cluster','samples'])
    #%energy computation logic for eacy cycle
    samp['state_no']  = np.repeat(range(tempval.shape[0]),tempval['samples'])
    samp_groups = samp.groupby(samp.state_no)

    off_cycles = list(tempval[tempval.cluster==0].samples)
    on_cycles = list(tempval[tempval.cluster==1].samples)
    on_cycles_taken =  len(on_cycles)
    off_cycles_taken =  len(off_cycles)
  
    temp_dic = {}
    temp_dic["on"] = on_cycles
    temp_dic["off"] = off_cycles
    temp_dic['on_cycles_taken'] = on_cycles_taken
    temp_dic['off_cycles_taken'] = off_cycles_taken
    dic[str(k)] = temp_dic
    
    #% Merge  OFF and ON states of different days into singe lists 
  ON_duration = []
  OFF_duration = []
  ON_cycles = []
  OFF_cycles = []
 
 #  I am here, now onwards complete the code...................
  for k,v in dic.items():
    ON_duration.append(v['on'])
    OFF_duration.append(v['off'])
    ON_cycles.append(v['on_cycles_taken'])
    OFF_cycles.append(v['off_cycles_taken'])
      
  ON_duration  =  [ item for sublist in ON_duration for item in sublist]
  OFF_duration =  [ item for sublist in OFF_duration for item in sublist]
  ON_cycles  =    [ item for item in ON_cycles ]
  OFF_cycles =    [ item for item in OFF_cycles]
  
   #%
  summ_dic = {}
  #for boxplot logic  
  summ_dic['ON_duration'] = {'mean':round(np.mean(ON_duration),3), 'std':round(np.std(ON_duration),3), 'minimum': min(ON_duration), 'maximum': max(ON_duration)}
  #summ_dic['ON_duration'].update(compute_boxplot_stats(ON_duration))  
  summ_dic['OFF_duration'] = {'mean':round(np.mean(OFF_duration),3), 'std':round(np.std(OFF_duration),3),'minimum': min(OFF_duration), 'maximum': max(OFF_duration)}
  
  summ_dic['ON_cycles'] = {'mean':round(np.mean(ON_cycles),3), 'std':round(np.std(ON_cycles),3), 'minimum': min(ON_cycles), 'maximum': max(ON_cycles)}
  #summ_dic['ON_duration'].update(compute_boxplot_stats(ON_duration))  
  summ_dic['OFF_cycles'] = {'mean':round(np.mean(OFF_cycles),3), 'std':round(np.std(OFF_cycles),3),'minimum': min(OFF_cycles), 'maximum': max(OFF_cycles)}
  
  return (summ_dic)
#%%
def call_cycle_stats(train_data, NoOfContexts, appliance):
    #%create training stats
    """" 1. get data
         2. divide it into different contexts/sets 
         3. divide each into day wise
         4. calculate above stats """
    contexts = create_contexts(train_data, NoOfContexts)      
    
    # create groups within contexts day wise, this will allow us to catch stats at day level otherwise preserving boundaries between different days might become difficult
    contexts_daywise = OrderedDict()
    for k,v in contexts.items():
      contexts_daywise[k] = v.groupby(v.index.date)
     #% Compute stats context wise
    contexts_stats = OrderedDict()
    print("AD module for {} called".format(appliance))
    for k,v in contexts_daywise.items():
        print("Contexts are {}".format(k))
        contexts_stats[k] = compute_cycle_statistics(v) 
    return contexts_stats
  #%%
dir = "/Volumes/MacintoshHD2/Users/haroonr/Detailed_datasets/Dominos/"
#stores = ['Dominos-257','Dominos-22','Dominos-25']
stores = ['Dominos-257', 'Dominos-22','Dominos-186','Dominos-19', 'Dominos-80', 'Dominos-27', 'Dominos-43', 'Dominos-79', 'Dominos-198', 'Dominos-25', 'Dominos-259', 'Dominos-397', 'Dominos-06', 'Dominos-402', 'Dominos-41', 'Dominos-232', 'Dominos-380', 'Dominos-290', 'Dominos-396', 'Dominos-384', 'Dominos-286', 'Dominos-58', 'Dominos-94', 'Dominos-187', 'Dominos-05', 'Dominos-298', 'Dominos-387', 'Dominos-254', 'Dominos-206', 'Dominos-127', 'Dominos-238', 'Dominos-339', 'Dominos-95', 'Dominos-328', 'Dominos-236', 'Dominos-310', 'Dominos-139', 'Dominos-121', 'Dominos-117']
#store = 'Dominos-257'
power = "meter_makeline.csv"
dic = {}
for store in stores:
  print(store)
  df = pd.read_csv(dir + store + '/' + power,index_col="Datetime")
  df.index = pd.to_datetime(df.index)
  df_samp = df.resample('1T',label = 'right', closed ='right').mean()
  df_sel = df_samp.current
  myapp = "DEFY"
  NoOfContexts, appliance = 1, myapp
  train_data =  df_sel['2018-02-01':'2018-02-10'] 
  train_results = call_cycle_stats(train_data, NoOfContexts, appliance)
  #%
  #dfs = pd.DataFrame()
  ON_cycles_mean = train_results['first12_gp']['ON_cycles']['mean']
  ON_cycles_std = train_results['first12_gp']['ON_cycles']['std']
  OFF_cycles_mean = train_results['first12_gp']['OFF_cycles']['mean']
  OFF_cycles_std = train_results['first12_gp']['OFF_cycles']['std']
  ON_duration_mean = train_results['first12_gp']['ON_duration']['mean']
  ON_duration_std = train_results['first12_gp']['ON_duration']['std']
  OFF_duration_mean = train_results['first12_gp']['OFF_duration']['mean']
  OFF_duration_std = train_results['first12_gp']['OFF_duration']['std']
  dic[store] ={'ON_cycles_mean':ON_cycles_mean,'ON_cycles_std':ON_cycles_std,'OFF_cycles_mean':OFF_cycles_mean,'OFF_cycles_std':OFF_cycles_std,'ON_duration_mean':ON_duration_mean,'ON_duration_std':ON_duration_std,'OFF_duration_mean':OFF_duration_mean,'OFF_duration_std':OFF_duration_std}
#%%
res_df = pd.DataFrame.from_dict(dic).T
res_df.to_csv('/Volumes/MacintoshHD2/Users/haroonr/Dropbox/zenatix/results/cycle_statistics_dominos_with_nocontext.csv')

res_df[res_df>150] = 10
#%%
df_select = res_df['ON_cycles_mean','ON_duration_mean','OFF_duration_mean']
df_select.columns = ['Cycles taken','ON cycle duration','OFF cycle duration']
df_select[df_select>150] = 10
df_select.boxplot(column=['ON cycle duration','OFF cycle duration'], return_type='axes',grid=False)
plt.savefig('/Volumes/MacintoshHD2/Users/haroonr/Dropbox/zenatix/paper/pics/cycle_duration.pdf')
plt.close()
#%%
df_select.boxplot(column=['Cycles taken'], return_type='axes',grid=False)
plt.savefig('/Volumes/MacintoshHD2/Users/haroonr/Dropbox/zenatix/paper/pics/cycle_taken.pdf')
plt.close()