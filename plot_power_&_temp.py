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
#%%
dir = "/Volumes/MacintoshHD2/Users/haroonr/Detailed_datasets/Dominos/"
plots_dir = "/Volumes/MacintoshHD2/Users/haroonr/Detailed_datasets/Dominos/makeline_plots/"
store = "Dominos-01"
power = "power_makeline.csv"
pdf = pd.read_csv(dir + store + '/' + power,index_col="Datetime")
pdf.index = pd.to_datetime(pdf.index)
pdf_samp = pdf.resample('5T',label = 'right', closed ='right').mean()

temp = "temp_makeline.csv"
tdf = pd.read_csv(dir + store + '/' + temp,index_col="Datetime")
tdf.index = pd.to_datetime(tdf.index)
tdf_samp = tdf.resample('5T',label = 'right', closed ='right').mean()
#% select only data chunk
pdf_sub = pdf_samp["2017-12-01":"2018-06-06"]
tdf_sub = tdf_samp["2017-12-01":"2018-06-06"]
df = pd.concat([pdf_sub,tdf_sub],axis=1)
df['day']  = df.index.date
df['timestamp'] = df.index.time
#% perform grouping
df_gp = df.groupby([df.index.year,df.index.month])
#%%
with PdfPages(plots_dir + store + '_power.pdf') as pdf:
  for i,group in df_gp:
    print(i)
    pdf.savefig(ps.plot_facet_plots_power(group))
#%%
with PdfPages(plots_dir + store + '_temperature.pdf') as pdf:
  for i,group in df_gp:
    print(i)
    pdf.savefig(ps.plot_facet_plots_temperature(group))
#%%
 # use this module to read data from hdf file format
data_path = "/Volumes/MacintoshHD2/Usfers/haroonr/Detailed_datasets/Dominos/"
ds = pd.io.pytables.HDFStore(data_path + 'dominos_dummy.h5')


ps = pd.io.pytables.HDFStore(data_path + 'dominos_dummy_5stores.h5')

