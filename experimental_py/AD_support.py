#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CODE borrowed from REFIT PROJECT
This contains different function defintions for anomaly detection on REFIT
Created on Tue Jan  2 08:54:04 2018

@author: haroonr
"""
#%%
from __future__ import division
import pandas as pd
from sklearn.cluster import KMeans
import numpy as np
from copy import deepcopy
from itertools import groupby
import standardize_column_names as scn
from collections import OrderedDict,Counter
from datetime import datetime,timedelta
import re
import os
import my_utilities as myutil
import  matplotlib.pyplot  as plt

#%%

def compute_tp_fp_fn_Dominso(gt,est):
    gt_day = list(gt.day)
    ob_day = list(est.timestamp)
    tp = fp = fn = 0
    for i in ob_day:
        if i in gt_day:
            tp = tp + 1
        else:
            fp = fp + 1 
    for j in gt_day:
        if j not in ob_day:
            fn = fn + 1 
    return tp, fp, fn
def compute_AD_confusion_metrics(gt,ob):
    gt = gt[gt.Status=='S'] # only sure anomalies in ground truth
    print('\n Computing results w.r.t Sure anomalies only\n')
    gt_day = gt.day.values
    ob_day = ob.day.values
    tp=fp=fn = 0
    precision = recall = fscore = np.nan
    for i in ob_day:
        if i in gt_day:
            tp = tp + 1
        else:
            fp = fp + 1 
    for j in gt_day:
        if j not in ob_day:
            fn = fn + 1 
    print('\n tp {}, fp {}, fn {}\n'.format(tp,fp,fn))
    try:
        precision = round(tp/(tp + fp),2)
    except :
        print ("Precision results in error\n")
    try:
        recall = round(tp/(tp + fn),2)
    except :
        print ("Recall results in error\n")
    try:
        fscore= round(2*(precision * recall)/(precision+recall),2)
    except :
        print ("Recall results in error\n")
    return precision,recall,fscore
#%%
def compute_tp_fp_fn(gt,est):
    gt_day = list(gt.day)
    ob_day = list(est.timestamp)
    tp = fp = fn = 0
    precision = recall = fscore = np.nan
    for i in ob_day:
        if i in gt_day:
            tp = tp + 1
        else:
            fp = fp + 1 
    for j in gt_day:
        if j not in ob_day:
            fn = fn + 1 
    return tp, fp, fn
def compute_tp_fp_fn(gt,ob):
    gt = gt[gt.Status == 'S'] # only sure anomalies in ground truth
    print('\n Computing results w.r.t Sure anomalies only\n')
    gt_day = gt.day.values
    ob_day = ob.day.values
    tp = fp = fn = 0
    #precision = recall = fscore = np.nan
    for i in ob_day:
        if i in gt_day:
            tp = tp + 1
        else:
            fp = fp + 1 
    for j in gt_day:
        if j not in ob_day:
            fn = fn + 1 
    print('\n tp {}, fp {}, fn {}\n'.format(tp,fp,fn))
    return tp,fp,fn
#%%
def show_tp_fp_fn_dates(gt,ob):
    '''This returns the list of all fp, tp, and fn dates'''
    gt = gt[gt.Status=='S'] # only sure anomalies in ground truth
    print('\n Computing results w.r.t Sure anomalies only\n')
    gt_day = gt.day.values
    ob_day = ob.day.values
    tp = fp = fn = 0
    tp_list = []
    fp_list = []
    fn_list = []
    #precision = recall = fscore = np.nan
    for i in ob_day:
        if i in gt_day:
            tp = tp + 1
            tp_list.append(i)
        else:
            fp = fp + 1 
            fp_list.append(i)
    for j in gt_day:
        if j not in ob_day:
            fn = fn + 1 
            fn_list.append(j)
    print('\n tp {}, fp {}, fn {}\n'.format(tp,fp,fn))
    return tp, fp, fn, tp_list, fp_list, fn_list

#%%
def read_REFIT_groundtruth():
  
  ''' This function reads and formats REFIT's groundtruth file
  return: intelligible pandas dataframe'''
  gt_file = "/Volumes/MacintoshHD2/Users/haroonr/Dropbox/UniOfStra/AD/anomaly_explanation.csv"
  gt_df  = pd.read_csv(gt_file)
  df_temp =  [(i.split(';')[0],i.split(';')[1]) for i in gt_df.Time_Duration.values]
  df_temp =  pd.DataFrame(df_temp)
  df_temp.columns = ["start_time","end_time"]
  
  start_times = [pd.to_datetime(val.replace('"','')) if val.rfind('"')>=0 else pd.to_datetime(val.replace('“','')) for val in df_temp['start_time']]
  end_times = [pd.to_datetime(val.replace('"','')) if val.rfind('"')>=0 else pd.to_datetime(val.replace('”','')) for val in df_temp['end_time']]
  gt_df['start_time'] = start_times
  gt_df['end_time'] = end_times
  return(gt_df)

#%%
def perform_clustering(samp,clusters):
  #TODO: this has not been completed yet
  # http://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html#sklearn.cluster.KMeans
  kmeans = KMeans(n_clusters=clusters, random_state=0).fit(samp)
  #kmeans.labels_
  #kmeans.cluster_centers_
  return (kmeans)
###
def re_organize_clusterlabels(samp):
  """this function checks if labels assigned to data are correct. Less consumption should get lower label and higher should get high label. Doing This maintains consistency across different days and datasets and allows comparison
 input: samp pandas dataframe has  columns: power and cluster
 ouput: pandas dataframe """
  dic = {}
  for i in np.unique(samp.cluster):
    dic[i] = samp[samp.cluster==i].power.iloc[0]
  if not sorted(list(dic.values())) == list(dic.values()):
    #if cluster labels are not assigned acc. to usage levels, i.e., less consumption should get lower label and so on
     p = pd.DataFrame(list(dic.items()))
     p.columns = ['old_label','value']
     q = p.sort_values('value')
     q['new_label'] = range(0,q.shape[0])
     r = dict(zip(q.old_label,q.new_label))
     samp['new_cluster'] =  [r[i] for i in samp['cluster'].values]
     samp.cluster = samp.new_cluster
     samp.drop('new_cluster',axis=1,inplace=True)
  return (samp)
#%%
###
def compute_boxplot_stats(boxdata):
  ''' Here i compute all stats of boxplot and return them as dictionary'''
  boxdict = OrderedDict()
  nmedian =  np.median(boxdata)
  istquat =  np.percentile(boxdata,0)
  thirdquat =  np.percentile(boxdata,100)
  iqr = thirdquat - istquat
  boxdict['nmedian'] = nmedian
  boxdict['lowerwisker'] =  nmedian - 1.5 * iqr 
  boxdict['upperwisker'] =  nmedian + 1.5 * iqr
  return (boxdict)
#%%
###
def create_training_stats(traindata,sampling_type,sampling_rate):
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
    energy_state= [np.sum(v.power*220)/1000 for k,v in samp_groups] # since power is a misnomer for current here, so I multiple it by 220 voltage to get figures correct, and  dividing by 1000 to convert watts to Killowats as in next steps I want to compute KWH instead of WH (watthour)
    group_magnitude_mean = [np.mean(v.power) for k,v in samp_groups]
    group_magnitude_std = [np.std(v.power) for k,v in samp_groups]
    if sampling_type =='minutes':
      energy_state = np.multiply(energy_state, (sampling_rate/60.))
    elif sampling_type == 'seconds':
      energy_state = np.multiply(energy_state, (sampling_rate/3600.)) 
    tempval['energy_state'] =  np.round(energy_state,2)
    tempval['magnitude_mean'] = np.round(group_magnitude_mean,3)
    tempval['magnitude_std']  = np.round(group_magnitude_std, 3)
   #% energy logic ends
    off_cycles = list(tempval[tempval.cluster==0].samples)
    on_cycles = list(tempval[tempval.cluster==1].samples)
    off_energy = list(tempval[tempval.cluster==0].energy_state)
    on_energy = list(tempval[tempval.cluster==1].energy_state)
    on_magnitude_mean = list(tempval[tempval.cluster==1].magnitude_mean)
    off_magnitude_mean = list(tempval[tempval.cluster==0].magnitude_mean)
    on_magnitude_std = list(tempval[tempval.cluster==1].magnitude_std)
    off_magnitude_std = list(tempval[tempval.cluster==0].magnitude_std)
    
    temp_dic = {}
    temp_dic["on"] = on_cycles
    temp_dic["off"] = off_cycles
    temp_dic["on_energy"] = on_energy
    temp_dic["off_energy"] = off_energy
    temp_dic['on_magnitude_mean'] = on_magnitude_mean
    temp_dic['off_magnitude_mean'] = off_magnitude_mean
    temp_dic['on_magnitude_std'] = on_magnitude_std
    temp_dic['off_magnitude_std'] = off_magnitude_std
    cycle_stat = Counter(tempval.cluster)
    temp_dic.update(cycle_stat)
    dic[str(k)] = temp_dic
    #% Merge  OFF and ON states of different days into singe lists 
  ON_duration = []
  OFF_duration = []
  ON_energy = []
  OFF_energy = []
  ON_cycles = []
  OFF_cycles = []
  ON_duration_mag = []
  OFF_duration_mag = []
  ON_duration_std = []
  OFF_duration_std = []
 #  I am here, now onwards complete the code...................
  for k,v in dic.items():
    ON_duration.append(v['on'])
    OFF_duration.append(v['off'])
    ON_energy.append(v['on_energy'])
    OFF_energy.append(v['off_energy'])
    ON_cycles.append(v[1])
    OFF_cycles.append(v[0])
    ON_duration_mag.append(v['on_magnitude_mean'])
    ON_duration_std.append(v['on_magnitude_std'])
    OFF_duration_mag.append(v['off_magnitude_mean'])
    OFF_duration_std.append(v['off_magnitude_std'])
    
  ON_duration  =  [ item for sublist in ON_duration for item in sublist]
  OFF_duration = [ item for sublist in OFF_duration for item in sublist]
  ON_energy  =  [ item for sublist in ON_energy for item in sublist]
  OFF_energy = [ item for sublist in OFF_energy for item in sublist]
  Magnitude_on_mean  = [ item for sublist in ON_duration_mag for item in sublist]
  Magnitude_off_mean = [ item for sublist in OFF_duration_mag for item in sublist]
  Magnitude_on_std   = [ item for sublist in ON_duration_std for item in sublist]
  Magnitude_off_std  = [ item for sublist in OFF_duration_std for item in sublist]
  
   #%
  summ_dic = {}
  #for boxplot logic  
  summ_dic['ON_duration'] = {'mean':round(np.mean(ON_duration),3), 'std':round(np.std(ON_duration),3)}
  summ_dic['ON_duration'].update(compute_boxplot_stats(ON_duration))  
  summ_dic['OFF_duration'] = {'mean':round(np.mean(OFF_duration),3), 'std':round(np.std(OFF_duration),3)}
  summ_dic['OFF_duration'].update(compute_boxplot_stats(OFF_duration))
  summ_dic['ON_energy'] = {'mean':round(np.mean(ON_energy),3), 'std':round(np.std(ON_energy),3)}
  summ_dic['ON_energy'].update(compute_boxplot_stats(ON_energy))
  summ_dic['OFF_energy'] = {'mean':round(np.mean(OFF_energy),3), 'std':round(np.std(OFF_energy),3)}
  summ_dic['OFF_energy'].update(compute_boxplot_stats(OFF_energy))
  summ_dic['ON_cycles'] = {'mean':round(np.mean(ON_cycles),0), 'std':round(np.std(ON_cycles),3)}
  summ_dic['ON_cycles'].update(compute_boxplot_stats(ON_cycles))
  summ_dic['OFF_cycles'] = {'mean':round(np.mean(OFF_cycles),0), 'std':round(np.std(OFF_cycles),3)}
  summ_dic['OFF_cycles'].update(compute_boxplot_stats(OFF_cycles))
  summ_dic['ON_magnitude'] = {'mean':round(np.mean(Magnitude_on_mean),3),'std':round(np.mean(Magnitude_on_std),3)}
  summ_dic['OFF_magnitude'] = {'mean':round(np.mean(Magnitude_off_mean),3),'std':round(np.mean(Magnitude_off_std),3)}
  #for debugging purpose
#  print(compute_boxplot_stats(ON_duration))
#  print(compute_boxplot_stats(OFF_duration))
 # print(compute_boxplot_stats(ON_cycles))
  return (summ_dic)

#%%
def  create_testing_stats_with_boxplot(testdata,k,sampling_type,sampling_rate):
  """  """
  temp_dic = {}
  #for k, v in testdata:
    #print(k)
  samp = testdata.to_frame()
  samp =  samp[samp != 0] # remove intial readings if store started late, otherwise it results in wrong clustering
  # handle nans in data
  nan_obs = int(samp.isnull().sum())
  #rule: if more than 50% are nan then I drop that day from calculcations othewise I drop nan readings only
  if nan_obs:  
    if nan_obs >= 0.50*samp.shape[0]:
      #print("More than 50percent missing hence dropping context {}".format(k))
      return (False)
    elif nan_obs < 0.50*samp.shape[0]:
      #print("dropping  {} nan observations for total of {} in context {}".format(nan_obs, samp.shape[0], k))
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
  
  tempval = [(h,sum(1 for i in g)) for h,g in groupby(samp.cluster.values)]
  tempval = pd.DataFrame(tempval,columns=['cluster','samples'])
  #%energy computation logic for eacy cycle
  samp['state_no']  = np.repeat(range(tempval.shape[0]),tempval['samples'])
  samp_groups = samp.groupby(samp.state_no)
  temp_energy_state= [np.sum(v.power*220)/1000 for h,v in samp_groups] 
  group_magnitude_mean = [np.mean(v.power) for h,v in samp_groups]
  group_magnitude_std  = [np.std(v.power) for h,v in samp_groups]
  if sampling_type =='minutes':
    temp_energy_state = np.multiply(temp_energy_state, (sampling_rate/60.)) # energy formula
  elif sampling_type == 'seconds':
    temp_energy_state = np.multiply(temp_energy_state, (sampling_rate/3600.)) # energy formula
  tempval['energy_state'] =  np.round(temp_energy_state,2)
  tempval['magnitude_mean'] = np.round(group_magnitude_mean,3)
  tempval['magnitude_std']  = np.round(group_magnitude_std, 3)

 #% energy logic ends
  off_cycles =list(tempval[tempval.cluster==0].samples)
  on_cycles =list(tempval[tempval.cluster==1].samples)
  off_energy =list(tempval[tempval.cluster==0].energy_state)
  on_energy =list(tempval[tempval.cluster==1].energy_state)
  on_magnitude_mean = list(tempval[tempval.cluster==1].magnitude_mean)
  off_magnitude_mean = list(tempval[tempval.cluster==0].magnitude_mean)
  on_magnitude_std = list(tempval[tempval.cluster==1].magnitude_std)
  off_magnitude_std = list(tempval[tempval.cluster==0].magnitude_std)
  #print(on_energy)
  temp_dic["on_energy"] = on_energy
  temp_dic["off_energy"] = off_energy
  temp_dic["on"] = on_cycles
  temp_dic["off"] = off_cycles
  temp_dic['on_magnitude_mean'] = on_magnitude_mean
  temp_dic['on_magnitude_std'] = on_magnitude_std
  temp_dic['off_magnitude_mean'] = off_magnitude_mean
  temp_dic['off_magnitude_std'] = off_magnitude_std
  cycle_stat = Counter(tempval.cluster)
  temp_dic.update(cycle_stat)
  summ_dic = OrderedDict()
  summ_dic['ON_duration'] = temp_dic["on"]
  summ_dic['OFF_duration'] = temp_dic["off"]
  summ_dic['ON_energy'] = temp_dic["on_energy"]
  summ_dic['OFF_energy'] = temp_dic["off_energy"]
  summ_dic['ON_cycles'] = temp_dic[1]
  summ_dic['OFF_cycles'] = temp_dic[0]
  summ_dic['ON_magnitude_mean'] = temp_dic['on_magnitude_mean']
  summ_dic['ON_magnitude_std'] = temp_dic['on_magnitude_std']
  summ_dic['OFF_magnitude_mean'] = temp_dic['off_magnitude_mean']
  summ_dic['OFF_magnitude_std'] = temp_dic['off_magnitude_std']
  return (summ_dic)
#%% Anomaly detection logic
def anomaly_detection_algorithm(test_stats,contexts_stats,alpha,num_std):
  ''' this function defines the anomaly detection logic '''
  LOG_FILENAME = '/Volumes/MacintoshHD2/Users/haroonr/Downloads/REFIT_log/logfile_REFIT.csv'
  with open(LOG_FILENAME,'a') as mylogger:
  
    mylogger.write("\n*****NEW ITERATION at time {}*************\n".format(datetime.now()))
    result = [] 
    for day,data in test_stats.items():
      for contxt,contxt_stats in data.items():
        #be clear - word contexts_stats [spelling stress] represents training data and word contxt represents test day stats
        train_results = contexts_stats[contxt] # all relevant train stats
        test_results  = contxt_stats
        temp_res = {}
        temp_res['timestamp'] = datetime.strptime(day,'%Y-%m-%d')
        temp_res['context']   = contxt # denotes part of the day
        temp_res['status']    = 0 # 1 will mean anomalous
        temp_res['anomtype']  = np.float("Nan") # anomaly type
        
        # rule 1: when compressor shuts in middle of a day
        if  np.mean(test_results['ON_magnitude_std']) > 20:
            temp_res['status'] = 1
            temp_res['anomtype'] = "compressor-down"
            print('one compressor shut on day {} at context {}'.format(day,contxt ))
            #mylogger.write(day + ":" + contxt + "is not elongated anomaly as off time was also longer \n")
            mylogger.write(day + ":"+ contxt + ", compressor-down-halfday" + ", train_stats, " + str(train_results['ON_magnitude']['mean']) + ":" + str(train_results['ON_magnitude']['std']) + "; test_stats, " + str(np.mean(test_results['ON_magnitude_std'])) + "\n" )
        # rule 2: when compressors are shut for entire day beginning from morning
        elif np.mean(test_results['ON_magnitude_mean']) <= (train_results['ON_magnitude']['mean'])/2:
            temp_res['status'] = 1
            temp_res['anomtype'] = "compressor-down"
            print('one compressor shut for entire context {} on day {}'.format(contxt, day))
            mylogger.write(day + ":"+ contxt + ", compressor-down-fullday" + ", train_stats, " + str(train_results['ON_magnitude']['mean']) + ":"+ str(train_results['ON_magnitude']['std']) + "; test_stats, " + str(np.mean(test_results['ON_magnitude_mean'])) + ":" + str(np.mean(test_results['ON_magnitude_std'])) + "\n" )
        elif np.mean(test_results['ON_duration']) > alpha * train_results['ON_duration']['mean'] + num_std* train_results['ON_duration']['std']:
          temp_res['status'] = 1
          temp_res['anomtype'] = "long-ON-cycle"
          print('Cycles with large  ON cycle duration in context {} on day {}'.format(contxt, day))
          mylogger.write(day + ":" + contxt + ", Long ON cycles" + ", train_stats, " + str(train_results['ON_duration']['mean']) + ":" + str(train_results['ON_duration']['std']) + "; test_stats, " + str(np.mean(test_results['ON_duration'])) + ":" + str(np.std(test_results['ON_duration'])) + "\n" )
        result.append(temp_res)
    res_df = pd.DataFrame.from_dict(result)
  return(res_df[res_df.status == 1]) # returns only anomaly packets 


#%%
def AD_refit_training(train_data, data_sampling_type, data_sampling_time, NoOfContexts, appliance):
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
        contexts_stats[k] = create_training_stats(v,sampling_type=data_sampling_type,sampling_rate=data_sampling_time) 
    return contexts_stats
#%%
def create_contexts(data, NoOfContexts):
    
    if NoOfContexts == 1:
        contexts = OrderedDict()
        contexts['all24_gp'] = data.between_time("00:00","23:59:59")
    elif NoOfContexts == 2:
        contexts = OrderedDict()
        contexts['first12_gp'] = data.between_time('09:45:00','12:59:59')
        contexts['last12_gp'] = data.between_time("13:00:00","23:00:00")
    elif  NoOfContexts == 3:
        contexts = OrderedDict()
        contexts['first8_gp'] = data.between_time("00:00","07:59:59")
        contexts['next8_gp'] = data.between_time("08:00","15:59:59")
        contexts['last8_gp'] = data.between_time("16:00","23:59:59")    
    else:
        raise ValueError("Please provide contexts which make sense\n")
    return (contexts)
#%%
def return_context_timeboundary(contxt):
    
    hdic = {}
    hdic['first12_gp'] = ["09:45:00","12:59:59"]
    hdic['last12_gp'] = ["13:00:00","23:00:00"]
    return hdic[contxt]
#%%
import copy
from scipy.stats import linregress
def  compute_slope(df_temp):
    df_temp = copy.copy(df_temp)
    df_temp = df_temp.dropna() # dropping NA values
    if df_temp.shape[0] == 0: # if empty frame left
        return -55
    df_temp.columns = ['temp']
    df_temp['num_ind'] = range(1,df_temp.shape[0]+1)
    lf = linregress(df_temp['num_ind'].values, df_temp['temp'].values)
    df_temp['fit'] = [lf.slope*num + lf.intercept for num in df_temp['num_ind'].values]
    #df_temp[['temp','fit']].plot()
    return lf.slope
#%%
def AD_refit_testing(test_data,data_sampling_type,data_sampling_time,NoOfContexts,appliance):
    
    test_data_daywise = test_data.groupby(test_data.index.date) # daywise groupings
    test_contexts_daywise = OrderedDict()
    for k,v in test_data_daywise:     # context wise division
       test_contexts_daywise[str(k)] = create_contexts(v,NoOfContexts)
    test_stats = OrderedDict()
    
    for day,data in test_contexts_daywise.items():
      temp = OrderedDict()
      for context,con_data in data.items():
          res = create_testing_stats_with_boxplot(con_data,context,sampling_type=data_sampling_type,sampling_rate=data_sampling_time)
          if res!= False:
            temp[context] = res
          else:
            continue   
      test_stats[day] = temp
    return test_stats
#%%

#%%
def tidy_gt_and_ob(house_no, appliance, day_start, day_end, result_sub):
    '''In this I re_format gt and observed results for calculating end results '''
    gt = read_REFIT_groundtruth()
    select_house = gt.House_No==house_no
    select_appliance = gt.Appliance==appliance
    gt_sub = gt[select_house & select_appliance]
    gt_appliance = deepcopy (gt_sub[(gt_sub.start_time >= day_start) & (gt_sub.end_time <= day_end)])
    columns = gt_appliance.columns.values.tolist()
    columns.append('day')
    gt_df = pd.DataFrame(columns= columns)
    for i in range(len(gt_appliance)):
        start = gt_appliance.start_time.iloc[i].date()
        end = gt_appliance.end_time.iloc[i].date()
        temp = gt_appliance.iloc[i]
         # if anomaly continued on more than one day then duplicate rows for th e range
        #days = pd.date_range(start,end) # this creates timestamp object, so dump it 
        total_days = (end - start).days + 1
        days = [start + timedelta(days=x) for x in range(0, total_days)]
        temp2 = pd.DataFrame([temp]*total_days)
        temp2['day'] = days
        gt_df = gt_df.append(temp2) 
        
    #% # Now format observed results properly
    result_appliance = deepcopy(result_sub)
    # convert timestamp to dates
    result_appliance['day']= result_appliance.updated_timestamp.apply(lambda x: x.date()).tolist()
    # remove duplicated entries
    result_appliance = result_appliance[~result_appliance.duplicated('day')]
    # drop few columns of gt
    drop_names = ['Explanation','Time_Duration','Comments','start_time','end_time']
    gt_df.drop(drop_names,inplace=True,axis=1)
    return gt_df,result_appliance  
#%%
def compute_noise_percentage(actual_power):
    '''Metric copied from Stephen Makonins paper '''
    temp = deepcopy(actual_power)
    aggregate_df =  temp['use']
    appliance_df = np.sum(temp.drop(['use'],axis=1),axis=1)
    
    numerator = abs(aggregate_df - appliance_df)
    denominator =  np.sum(aggregate_df)
    noise_percent = (np.sum(numerator)/denominator) *100
    return noise_percent
 #%%
def get_selected_home_data(home,df_selected):
     if home == "House10.csv":
         train_dset = df_selected['2014-04-01':'2014-04-30'] # home10
         test_dset = df_selected['2014-05-01':] #home 10
     elif home == "House20.csv": 
         train_dset = df_selected['2014-05-01':'2014-05-31'] # home20
         test_dset = df_selected['2014-06-01':] #home 20
     elif home == "House18.csv":
         train_dset = df_selected['2014-07-01':'2014-07-31'] # home18
         test_dset = df_selected['2014-08-01':] #home 18
     elif home == "House16.csv":    
         train_dset = df_selected['2014-03-01':'2014-03-31'] # home16
         test_dset = df_selected['2014-04-01':] #home 16
     elif home == "House1.csv":    
         train_dset = df_selected['2014-12'] # home1
         test_dset = df_selected['2015-01':'2015-04'] #home 1
     else :
         raise ValueError ("Supply data selection details for the home")
     train_dset.dropna(inplace=True)
     test_dset.dropna(inplace=True)
     return train_dset,test_dset
#%%
def get_selected_home_appliance(home):
     if home == "House10.pkl":
         myapp = "Chest_Freezer"# ho
     elif home == "House20.pkl": 
         myapp = "Freezer"# home 
     elif home == "House18.pkl":
         myapp = "Fridge_Freezer"# home
     elif home == "House16.pkl":    
         myapp = "Fridge_Freezer_1"# home
     elif home == "House1.pkl":    
         myapp = "ElectricHeater"# home 
     else :
         raise ValueError ("Supply correct home details")
     return myapp
#%%
def anomalous_days_from_gt(house_no,appliance,day_start,day_end):
    ''' This returns anomalous days from the ground truth for the specific applaince '''
    gt = read_REFIT_groundtruth()
    select_house = gt.House_No==house_no
    select_appliance = gt.Appliance==appliance
    gt_sub = gt[select_house & select_appliance]
    gt_appliance = deepcopy(gt_sub[(gt_sub.start_time >= day_start) & (gt_sub.end_time <= day_end)])
    columns = gt_appliance.columns.values.tolist()
    columns.append('day')
    gt_df = pd.DataFrame(columns= columns)
    for i in range(len(gt_appliance)):
        start = gt_appliance.start_time.iloc[i].date()
        end = gt_appliance.end_time.iloc[i].date()
        temp = gt_appliance.iloc[i]
         # if anomaly continued on more than one day then duplicate rows for th e range
        #days = pd.date_range(start,end) # this creates timestamp object, so dump it 
        total_days = (end - start).days + 1
        days = [start + timedelta(days=x) for x in range(0, total_days)]
        temp2 = pd.DataFrame([temp]*total_days)
        temp2['day'] = days
        gt_df = gt_df.append(temp2)
    return (gt_df.day)

#%%
def find_my_anomalous_dates_from_gt(home):    
    myapp = get_selected_home_appliance(home)
    start_date,end_date = get_test_dates(home)
    home = home.split('.')[0]+'.csv'
    appliance = scn.reverse_lookup(home,myapp) # find actual name of appliance in anomaly database
    assert len(appliance) > 1
    house_no =  int(re.findall('\d+',home)[0])
    days_frame = anomalous_days_from_gt(house_no,appliance,start_date,end_date)
    anom_days = [x.strftime('%Y-%m-%d') for x in days_frame.values.tolist()]
    return anom_days
#%%
def plot_bind_save_all_anomalies(actual_data, anom_list, home, myapp):
    ''' this creates one pdf per day and then combines all pdfs into one pdf '''
    if len(anom_list) < 1:
        return
    for i in range(len(anom_list)): 
        fpdate = str(anom_list[i])
        df = actual_data[fpdate] 
        df.columns = ['submetered']
        ax = df.plot(title = home.split('.')[0] + "-" + myapp + "-" + "true_anomaly", figsize = (12,3))
        fig = ax.get_figure()
        savedir = "/Volumes/MacintoshHD2/Users/haroonr/Detailed_datasets/REFITT/Intermediary_results/anomalies/"
        savedir = savedir + home.split('.')[0] + "/"
        fig.savefig(savedir + myapp + "-" + fpdate + ".pdf", bbox_inches = 'tight')
        plt.close()
    #% now combine pdfs
    file_list = [savedir + i for i in os.listdir(savedir) if i.endswith(".pdf")]
    saveresult = savedir + "combine" + ".pdf"
    myutil.create_pdf_from_pdf_list(file_list, saveresult)
#%%
def get_train_test_dates(store_name):
    store_dic = {}
    dic_values = {}
    store_dic['Dominos-22'] = {'train_duration':{'start':'2018-02-10','end': '2018-02-20'},'test_duration':{'start':'2018-03-01','end':'2018-06-30'}}
    store_dic['Dominos-25'] = {'train_duration':{'start':'2018-02-01','end': '2018-02-07'},'test_duration':{'start':'2018-03-01','end':'2018-06-30'}}
    store_dic['Dominos-07'] = {'train_duration':{'start':'2018-02-15','end': '2018-02-21'},'test_duration':{'start':'2018-03-01','end':'2018-06-30'}}
    store_dic['Dominos-95'] = {'train_duration':{'start':'2018-02-08','end': '2018-02-14'},'test_duration':{'start':'2018-03-01','end':'2018-06-30'}}
    store_dic['Dominos-117']= {'train_duration':{'start':'2018-02-15','end': '2018-02-21'},'test_duration':{'start':'2018-03-01','end':'2018-06-30'}}
    store_dic['Dominos-127']= {'train_duration':{'start':'2018-02-01','end': '2018-02-07'},'test_duration':{'start':'2018-03-01','end':'2018-06-30'}}
    store_dic['Dominos-236']= {'train_duration':{'start':'2018-02-01','end': '2018-02-07'},'test_duration':{'start':'2018-03-01','end':'2018-06-30'}}
    store_dic['Dominos-380']= {'train_duration':{'start':'2018-02-08','end': '2018-02-14'},'test_duration':{'start':'2018-03-01','end':'2018-04-09'}}
    store_dic['Dominos-139']= {'train_duration':{'start':'2018-02-01','end': '2018-02-07'},'test_duration':{'start':'2018-03-01','end':'2018-06-30'}}
    store_dic['Dominos-254']= {'train_duration':{'start':'2018-02-01','end': '2018-02-07'},'test_duration':{'start':'2018-03-01','end':'2018-06-30'}}
    store_dic['Dominos-259']= {'train_duration':{'start':'2018-02-01','end': '2018-02-07'},'test_duration':{'start':'2018-03-01','end':'2018-06-30'}}
    store_dic['Dominos-80']= {'train_duration':{'start':'2018-02-08','end':  '2018-02-14'},'test_duration':{'start':'2018-03-01','end':'2018-05-31'}}   
    store_dic['Dominos-310']= {'train_duration':{'start':'2018-02-16','end': '2018-02-21'},'test_duration':{'start':'2018-03-01','end':'2018-06-30'}}   
    store_dic['Dominos-257']= {'train_duration':{'start':'2018-02-17','end': '2018-02-27'},'test_duration':{'start':'2018-03-01','end':'2018-04-30'}}   

    try:
        dic_values = store_dic[store_name]
    except:
        print('the store is not registered in the database: please update this in the method get_train_test_datas method')
    return dic_values
    