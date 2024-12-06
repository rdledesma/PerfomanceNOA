import pandas as pd
import matplotlib.pyplot as plt
from Geo import Geo
from datetime import timedelta
import numpy as np

d1 = pd.read_csv('nsrdb/LQ/lq_2020.csv', header=2)
d2 = pd.read_csv('nsrdb/LQ/lq_2021.csv', header=2)

d = pd.concat([d1,d2])

d['date'] = pd.to_datetime(
    pd.date_range(
        start="2020/01/01 00:00", end="2021/12/31 23:59", freq="10 min"))



d = d[['date','GHI','Clearsky GHI']]


plt.plot(d.date, d.GHI)


g = Geo(range_dates= d.date + timedelta(minutes=5), 
            lat=-22.1038, 
            long=-65.60125, 
            gmt =0, 
            alt = 3500, 
            beta=0).df


d['sza'] = g.SZA.values

plt.plot(g.date, g.GHIargp2)
plt.plot(d.date, d['Clearsky GHI'])


g['ghi'] = d.GHI.values
g['ghi'] = np.where(g.SZA<83, g.ghi, np.nan)
g['ghi'] = np.where(g.ghi>0, g.ghi, np.nan)

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
    s['ghi'] = s.ghi.interpolate()
    s['ghi'] = np.where(s.sza<83, s.ghi, np.nan)
    
    if i == 5:
        t = s
    
    
    s.to_csv(f'nsrdb/LQ/lq_{i}.csv', index=False)



