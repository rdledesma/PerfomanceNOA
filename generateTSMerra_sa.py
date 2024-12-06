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


d = pd.read_csv('MERRA-2/sa.csv', usecols=['date','swfdn'])
d['date'] = pd.to_datetime(d.date)



d = d[d.date.dt.year.isin([2022,2023])]
d = d.sort_values(by=['date'], ascending=True)

d.columns = ['date','ghi']

dates = pd.date_range(
    start="2022/01/01 00:00", 
    end="2023/12/31 23:59", freq="60 min")


g = Geo(dates + timedelta(minutes=30), 
            lat=-24.7288, 
            long=-65.4095, 
            gmt=0, 
            beta=0,
            alt=1233).df


plt.figure()
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
    
    
    sg = Geo(range_dates= s.date + timedelta(minutes= i/2), 
                lat=-24.7288, 
                long=-65.4095, 
                gmt=0, 
                beta=0,
                alt=1233).df
    
    s['sza'] = sg.SZA.values
    s['kt'] = s.ghi / sg.TOA
    s['kt'] = np.where(s.sza<83,s.kt, 0)
    s['ghi'] = s.kt.interpolate() * sg.TOA
    
    s['ghi'] = np.where(s.sza<83, s.ghi, np.nan)
    
    
    plt.figure()
    plt.plot(s.date, s.ghi)
    
    
    
    if i == 5:
        t = s
    s.to_csv(f'MERRA-2/SA/sa_{i}.csv', index=False)

