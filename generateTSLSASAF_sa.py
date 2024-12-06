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

d1 = pd.read_csv('LSA-SAF/SA/lsa-sa_2022.csv')
d2 = pd.read_csv('LSA-SAF/SA/lsa-sa_2023.csv')
d = pd.concat([d1,d2])


d['date'] = pd.to_datetime(d.date)


d = d[['date','ghi']]
d.columns = ['date','GHI']

plt.figure()
plt.plot(d.date, d.GHI)



g = Geo(d.date  + timedelta(minutes=7.5), 
            -24.7288, 
            -65.4095, 
            gmt =0, 
            alt = 1233, 
            beta=0).df




g['ghi'] = d.GHI.values
g['ghi'] = np.where(g.SZA<83, g.ghi, np.nan)
g['ghi'] = np.where(g.ghi>0, g.ghi, np.nan)



g['kt'] = g.ghi / g.TOA 
g['kt'] = np.where(g.TOA<=0, 0 , g.kt)
g['kt'] = g.kt.interpolate(limit=4)
g['ghi'] = g.kt * g.TOA


plt.figure()
plt.plot(g.date, g.ghi)
plt.plot(g.date, g.GHIargp2)

g['sza'] = g.SZA.values

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
    s['ghi'] = s.ghi.interpolate()
    s['ghi'] = np.where(s.sza<83, s.ghi, np.nan)
    
    if i == 5:
        t = s
    
    
    s.to_csv(f'LSA-SAF/SA/sa_{i}.csv', index=False)









# plt.plot(d.date, d.GHI) 
# plt.plot(g.date, g.GHIargp2)

# for i in [1,5,10,15,30,60]:
#     s = d.resample(
#                         f'{i} min', 
#                         on='date', 
#                         ).mean().reset_index()
#     s.to_csv(f'nsrdb/LQ/lq_{i}.csv', index=False)





