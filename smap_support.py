#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This contains supporting functions for feteching data
Created on Fri Jun  8 15:29:51 2018

@author: haroonr
"""
import pandas as pd
import datetime
import httplib
from smap.archiver import client
import os
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

def makeline_temp_query(start_time,end_time,campus):
    query = "apply  to data in ('" + start_time + "','" + end_time +     "') limit -1 where Metadata/ControllerLocation/Campus = '" + campus + "' and      Metadata/Extra/PhysicalParameter = 'Temperature' and Metadata/Instrument/LoadType  = 'Makeline' "
    return query

def makeline_power_query(start_time,end_time,campus):
    query = "apply  to data in ('" + start_time + "','" + end_time +     "') limit -1 where Metadata/ControllerLocation/Campus = '" + campus + "' and      Metadata/Extra/PhysicalParameter = 'Power' and Metadata/Extra/R_PHASE  = 'Makeline' "
    return query
