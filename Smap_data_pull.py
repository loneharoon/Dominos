#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This code is used to download data from Smap and most of it is taken from Jitesh.
Created on Thu Jun  7 15:45:34 2018

@author: haroonr
"""
import os
import smap_support as ss
import pandas as pd
KEY = "jmAcs0ah172L8DQXJlkIeuKE8ppTetrBTczq"
#%%
conn1 = ss.connect_archiver('dominos.zenatix.com','9105')
start_time =   "02/01/2018" #monthd/day/year
end_time =     "06/30/2018 23:59:59"
save_path = "/Volumes/MacintoshHD2/Users/haroonr/Detailed_datasets/Dominos/"
#stores =  ['Dominos-'+ str(i) for i in range(60,66)]
stores = ['Dominos-257', 'Dominos-22','Dominos-186','Dominos-19', 'Dominos-80', 'Dominos-27', 'Dominos-43', 'Dominos-79', 'Dominos-198', 'Dominos-25', 'Dominos-259', 'Dominos-397', 'Dominos-06', 'Dominos-402', 'Dominos-41', 'Dominos-232', 'Dominos-380', 'Dominos-290', 'Dominos-396', 'Dominos-384', 'Dominos-286', 'Dominos-58', 'Dominos-94', 'Dominos-187', 'Dominos-407', 'Dominos-05', 'Dominos-298', 'Dominos-387', 'Dominos-254', 'Dominos-206', 'Dominos-127', 'Dominos-238', 'Dominos-339', 'Dominos-95', 'Dominos-328', 'Dominos-236', 'Dominos-310', 'Dominos-139', 'Dominos-121', 'Dominos-117']
#problematic ones 187,407

sel_stores = ['Dominos-22', 'Dominos-25', 'Dominos-43', 'Dominos-79', 'Dominos-198', 'Dominos-257', 'Dominos-206', 'Dominos-380', 'Dominos-121', 'Dominos-117', 'Dominos-127', 'Dominos-95', 'Dominos-236', 'Dominos-310', 'Dominos-187']
#%% fetch power
for i in range(0,16):
    store = sel_stores[i]
    #store = "Dominos-19"
    
    query = ss.makeline_temp_query(start_time, end_time, store)
    data, col_names = ss.temp_data(conn1, query, KEY)
    temp_df = ss.ems_datafram(data, col_names)
    temp_df.columns = ['temperature']
    if not os.path.isdir(save_path + store):
        os.makedirs(save_path + store)
    temp_df.to_csv(save_path + store + "/temp_"  + "makeline.csv" )
 
    query = ss.makeline_power_query(start_time,end_time,store)
    data, col_names = ss.temp_data(conn1, query, KEY)
    power_df = ss.ems_datafram(data, col_names)
    power_df.columns = ['power']
    
    query = ss.makeline_current_query(start_time,end_time,store)
    data, col_names = ss.temp_data(conn1, query, KEY)
    current_df = ss.ems_datafram(data, col_names)
    current_df.columns = ['current']
    
    query = ss.makeline_power_factor_query(start_time,end_time,store)
    data, col_names = ss.temp_data(conn1, query, KEY)
    power_factor_df = ss.ems_datafram(data, col_names)
    power_factor_df.columns = ['power_factor']
    

    query = ss.makeline_remote_control_query(start_time,end_time,store)
    data, col_names = ss.temp_data(conn1, query, KEY)
    control_df = ss.ems_datafram(data, col_names)
    control_df.columns = ['control']
    control_df.to_csv(save_path + store + "/control_"  + "makeline.csv" )
    
    if not os.path.isdir(save_path + store):
        os.makedirs(save_path + store)
    comb_df = pd.concat([power_df,current_df,power_factor_df],axis = 1)
    comb_df.to_csv(save_path + store + "/meter_"  + "makeline.csv" )
    print ('{} done'.format(store))
    
#%%
    
    
#%%

#et = datetime.datetime.now().replace(hour=0,minute =0,second =0)
#st = et - datetime.timedelta(hours = 24*10)
##et =   "2018-06-07"
##st =   "2018-04-01"
#SMAP_FORMAT = "%m/%d/%Y %H:%M:%S"
#start_time = st.strftime(SMAP_FORMAT)
#end_time = et.strftime(SMAP_FORMAT)