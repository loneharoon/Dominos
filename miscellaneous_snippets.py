#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This contains different snippts for doing multiple things
Created on Fri Jun 15 07:46:20 2018

@author: haroonr
"""
import pandas as pd
#%% to read selected data sites names
df = pd.read_csv("/Volumes/MacintoshHD2/Users/haroonr/Detailed_datasets/Dominos/sites_to_select.csv")
df.columns = ['store','city','region']
print list(df.store)

['Dominos-257', 'Dominos-22', 'Dominos-186', 'Dominos-19', 'Dominos-80', 'Dominos-27', 'Dominos-43', 'Dominos-79', 'Dominos-198', 'Dominos-25', 'Dominos-259', 'Dominos-397', 'Dominos-06', 'Dominos-402', 'Dominos-41', 'Dominos-232', 'Dominos-380', 'Dominos-290', 'Dominos-396', 'Dominos-384', 'Dominos-286', 'Dominos-58', 'Dominos-94', 'Dominos-187', 'Dominos-407', 'Dominos-05', 'Dominos-298', 'Dominos-387', 'Dominos-254', 'Dominos-206', 'Dominos-127', 'Dominos-238', 'Dominos-339', 'Dominos-95', 'Dominos-328', 'Dominos-236', 'Dominos-310', 'Dominos-139', 'Dominos-121', 'Dominos-117']
#%%