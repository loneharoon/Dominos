#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This code is used to download data from Smap and most of it is taken from Jitesh.
Created on Thu Jun  7 15:45:34 2018

@author: haroonr
"""
import os
import smap_support as ss
KEY = "jmAcs0ah172L8DQXJlkIeuKE8ppTetrBTczq"
#%%
conn1 = ss.connect_archiver('dominos.zenatix.com','9105')
start_time =   "01/01/2017" #monthd/day/year
end_time =     "05/31/2018"
save_path = "/Volumes/MacintoshHD2/Users/haroonr/Detailed_datasets/Dominos/"
store = 'Dominos-01'
#%% fetch power
query = ss.makeline_temp_query(start_time, end_time, store)
data, col_names = ss.temp_data(conn1, query, KEY)
temp_df = ss.ems_datafram(data, col_names)
temp_df.columns = ['temperature']
if not os.path.isdir(save_path + store):
    os.makedirs(save_path + store)
temp_df.to_csv(save_path + store + "/temp_"  + "makeline.csv" )
#%% fetech temperature
query = ss.makeline_power_query(start_time,end_time,store)
data, col_names = ss.temp_data(conn1, query, KEY)
power_df = ss.ems_datafram(data, col_names)
power_df.columns = ['power']
power_df.to_csv(save_path + store + "/power_"  + "makeline.csv" )
#%%

#et = datetime.datetime.now().replace(hour=0,minute =0,second =0)
#st = et - datetime.timedelta(hours = 24*10)
##et =   "2018-06-07"
##st =   "2018-04-01"
#SMAP_FORMAT = "%m/%d/%Y %H:%M:%S"
#start_time = st.strftime(SMAP_FORMAT)
#end_time = et.strftime(SMAP_FORMAT)