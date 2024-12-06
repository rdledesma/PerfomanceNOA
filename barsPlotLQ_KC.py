import pandas as pd

x = 60
site = 'LQ'

m60 = pd.read_csv(f'measured/{site}/lq_{x}.csv')
c60 = pd.read_csv(f'cams/{site}/lq_{x}.csv')
n60 = pd.read_csv(f'nsrdb/{site}/lq_{x}.csv')
d60 = pd.read_csv(f'DSR/{site}/lq_{x}.csv')
me = pd.read_csv(f'MERRA-2/{site}/lq_{x}.csv')
era = pd.read_csv(f'era5/{site}/lq_{x}.csv')
lsa = pd.read_csv(f'LSA-SAF/{site}/lq_{x}.csv')
d60['GHI'] = d60.ghi

m60['date'] = pd.to_datetime(m60['date'])
m60 = m60[m60.date.dt.year.isin([2021, 2022])]
c60['date'] = pd.to_datetime(c60['date'])
c60 = c60[c60.date.dt.year.isin([2021, 2022])]
n60['date'] = pd.to_datetime(n60['date'])
n60 = n60[n60.date.dt.year.isin([2021, 2022])]
d60['date'] = pd.to_datetime(d60['date'])
d60 = d60[d60.date.dt.year.isin([2021, 2022])]
me['date'] = pd.to_datetime(me.date)
era['date'] = pd.to_datetime(era.date)
lsa['date'] = pd.to_datetime(lsa.date)

df = pd.DataFrame()
df['date'] = m60.date.values
df['ghi'] = m60.ghi.values
df['Heliosat-4'] = c60.GHI.values
df['NSRDB'] = n60.GHI.values
df['DSR'] = d60.GHI.values
df['MERRA'] = me.ghi.values
df['ERA-5'] = era.ghi.values
df['LSA-SAF'] = lsa.ghi.values
df['sza'] = d60.SZA.values
df['date'] = pd.to_datetime(df.date)

models = ['Heliosat-4', 'NSRDB', 'DSR','LSA-SAF', 'MERRA', 'ERA-5']

df = df.dropna()
df['date'] = pd.to_datetime(df.date)
df = df[df.sza<85]

mean = df.ghi.mean()

import Metrics as ms
import numpy as np
for rangekc in np.arange(0,1, 0.1):
    print(rangekc,rangekc+0.1 )
    
rmsevals = []
for m in models:
    true = df.ghi.values
    pred = df[m].values
    
    
    
    
    
    