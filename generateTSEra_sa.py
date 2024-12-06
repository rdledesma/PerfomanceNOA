import pandas as pd
import matplotlib.pyplot as plt
from Geo import Geo
import numpy as np
from datetime import timedelta

d = pd.read_csv('era5/SA/SLA.csv')
d['date'] = pd.to_datetime(d.date)

d = d[d.date.dt.year.isin([2022,2023])]

dates = pd.date_range(
    start="2022/01/01 00:00", end="2023/12/31 23:59",
    freq="1h")


plt.plot(d.ghi.values)

g = Geo(dates + timedelta(minutes=30), 
            lat=-24.7288, 
            long=-65.4095, 
            gmt=0, 
            beta=0,
            alt=1233).df

plt.figure()
plt.plot(g.GHIargp2.values)
plt.plot(d.ghi.shift(-1).values)




g['sza'] = g.SZA.values
g['ghi'] = d.ghi.shift(-1).values

plt.figure()
plt.plot(g.date, g.ghi)


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
    #s['ghi'] = s.ghi.interpolate() 
    s['ghi'] = np.where(s.sza<83, s.ghi, np.nan)
    
    
    s.to_csv(f'era5/SA/sa_{i}.csv', index=False)




