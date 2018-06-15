#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
I use this scipt to get seaborn facet plots of daywise power and temperature data
Created on Fri Jun  8 08:59:52 2018

@author: haroonr
"""

import pandas as pd
import plot_support as ps
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
plt.ioff()
stores = ['Dominos-257', 'Dominos-22', 'Dominos-186', 'Dominos-19', 'Dominos-80', 'Dominos-27', 'Dominos-43', 'Dominos-79', 'Dominos-198', 'Dominos-25', 'Dominos-259', 'Dominos-397', 'Dominos-06', 'Dominos-402', 'Dominos-41', 'Dominos-232', 'Dominos-380', 'Dominos-290', 'Dominos-396', 'Dominos-384', 'Dominos-286', 'Dominos-58', 'Dominos-94', 'Dominos-187', 'Dominos-407', 'Dominos-05', 'Dominos-298', 'Dominos-387', 'Dominos-254', 'Dominos-206', 'Dominos-127', 'Dominos-238', 'Dominos-339', 'Dominos-95', 'Dominos-328', 'Dominos-236', 'Dominos-310', 'Dominos-139', 'Dominos-121', 'Dominos-117']
#%%
dir = "/Volumes/MacintoshHD2/Users/haroonr/Detailed_datasets/Dominos/"
plots_dir = "/Volumes/MacintoshHD2/Users/haroonr/Detailed_datasets/Dominos/makeline_plots/"
for i in range(5,11):
    store = stores[i]
    #store = "Dominos-22"
    power = "power_makeline.csv"
    pdf = pd.read_csv(dir + store + '/' + power,index_col="Datetime")
    pdf.index = pd.to_datetime(pdf.index)
    pdf_samp = pdf.resample('5T',label = 'right', closed ='right').mean()
    
    temp = "temp_makeline.csv"
    tdf = pd.read_csv(dir + store + '/' + temp,index_col="Datetime")
    tdf.index = pd.to_datetime(tdf.index)
    tdf_samp = tdf.resample('5T',label = 'right', closed ='right').mean()
    #% select only data chunk
    #pdf_sub = pdf_samp["2017-12-01":"2018-06-06"]
    #tdf_sub = tdf_samp["2017-12-01":"2018-06-06"]
    pdf_sub = pdf_samp
    tdf_sub = tdf_samp
    df = pd.concat([pdf_sub,tdf_sub],axis=1)
    df['day']  = df.index.date
    df['timestamp'] = df.index.time
    #% perform grouping
    df_gp = df.groupby([df.index.year,df.index.month])
    #%
    with PdfPages(plots_dir +  str.split(store,'-')[1] + '_power.pdf') as pdf:
      for i,group in df_gp:
        print(i)
        pdf.savefig(ps.plot_facet_plots_power(group))
    #%
    with PdfPages(plots_dir +  str.split(store,'-')[1] + '_temperature.pdf') as pdf:
      for i,group in df_gp:
        print(i)
        pdf.savefig(ps.plot_facet_plots_temperature(group))
    print ('{} done'.format(store))
#%%
 # use this module to read data from hdf file format
data_path = "/Volumes/MacintoshHD2/Usfers/haroonr/Detailed_datasets/Dominos/"
ds = pd.io.pytables.HDFStore(data_path + 'dominos_dummy.h5')


ps = pd.io.pytables.HDFStore(data_path + 'dominos_dummy_5stores.h5')

