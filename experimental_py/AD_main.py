#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CODE borrowed from REFIT PROJECT
This scritp contains the AD logic for refit HOMES. 
It contains logic for anomoaly detection and computing detection accuracy. It does not relate to disaggregation
Created on Tue Jan  2 08:53:47 2018

@author: haroonr
"""
#%%
import pandas as pd

import sys
sys.path.append('/volumes/MacintoshHD2/Users/haroonr/Dropbox/Zenatix/Dominos/experimental_py/')
import AD_support as ads
#%%
#dir = "/Volumes/MacintoshHD2/Users/haroonr/Detailed_datasets/REFITT/CLEAN_REFIT_081116/"
#home = "House10.csv"
#df = pd.read_csv(dir+home,index_col="Time")
#df.index = pd.to_datetime(df.index)
#df_sub = df["2014-03":] # since before march their are calibration issues

dir = "/Volumes/MacintoshHD2/Users/haroonr/Detailed_datasets/Dominos/"
store = 'Dominos-22'
power = "meter_makeline.csv"
df = pd.read_csv(dir + store + '/' + power,index_col="Datetime")
df.index = pd.to_datetime(df.index)
df_samp = df.resample('1T',label = 'right', closed ='right').mean()
#df_sel = df_samp.between_time('09:45','23:00')
df_sel = df_samp.current
#%% Resampling data
#print("*****RESAMPLING********")
#df_samp = df_sub.resample('1T',label = 'right', closed ='right').mean()
data_sampling_time = 1 #in minutes
data_sampling_type = "minutes" # or seconds
#scn.rename_appliances(home, df_samp)
#% select particular appliance for anomaly detection
#df_samp.columns
myapp = "DEFY"
train_data =  df_sel['2018-02-10' : '2018-02-20'] # home 3 freezer
NoOfContexts, appliance = 2,myapp
test_data =  df_sel['2018-04-30':'2018-05-30'] 
#test_data =  df_sel['2018-02-26'] 
#test_data =  df_samp['2014-05-01':'2014-05-31'] # home 3
train_results = ads.AD_refit_training(train_data,data_sampling_type,data_sampling_time, NoOfContexts, appliance)
test_results  = ads.AD_refit_testing(test_data,data_sampling_type,data_sampling_time,NoOfContexts, appliance)            
#% Anomaly detection logic
num_std = 2
alpha = 4
res_df = anomaly_detection_algorithm(test_results,train_results,alpha,num_std)
result_sub = res_df[res_df.status==1]
#%%

list(result_sub.anomtype)[0]
 
list(result_sub.timestamp)[0]


day = str(list(result_sub.timestamp)[0].date())
time_start = day + ' '+ return_context_timeboundary(list(result_sub.context)[0])[0]
time_end =   day + ' '+ return_context_timeboundary(list(result_sub.context)[0])[1]
temp_data = df_samp_temp[time_start:time_end]
slope = compute_slope(temp_data)
all_slopes = []
for index, row in result_sub.iterrows():
    day = str(row.timestamp.date())
    time_start = day + ' '+ return_context_timeboundary(row.context)[0]
    time_end =   day + ' '+ return_context_timeboundary(row.context)[1]
    temp_data = df_samp_temp[time_start:time_end]
    slope = compute_slope(temp_data)
    all_slopes.append(slope)
result_sub['temp_slope'] = all_slopes
#%%
# Compute different accuracies
#house_no = 1
house_no =  int(re.findall('\d+',home)[0])
appliance = scn.reverse_lookup(home,myapp) # find actual name of appliance in anomaly database
day_start = test_data.first_valid_index()
day_end = test_data.last_valid_index()
print('both S and NS anomalies selected')
gt,ob = ads.tidy_gt_and_ob(house_no,appliance,day_start,day_end,result_sub)
#confusion_matrix(gt.day.values,ob.day.values)
precision,recall, fscore = ads.compute_AD_confusion_metrics(gt,ob)
print(precision,recall, fscore)  
    
#%%

#%% visualise specific data portion
dat = "2014-05-03"
test_data[dat].plot()