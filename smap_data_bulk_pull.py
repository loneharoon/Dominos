#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
I use this script to download smap data at bulk and then store data in a HDF5 file
Created on Sat Jun  9 15:12:44 2018

@author: haroonr
"""

import pandas as pd
import smap_support as ss
KEY = "jmAcs0ah172L8DQXJlkIeuKE8ppTetrBTczq"
#%%
conn1 = ss.connect_archiver('dominos.zenatix.com','9105')
start_time =   "01/01/2017" #monthd/day/year
end_time =     "05/31/2018"
save_path = "/Volumes/MacintoshHD2/Users/haroonr/Detailed_datasets/Dominos/"
miss_store = []
#stores =  ['Dominos-'+ str(i) for i in range(10,617)]
stores =  ['Dominos-'+ str(i) for i in range(60,66)]
#%% create hdf file for the first time
hstore = pd.HDFStore(save_path +'dominos_dataset_5stores.h5')
#%% fetch power for hdf
for store in stores:
    try:
        conn1 = ss.connect_archiver('dominos.zenatix.com','9105')
        query = ss.makeline_temp_query(start_time, end_time, store)
        data, col_names = ss.temp_data(conn1, query, KEY)
        temp_df = ss.ems_datafram(data, col_names)
        temp_df.columns = ['temperature']
        hstore.put('/' + store+'/makeline_temperature',temp_df)
        
        query = ss.makeline_power_query(start_time,end_time,store)
        conn1 = ss.connect_archiver('dominos.zenatix.com','9105')
        data, col_names = ss.temp_data(conn1, query, KEY)
        power_df = ss.ems_datafram(data, col_names)
        power_df.columns = ['power']
        hstore.put('/' + store+'/makeline_power',power_df)  
        print('Store done {}'.format(store))
    except:
        miss_store.append(store)
        print('Missing store {}'.format(store))
hstore.close()   
#%% fetech temperature
power_df.to_csv(save_path + store + "/power_"  + "makeline.csv" )
ll = pd.io.pytables.HDFStore(save_path + 'dominos_dummy.h5')