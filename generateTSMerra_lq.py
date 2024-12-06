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


d = pd.read_csv('MERRA-2/lq.csv', usecols=['date','swfdn'])
d['date'] = pd.to_datetime(d.date)



d = d[d.date.dt.year<=2021]
d = d.sort_values(by=['date'], ascending=True)

d.columns = ['date','ghi']

dates = pd.date_range(
    start="2020/01/01 00:00", 
    end="2021/12/31 23:59", freq="60 min")


g = Geo(dates + timedelta(minutes=30), 
            -22.103936, 
            -65.599923, 
            gmt =0, 
            alt = 3500, 
            beta=0).df



plt.plot(d.ghi.values)
plt.plot(g.GHIargp2.values)



g['ghi'] = d.ghi.values
g['sza'] = g.SZA
g = g[['date','ghi','sza']]

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
    s['kt'] = s.ghi / sg.TOA
    s['ghi'] = s.kt.interpolate() * sg.TOA
    s['ghi'] = np.where(s.sza<83, s.ghi, np.nan)
    
    if i == 5:
        t = s
    s.to_csv(f'MERRA-2/LQ/lq_{i}.csv', index=False)

