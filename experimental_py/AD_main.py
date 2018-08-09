#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CODE borrowed from REFIT PROJECT
This scritp contains the anomaly detection done on Dominos data 
It contains logic for anomoaly detection and computing detection accuracy. 

Created on Tue Jan  2 08:53:47 2018

@author: haroonr
"""
#%%
import pandas as pd
import sys
sys.path.append('/volumes/MacintoshHD2/Users/haroonr/Dropbox/Zenatix/Dominos/experimental_py/')
import AD_support as ads
#%%
dir = "/Volumes/MacintoshHD2/Users/haroonr/Detailed_datasets/Dominos/"
store = 'Dominos-257'
power = "meter_makeline.csv"
df = pd.read_csv(dir + store + '/' + power,index_col="Datetime")
df.index = pd.to_datetime(df.index)
df_samp = df.resample('1T',label = 'right', closed ='right').mean()
df_sel = df_samp.current
# reading temperature
temperature = "temp_makeline.csv"
df_temp = pd.read_csv(dir + store + '/' + temperature,index_col="Datetime")
df_temp.index = pd.to_datetime(df_temp.index)
df_samp_temp  = df_temp.resample('1T',label = 'right', closed ='right').mean()
#% Resampling data
#print("*****RESAMPLING********")

data_sampling_time = 1 #in minutes
data_sampling_type = "minutes" # or seconds
myapp = "DEFY"
#train_data =  df_sel['2018-02-10' : '2018-02-20'] # home 3 freezer
NoOfContexts, appliance = 2, myapp
#test_data =  df_sel['2018-03-01':'2018-06-30'] 
#test_data =  df_sel['2018-03-04'] 
#test_data =  df_samp['2014-05-01':'2014-05-31'] # home 3
dates = ads.get_train_test_dates(store)
train_data = df_sel[dates['train_duration']['start']:dates['train_duration']['end']]
test_data  = df_sel[dates['test_duration']['start']:dates['test_duration']['end']]

train_results = ads.AD_refit_training(train_data,data_sampling_type,data_sampling_time, NoOfContexts, appliance)
test_results  = ads.AD_refit_testing(test_data,data_sampling_type,data_sampling_time,NoOfContexts, appliance)            
#% Anomaly detection logic
#%
num_std = 2
alpha = 4
res_df = ads.anomaly_detection_algorithm(test_results,train_results,alpha,num_std)
#res_df = test_anomaly_detection_algorithm(test_results,train_results,alpha,num_std)
#%
result_sub = res_df[res_df.status==1]
all_slopes = []
for index, row in result_sub.iterrows():
    #print(row.timestamp.date())
    day = str(row.timestamp.date())
    time_start = day + ' '+ ads.return_context_timeboundary(row.context)[0]
    time_end =   day + ' '+ ads.return_context_timeboundary(row.context)[1]
    temp_data = df_samp_temp[time_start:time_end]
    slope = ads.compute_slope(temp_data)
    all_slopes.append(slope)
result_sub['temp_slope'] = all_slopes
print(result_sub)
res_dir = "/Volumes/MacintoshHD2/Users/haroonr/Dropbox/zenatix/results/"
result_sub['store'] = store
result_sub.to_csv(res_dir+store+'.csv',index=False)
#%% calculating accuracies
gt_file = "/Volumes/MacintoshHD2/Users/haroonr/Dropbox/zenatix/results/ground-truth-dominos.csv"
df_gt = pd.read_csv(gt_file)
all_stores = np.unique(df_gt.store)
result = {}
for i in range(len(all_stores)):
    est = pd.read_csv('/Volumes/MacintoshHD2/Users/haroonr/Dropbox/zenatix/results/'+ all_stores[i] + '.csv')
    gt = df_gt[df_gt.store == all_stores[i]]
    gt_long  = gt[gt.anomtype == 'long-ON-cycle']    
    gt_compres_down = gt[gt.anomtype == 'compressor-down']
    
    est_long = est[est.anomtype == 'long-ON-cycle']
    est_long.drop_duplicates(subset='timestamp',keep='first',inplace=True)
    
    est_compres_down = est[est.anomtype == 'compressor-down']
    est_compres_down.drop_duplicates(subset='timestamp',keep='first',inplace=True)
    
    tp1,fp1,fn1 = ads.compute_tp_fp_fn_Dominos(gt_long,est_long) # long-cycle
    tp2,fp2,fn2 = ads.compute_tp_fp_fn_Dominos(gt_compres_down,est_compres_down) # compressor-down
    actual_long = gt_long.shape[0]
    actual_compres_down = gt_compres_down.shape[0]
    precision = (tp1+tp2)/(tp1+tp2+fp1+fp2)
    recall = (tp1+tp2)/(tp1+tp2+fn1+fn2)
    fscore = round(2*(precision * recall)/(precision+recall),2)
    result[all_stores[i]]  = {'store':all_stores[i], 'actual_long': actual_long,'actual_compressed': actual_compres_down, 'long_detected': tp1, 'compressed_detected': tp2, 'precision': precision, 'recall': recall, 'fscore': fscore  }
pd.DataFrame.from_dict(result).T    
#%%

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
def 
#%% visualise specific data portion
dat = "2014-05-03"
test_data[dat].plot()