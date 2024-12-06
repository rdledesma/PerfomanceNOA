#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 10 13:54:25 2024

@author: dario
"""
import pandas as pd
import Metrics as m
import Geo
from datetime import timedelta
for i in [1,5,10,15,30,60]:
    d = pd.read_csv(f'measured/LQ/lq_{i}.csv')
    c = pd.read_csv(f'nsrdb/LQ/lq_{i}.csv')

    c['date'] = pd.to_datetime(c.date)
    d['date'] = pd.to_datetime(d.date)
    
    
    
 
    c = (c.set_index('date')
          .reindex(d.date)
          .rename_axis(['date'])
          #.fillna(0)
          .reset_index())

    

    c['ghi'] = d.ghi.values
    
    
    
    g = Geo.Geo(c.date  + timedelta(minutes = i/2), 
                -22.103936, 
                -65.599923, 
                gmt =0, 
                alt = 3468, 
                beta=0).df

    c['sza'] = g.SZA.values
    c['mak'] = g.Mak.values
    c['alpha'] = g.alphaS.values
    c['argp2'] = g.GHIargp2.values
    c['ghicc'] = c['Clearsky GHI']
    c['ktmod'] = c['GHI'] / g['TOA'].values
    c['kcmod'] = c['GHI'] / c['ghicc']
    c['kcmodargp'] = c['GHI'] / c['argp2']
    c = c.drop(['Clearsky GHI'], axis=1)
    
    
    
    
    
    
    
    c.to_csv(f'process/LQNSRDB/{i}.csv', index=False)
    
    s = c.dropna()

    pred = s.GHI.values
    true = s.ghi.values

    m.rrmsd(true, pred)
    print(m.rrmsd(true, pred))
