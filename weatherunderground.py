#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 21:22:23 2018
I use this script to download data from weather underground API

@author: haroonr
"""

#%%
'''
VIDP: DELhi international airport
VABB: Chattarpatri shivaji international mumbai
VOMM: Chennai international
VOHY: Hyderabad
VOBG: HAl bangalore

'''
import csv
import datetime
from datetime import date
from time import sleep
import requests # this library makes html requests much simpler
key = "aca4914ccfcb186d" # put your key here3
api_key = key
station_id ='VIDP' # VIDP is international airport while as VIDD is safdarjung airport
start_date = datetime.date(2017,12,1)
end_date = datetime.date(2018,5,31)
savefilename = "/Volumes/MacintoshHD2/Users/haroonr/Detailed_datasets/Dominos/weather_data/" + station_id + '.csv'
download_weather_data(station_id,start_date,end_date,savefilename)

#%%
def download_weather_data(station_id,start_date,end_date,savefilename):
  
  with open(savefilename, 'wb') as outfile:
    writer = csv.writer(outfile)
    # defines all weather acronyms
    #https://serbian.wunderground.com/weather/api/d/docs?d=resources/phrase-glossary
    headers = ['date','temperature','humidity','wind speed','wind direction'] # edit these as required
    writer.writerow(headers)
    datex = start_date
    while datex <= end_date:
      date_string = datex.strftime('%Y%m%d')
      url = ("http://api.wunderground.com/api/{}/history_{}/q/{}.json".format(api_key,date_string,station_id))
      data = requests.get(url).json()
      for history in data['history']['observations']:
        row = []
        row.append(str(history['date']['pretty']))
        row.append(str(history['tempm']))	
        row.append(str(history['hum']))
        row.append(str(history['wspdm']))
        row.append(str(history['wdird']))
        writer.writerow(row)
      sleep(30) # in seconds, limit is 10 calls per minute
      datex += datetime.timedelta(days=1) 				 

#%% download data of pending dates [next two cells deal with that only]
key="aca4914ccfcb186d" # put your key here3
api_key = key
station_id ='VIDP'     
pending_dates = [datetime.date(2016,4,1),datetime.date(2016,5,11),datetime.date(2016,5,18),
                 datetime.date(2016,5,28),datetime.date(2016,6,15),datetime.date(2016,8,1),
                datetime.date(2016,11,23)]
headers = ['date','temperature','humidity','wind speed','wind direction'] # edit these as required
 
day = []
for datex in pending_dates:
  date_string = datex.strftime('%Y%m%d')
  try:
    url = ("http://api.wunderground.com/api/{}/history_{}/q/{}.json".format(api_key,date_string,station_id))
    data = requests.get(url).json()
    for history in data['history']['observations']:
      row = []
      row.append(str(history['date']['pretty']))
      row.append(str(history['tempm'])) 
      row.append(str(history['hum']))
      row.append(str(history['wspdm']))
      row.append(str(history['wdird']))
      day.append(row)
  except:
      print('no data for day {}'.format(datex))
  sleep(30) 
#%%
filename = "year2016_VIDP_station.csv"
dframe = pd.DataFrame.from_records(day)
dframe.columns = headers
dframe.index = dframe.date
dframe.index = pd.to_datetime(dframe.index)
dframe.drop('date',axis=1,inplace=True)
save_path = "/Volumes/MacintoshHD2/Users/haroonr/Detailed_datasets/IIIT_dataset/weather/missing_days/"
dframe.to_csv(save_path+filename)
#%% few of pending days
pending_dates = [datetime.date(2017,2,15),datetime.date(2017,3,9),datetime.date(2017,4,15),
                 datetime.date(2017,5,8),datetime.date(2017,5,19),datetime.date(2017,7,19),
                datetime.date(2017,9,12),datetime.date(2017,10,5),datetime.date(2017,10,7),
                 datetime.date(2017,10,10),datetime.date(2017,11,21),datetime.date(2017,11,23),
                 datetime.date(2017,11,30)]
 
pending_dates = [datetime.date(2016,4,1),datetime.date(2016,5,11),datetime.date(2016,5,18),
                 datetime.date(2016,5,28),datetime.date(2016,6,15),datetime.date(2016,8,1),
                datetime.date(2016,11,23)]

