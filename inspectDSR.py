#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 15:40:04 2024

@author: dario
"""
import matplotlib.pyplot as plt
import pandas as pd
site='sa'
freq=60
d = pd.read_csv(f'measured/SA/{site}_{freq}.csv')
ds = pd.read_csv(f'DSR/SA/{site}_{freq}_linear.csv')

d['date'] = pd.to_datetime(d.date)

ds['date'] = pd.to_datetime(ds.date)


ds = ds[ds.sza<83]


plt.plot(d.date,d.ghi)
plt.plot(ds.date, ds.ghi)


dsi = (ds.set_index('date')
      .reindex(d.date)
      .rename_axis(['date'])
      #.fillna(0)
      .reset_index())



plt.plot(d.date,d.ghi)
plt.plot(dsi.date, dsi.ghi)


