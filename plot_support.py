#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This contains supporting functions for plotting data
Created on Mon Jun 11 16:12:36 2018

@author: haroonr
"""

import seaborn as sns
sns.set(style="ticks",color_codes=True)
import matplotlib.pyplot as plt

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