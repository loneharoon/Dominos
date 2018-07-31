#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
In this I check How good are AR models for AD.
Created on Wed Jul 25 09:11:44 2018

@author: haroonr
"""
import matplotlib.pyplot as plt

#%%
from sklearn.decomposition import MiniBatchDictionaryLearning
dico = MiniBatchDictionaryLearning(n_components=220, alpha=1, n_iter=100)

train_data = days_obs.loc[datetime.date(2018,2,13):datetime.date(2018,2,28)]
D = dico.fit(train_data).components_

#%%
fig,ax = plt.subplots(ncols = 10, nrows = D.shape[0]/10 )
i = 0
for row in ax:
    for col in row:
        col.plot(D[i])
        i = i +1
    