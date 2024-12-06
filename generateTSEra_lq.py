#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 30 18:38:25 2024

@author: dario
"""

import pandas as pd
import matplotlib.pyplot as plt
from Geo import Geo
import numpy as np
from datetime import timedelta



d = pd.read_csv('era5/LQ/LQ.csv')
d['date'] = pd.to_datetime(d.date)

d = d[d.date.dt.year.isin([2020,2021])]

dates = pd.date_range(
    start="2020/01/01 00:00", end="2021/12/31 23:59",
    freq="1h")



g = Geo(range_dates= dates + timedelta(minutes=30), 
            lat=-22.1038, 
            long=-65.60125, 
            gmt =0, 
            alt = 3500, 
            beta=0).df



plt.plot(g.GHIargp2.values)
plt.plot(d.ghi.shift(-1).values)




g['sza'] = g.SZA.values
g['ghi'] = d.ghi.shift(-1).values

plt.plot(g.date, g.ghi)


for i in [1,5,10,15,30,60]:
    s = g.resample(
                        f'{i} min', 
                        on='date', 
                        ).mean().reset_index()
    
    
    sg = Geo(range_dates= s.date + timedelta(minutes= int(i/2)), 
                lat=-22.1038, 
                long=-65.60125, 
                gmt =0, 
                alt = 3500, 
                beta=0).df
    
    s['sza'] = sg.SZA.values
    s['ghi'] = (s.ghi / sg.TOA).interpolate() * sg.TOA
    s['ghi'] = np.where(s.sza<83, s.ghi, np.nan)
    
    if i == 5:
        t = s
    s.to_csv(f'era5/LQ/lq_{i}.csv', index=False)




