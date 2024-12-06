#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 14:06:10 2024

@author: solar
"""

import pandas as pd
import time

SITE = "lq"

dates = pd.date_range(start="2021/01/01 00:00", 
                      end="2022/12/31 23:59", freq="10min")
    
d = pd.read_csv('CIM/lq/lq_10.csv')
d['date'] = pd.to_datetime(d.date)
d = d[d.date.dt.year.isin([2021,2022])]


dates = pd.date_range(start="2021/01/01 00:00", 
                      end="2022/12/31 23:59", freq="1min")

d = (d.set_index('date')
      .reindex(dates)
      .rename_axis(['date'])
      #.fillna(0)
      .reset_index())


d = d.interpolate()


for i in [1,5,10,15,30,60]:
    s = d.resample(
                        f'{i} min', 
                        on='date', 
                        ).mean().reset_index()
   
    s.to_csv(f'CIM/lq/lq_{i}.csv', index=False)





