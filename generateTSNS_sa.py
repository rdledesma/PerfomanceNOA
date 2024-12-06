import pandas as pd
import matplotlib.pyplot as plt
from Geo import Geo
from datetime import timedelta
import numpy as np

d = pd.read_csv('nsrdb/SA/sa.csv', header=2)

d['date'] = pd.to_datetime(
    pd.date_range(
        start="2022/01/01 00:00", 
        end="2022/12/31 23:59", freq="10 min"))



d = d[['date','GHI']]

plt.figure()
plt.plot(d.date, d.GHI)

g = Geo(d.date + timedelta(minutes=5), 
            lat=-24.7288, 
            long=-65.4095, 
            gmt =0, 
            alt = 1233, 
            beta=0).df


d['sza'] = g.SZA.values


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
    
    
    sg = Geo(range_dates= s.date + timedelta(minutes= i/2), 
                lat=-24.7288, 
                long=-65.4095, 
                gmt =0, 
                alt = 1233, 
                beta=0).df
    
    s['sza'] = sg.SZA.values
    s['ghi'] = (s.ghi / sg.TOA).interpolate() * sg.TOA
    s['ghi'] = np.where(s.sza<83, s.ghi, np.nan)
    
    
    s.to_csv(f'nsrdb/SA/sa_{i}.csv', index=False)



