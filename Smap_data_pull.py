#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This code is used to download data from Smap and most of it is taken from Jitesh.
Created on Thu Jun  7 15:45:34 2018

@author: haroonr
"""
import pandas as pd
import datetime
import httplib
from smap.archiver import client
KEY = "jmAcs0ah172L8DQXJlkIeuKE8ppTetrBTczq"

#%%
def connect_archiver(address, port):
    address = address
    port = port
    conn = httplib.HTTPConnection(address, port)
    return conn

#get the response and parse the json returned
def fetch_data(conn, key,query):
    api_call = "/api/query/?key=" + key
    conn.request("POST",api_call, query)
    response = conn.getresponse()
    global sda
    sda = response
    res = client.parser(response.read())
    return res


def temp_data(connection,query, key):
    a,b = [],[]
    data = fetch_data(connection, key, query)
    for each in range(len(data)):
        if len(data[each]['Readings']) > 1:
            tmp = pd.DataFrame(data[each]['Readings'])
            tmp[0] = pd.to_datetime(tmp[0],unit='ms')
            a.append(tmp.set_index(0))#.resample('30s').first()
            b.append(data[each]['Metadata']['Instrument']['LoadType'])
    return a,b

def ems_datafram(a, b):
    df = pd.concat(a,axis=1)
    df.columns = b # pd.MultiIndex.from_tuples(zip(b,c))    #setting index name of df
    df.index.name = 'Datetime'
    df.index = df.index + datetime.timedelta(hours=5,minutes=30)
    return df
#%%
conn1 = connect_archiver('dominos.zenatix.com','9105')
#et = datetime.datetime.now().replace(hour=0,minute =0,second =0)
#st = et - datetime.timedelta(hours = 24*10)
#
##et =   "2018-06-07"
##st =   "2018-04-01"
##
#SMAP_FORMAT = "%m/%d/%Y %H:%M:%S"
##
#start_time = st.strftime(SMAP_FORMAT)
#end_time = et.strftime(SMAP_FORMAT)

start_time =   "01/01/2017" #monthd/day/year
end_time =     "05/31/2018"

#%%
def makeline_temp_query(start_time,end_time,campus):
    query = "apply  to data in ('" + start_time + "','" + end_time +     "') limit -1 where Metadata/ControllerLocation/Campus = '" + campus + "' and      Metadata/Extra/PhysicalParameter = 'Temperature' and Metadata/Instrument/LoadType  = 'Makeline' "
    return query

query = makeline_temp_query(start_time, end_time, 'Dominos-04')

data, col_names = temp_data(conn1, query, KEY)
temp_df = ems_datafram(data, col_names)
temp_df.columns = ['temperature']
save_path = "/Volumes/MacintoshHD2/Users/haroonr/Detailed_datasets/Dominos/"
temp_df.to_csv(save_path + campus + "/temp_"  + "makeline.csv" )
#%%
def makeline_power_query(start_time,end_time,campus):
    query = "apply  to data in ('" + start_time + "','" + end_time +     "') limit -1 where Metadata/ControllerLocation/Campus = '" + campus + "' and      Metadata/Extra/PhysicalParameter = 'Power' and Metadata/Extra/R_PHASE  = 'Makeline' "
    return query

query = makeline_power_query(start_time,end_time,'Dominos-04')
data, col_names = temp_data(conn1, query, KEY)
power_df = ems_datafram(data, col_names)
power_df.columns = ['power']
power_df.to_csv(save_path + campus + "/power_"  + "makeline.csv" )
#%%
