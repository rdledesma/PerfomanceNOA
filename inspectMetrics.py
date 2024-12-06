#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 14 14:29:01 2024

@author: dario
"""

import pandas as pd 
import Metrics as m
import matplotlib.pyplot as plt

d = pd.read_csv('process/LQ/10.csv', usecols = ['date','ghi','alpha','sza','argp2'])
n = pd.read_csv('process/LQNSRDB/10.csv', usecols = ['GHI'])
c = pd.read_csv('process/LQ/10.csv', usecols = ['GHI'])

d['ghin'] = c.GHI.values
d['ghic'] = n.GHI.values


d['date'] = pd.to_datetime(d.date)

d = d[d.date.dt.year<=2022]

d = d[d.sza<85]
d['kc'] = d.ghi / d.argp2

d['cc'] = d.kc<0.8 


cc = d.dropna()


plt.plot(cc.date, cc.ghi, label="Measured")
plt.plot(cc.date, cc.ghic, label="CAMS")
plt.plot(cc.date, cc.ghin, label="NSRDB")
plt.legend()

true = cc.ghi.values
pred = cc.ghic.values
m.rrmsd(true, pred)
