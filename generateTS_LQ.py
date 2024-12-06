#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 12:45:48 2024

@author: solar
"""

import pandas as pd
import matplotlib.pyplot as plt
import Geo

d = pd.read_csv('measured/sa/lq.csv')

d['date'] = pd.to_datetime(d.date)
plt.plot(d.date, d.ghi)

g = Geo.Geo(d.date, 
            -22.103936, 
            -65.599923, 
            gmt =0, 
            alt = 3500, 
            beta=0).df



d['sza'] = g.SZA.values
d['msk'] = d.sza<90

d['argp'] = g.GHIargp
d['kt'] = d.ghi / g.TOA


plt.plot(d.date, d.argp)

plt.plot(d.date, d.ghi)


for m in d.date.dt.month.unique():
    s = d[d.msk]
    s = s[s.date.dt.month == m]
    plt.figure()
    plt.plot(s.sza, s.ghi, '.', markersize=0.1)


s = d[d.msk]
s = s[s.date.dt.month >= 9]



show = s[s.date.dt.year == 2023]
show['n'] = show.date.dt.day_of_year


dia = show[show.n <= 289]

diab = show[show.n > 289]


plt.plot(dia.sza, dia.ghi, '.', markersize=0.5)
plt.plot(diab.sza, diab.ghi, '.', markersize=0.5)




plt.plot(dia.date, dia.argp, '-', markersize=0.5)



"problema inicia en  244 y finaliza en 290 año 2023"




g['ghi'] = d.ghi


import NollasQC
import numpy as np
NollasQC.QC(g)


g['ghi'] = np.where(g.Acepted, g.ghi, np.nan)

g['ghi'] = np.where( (g.date.dt.year == 2023) & (g.date.dt.day_of_year >= 230) 
                    & (g.date.dt.day_of_year <= 290),
                    np.nan, g.ghi )



plt.plot(g.SZA, g.ghi, '.', markersize=0.2)




plt.plot(g.date, g.ghi)
plt.plot(g.date, g.GHIargp)



for i in [1,5,10,15,30,60]:
    d = g[['date','ghi']].resample(
                        f'{i} min', 
                        on='date', 
                        ).mean().reset_index()
    d.to_csv(f'measured/lq/lq_{i}.csv', index=False)



