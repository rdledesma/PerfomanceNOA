import pandas as pd 
import matplotlib.pyplot as plt
from NollasQC import QC
import numpy as np
from Geo import Geo

d20 = pd.read_csv('measured/LQ/GHI_LQ/GHI_LQ2020.csv')
d21 = pd.read_csv('measured/LQ/GHI_LQ/GHI_LQ2021.csv')

d = pd.concat([d20,d21])
d.columns = ['a','b','c','ghi','date']

d = d[['date','ghi']]
d['date'] = pd.to_datetime(d.date)

d = d[d.date.dt.year<2022]
del d20, d21

plt.plot(d.date, d.ghi)



d = (d.set_index('date')
      .reindex(pd.date_range(
          start="2020/01/01", end="2021/12/31", freq="1min"))
      .rename_axis(['date'])
      #.fillna(0)
      .reset_index())




g = Geo(range_dates= d.date, 
            lat=-22.1038, 
            long=-65.60125, 
            gmt =0, 
            alt = 3500, 
            beta=0).df

g['ghi'] = d.ghi.values


QC(g)

d['sza'] = g.SZA.values
d['argp'] = g.GHIargp2.values
d['Acepted'] = g.Acepted.values


d['ghi'] = np.where(d.Acepted, d.ghi, np.nan)
d['ghi'] = np.where(d.sza<83, d.ghi, np.nan)

plt.plot(d.date, d.ghi)
plt.plot(d.date, d.argp)

from datetime import timedelta

for i in [1,5,10,15,30,60]:
    s = d.resample(
                        f'{i} min', 
                        on='date', 
                        ).mean().reset_index()
    
    
    gs = Geo(range_dates= s.date + timedelta(minutes=int(i/2)), 
                lat=-22.1038, 
                long=-65.60125, 
                gmt =0, 
                alt = 3500, 
                beta=0).df

    s['sza'] = gs.SZA.values
    s['argp'] = gs.GHIargp2.values
    s['ghi'] = np.where(s.Acepted>0.6, s.ghi, np.nan)
    s['ghi'] = np.where(s.sza<83, s.ghi, np.nan)

    s.to_csv(f'measured/LQ/lq_{i}.csv', index=False)



