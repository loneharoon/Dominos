#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
I use this scipt to get seaborn facet plots of daywise power and temperature data
Created on Fri Jun  8 08:59:52 2018

@author: haroonr
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="ticks",color_codes=True)
from matplotlib.backends.backend_pdf import PdfPages
plt.ioff()
#%%
dir = "/Volumes/MacintoshHD2/Users/haroonr/Detailed_datasets/Dominos/Dominos-04/"
power = "power_makeline.csv"
pdf = pd.read_csv(dir + power,index_col="Datetime")
pdf.index = pd.to_datetime(pdf.index)
pdf_samp = pdf.resample('5T',label = 'right', closed ='right').mean()

temp = "temp_makeline.csv"
tdf = pd.read_csv(dir + temp,index_col="Datetime")
tdf.index = pd.to_datetime(tdf.index)
tdf_samp = tdf.resample('5T',label = 'right', closed ='right').mean()
#%% select only data chunk

pdf_sub = pdf_samp["2017-12-01":"2018-06-06"]
tdf_sub = tdf_samp["2017-12-01":"2018-06-06"]
df = pd.concat([pdf_sub,tdf_sub],axis=1)
df['day']  = df.index.date
df['timestamp'] = df.index.time
#%% perform grouping
df_gp = df.groupby([df.index.year,df.index.month])
#%%
with PdfPages(dir + 'makeline_power.pdf') as pdf:
  for i,group in df_gp:
    print(i)
    pdf.savefig(plot_facet_plots_power(group))
#%%
with PdfPages(dir + 'makeline_temperature.pdf') as pdf:
  for i,group in df_gp:
    print(i)
    pdf.savefig(plot_facet_plots_temperature(group))
#%%
def plot_facet_plots_power(df):
    h =  sns.FacetGrid(df,col='day', col_wrap = 7,size = 2.5,sharex=True,sharey=True,dropna=False)
    h = h.set_xticklabels(rotation = 15)
    h = (h.map_dataframe(plt.plot,'timestamp','power')
        .set_axis_labels('','power')
        .fig.subplots_adjust(wspace=.2,hspace=.5)
        )
    return h
def plot_facet_plots_temperature(df):
    h =  sns.FacetGrid(df,col='day', col_wrap = 7,size = 2.5,sharex=True,sharey=True,dropna=False)
    h = h.set_xticklabels(rotation = 15)
    h = (h.map_dataframe(plt.plot,'timestamp','temperature')
        .set_axis_labels('','temperature')
        .fig.subplots_adjust(wspace=.2,hspace=.5)
        )
    return h
#%%

