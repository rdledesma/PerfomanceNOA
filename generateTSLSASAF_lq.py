#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 09:52:31 2024

@author: dario
"""


import pandas as pd
import matplotlib.pyplot as plt
from Geo import Geo
import numpy as np
from datetime import timedelta

d1 = pd.read_csv('LSA-SAF/LQ/lsasaf-LQ_2020.csv')
d2 = pd.read_csv('LSA-SAF/LQ/lsasaf-LQ_2021.csv')
d = pd.concat([d1,d2])

del d1,d2

d['date'] = pd.to_datetime(d.date)

d = d[['date','ghi']]
d.columns = ['date','GHI']




g = Geo(range_dates= d.date + timedelta(minutes=7.5), 
            lat=-22.1038, 
            long=-65.60125, 
            gmt =0, 
            alt = 3500, 
            beta=0).df


g['ghi'] = d.GHI.values
g['ghi'] = np.where(g.SZA<83, g.ghi, np.nan)
g['ghi'] = np.where(g.ghi>0, g.ghi, np.nan)



g['kt'] = g.ghi / g.TOA 
g['kt'] = np.where(g.TOA<=0, 0 , g.kt)
g['kt'] = g.kt.interpolate(limit=4)
g['ghi'] = g.kt * g.TOA



plt.plot(g.date, g.ghi)
plt.plot(g.date, g.GHIargp2)

g['sza'] = g.SZA.values

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
    s['ghi'] = s.ghi.interpolate()
    s['ghi'] = np.where(s.sza<83, s.ghi, np.nan)
    
    if i == 5:
        t = s
    
    
    s.to_csv(f'LSA-SAF/LQ/lq_{i}.csv', index=False)




