#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 14:06:10 2024

@author: solar
"""

import pandas as pd
import matplotlib.pyplot as plt 
from Geo import Geo
from datetime import timedelta
import time
import numpy as np
start_time = time.time()

SITE = "sa"

dates = pd.date_range(start="2022/01/01 00:00", 
                      end="2023/12/31 23:59", freq="15min")
    
d = pd.read_csv('cams/SA/sa.csv', sep=";",
                header=42, usecols=['TOA', 'Clear sky GHI','GHI'])

d['date'] = dates


d['TOA'] = d.TOA * 4
d['Clear sky GHI'] = d['Clear sky GHI'] * 4
d['ghi'] = d['GHI'] * 4



g = Geo(d.date + timedelta(minutes=7.5), 
            lat=-24.7288, 
            long=-65.4095, 
            gmt =0, 
            alt = 1233, 
            beta=0).df

d['sza'] = g.SZA.values



d = d[['date','sza','ghi']]

for i in [1,5,10,15,30,60]:
    s = d.resample(
                        f'{i} min', 
                        on='date', 
                        ).mean().reset_index()
    
    
    sg = Geo(range_dates= s.date + timedelta(minutes= i/2), 
                lat=-24.7288, 
                long=-65.4095, 
                gmt =0, 
                alt = 1233, 
                beta=0).df
    
    s['sza'] = sg.SZA.values
    s['ghi'] = (s.ghi / sg.TOA).interpolate() * sg.TOA
    s['ghi'] = np.where(s.sza<83, s.ghi, np.nan)
    
    
    if i == 5:
        t = s
    s.to_csv(f'cams/SA/sa_{i}.csv', index=False)








