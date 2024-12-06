import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import timedelta
from Geo import Geo

c = pd.read_csv('cams/SA/sa_60.csv')
c['date'] = pd.to_datetime(c.date)
dates = pd.date_range(
    start="2022/01/01 00:00",
    end="2022/12/31 23:59", freq="1 min")


d = pd.read_csv('DSR/SA_DSR.csv')
d['date'] = pd.to_datetime(d.date)
d['DSR'] = np.where(d.DQF ==1, np.nan, d.DSR)

d['DSR'] = np.where(d.DSR >1500, np.nan, d.DSR)






d = d[d.date.dt.year==2022]
d = d.sort_values(by=['date']).dropna()

d['date'] = d['date'].dt.strftime('%Y-%m-%d %H:%M:00')
d['date'] = pd.to_datetime(d.date)



d = (d.set_index('date')
      .reindex(dates)
      .rename_axis(['date'])
      #.fillna(0)
      .reset_index())






g = Geo(d.date + timedelta(minutes=0.5), 
            lat=-24.7288, 
            long=-65.4095, 
            gmt=0, 
            beta=0,
            alt=1233).df


d['sza'] = g.SZA.values
d['DSR'] = np.where(g.SZA<90, d.DSR, 0)


d['DSRras'] = (d.DSR / g.TOA).interpolate() * g.TOA 
d['DSRras']= np.where(g.SZA<80, d.DSRras, np.nan)
d['DSRras'] = d['DSRras'].shift(-30)




d['DSRLin'] =d.DSR.interpolate()
d['DSRLin'] = np.where(g.SZA<80, d.DSRLin, np.nan)

d['DSRLin'] = d['DSRLin'].shift(-30)


dhorario = d[['date','DSRLin','DSRras']].resample(
                    f'60 min', 
                    on='date', 
                    ).mean().reset_index()


gh = Geo(dhorario.date + timedelta(minutes=30), 
            lat=-24.7288, 
            long=-65.4095, 
            gmt=0, 
            beta=0,
            alt=1233).df


dhorario['sza'] = gh.SZA.values

dhorario['DSRLin'] = np.where(dhorario.sza<83, dhorario.DSRLin, np.nan)
dhorario['DSRras'] = np.where(dhorario.sza<83, dhorario.DSRras, np.nan)


plt.figure()
plt.plot(dhorario.date, dhorario.DSRras)
plt.plot(dhorario.date, dhorario.DSRLin)
plt.plot(c.date, c.ghi)
plt.grid()


dhorario.to_csv('DSR/SA/sa_2023.csv', index=False)
