import pandas as pd
import matplotlib.pyplot as plt
from Geo import Geo
import numpy as np
from NollasQC import QC
import datetime
d0 = pd.read_csv('measured/SA/sla_2022.csv')
d1 = pd.read_csv('measured/SA/sa_2023_raw.csv')

d0.columns = ['date','ghi']

d = pd.concat([d0,d1])
d['date'] = pd.to_datetime(d.date)


d = d[d.date.dt.date >= 	datetime.date(2022,10,7)]




d['ghi'] = np.where((d.date.dt.date >= 	datetime.date(2022,11,29)) & (d.date.dt.date <= 	datetime.date(2022,12,21)) , np.nan, d.ghi)


d['ghi'] = np.where((d.date.dt.date >= 	datetime.date(2022,12,21)) & (d.date.dt.date <= 	datetime.date(2022,12,31)) , np.nan, d.ghi)



d['ghi'] = np.where((d.date.dt.date >= 	datetime.date(2023,2,16)) & (d.date.dt.date <= 	datetime.date(2022,2,22)) , np.nan, d.ghi)




d['ghi'] = np.where((d.date >= 	datetime.datetime(2023,5,15,13,50)) & (d.date <= 	datetime.datetime(2023,5,15,14,00)) , np.nan, d.ghi)


dates = pd.date_range(
    start="2022/10/07 00:00", 
    end="2023/12/31 23:59", freq="1min")

# df = d.loc[~d.index.duplicated(keep='first')]
# df = df.reset_index(drop=True)
d = (d.set_index('date')
      .reindex(dates)
      .rename_axis(['date'])
      #.fillna(0)
      .reset_index())


plt.figure()
plt.plot(d.date, d.ghi)

g = Geo(d.date, 
            lat=-24.7288, 
            long=-65.4095, 
            gmt=0, 
            beta=0,
            alt=1233).df


g['ghi'] = d.ghi.shift(180).values

plt.figure()
plt.plot(g.date, g.ghi)
plt.plot(g.date, g.TOA)


QC(g)



g['ghi'] = np.where(g.Acepted, g.ghi, np.nan)

plt.figure()
plt.plot(g.date, g.ghi)
plt.plot(g.date, g.TOA)

g['ghi'] = np.where(g.SZA<83, g.ghi, np.nan)


plt.figure()
plt.plot(g.date, g.ghi)
plt.plot(g.date, g.GHIargp2)


from datetime import timedelta
for i in [1,5,10,15,30,60]:
    d = g[['date','ghi']].resample(
                        f'{i} min', 
                        on='date', 
                        ).mean().reset_index()
    
    
    sg = Geo(range_dates= d.date + timedelta(minutes= i/2), 
                lat=-24.7288, 
                long=-65.4095, 
                gmt=0, 
                beta=0,
                alt=1233).df
    
    d['sza'] = sg.SZA
    d['ghi'] = np.where(d.sza<83, d.ghi, np.nan)
    
    d.to_csv(f'measured/SA/sa_{i}.csv', index=False)





