import pandas as pd
import matplotlib.pyplot as plt 
import Metrics as m


site = 'sa'
for f in [15]:
    freq = f
    d = pd.read_csv(f'measured/SA/{site}_{freq}.csv')
    print(d.ghi.mean())
    
ns = pd.read_csv(f'nsrdb/SA/{site}_{freq}.csv')
ca = pd.read_csv(f'cams/SA/{site}_{freq}.csv')
ds = pd.read_csv(f'DSR/SA/{site}_{freq}_linear.csv')
ls = pd.read_csv(f'LSA-SAF/SA/{site}_{freq}.csv')
er = pd.read_csv(f'era5/SA/{site}_{freq}.csv')
me = pd.read_csv(f'MERRA-2/SA/{site}_{freq}.csv')







d['date'] = pd.to_datetime(d.date)
ns['date'] = pd.to_datetime(ns.date)
ca['date'] = pd.to_datetime(ca.date)
ds['date'] = pd.to_datetime(ds.date)
ls['date'] = pd.to_datetime(ls.date)
er['date'] = pd.to_datetime(er.date)
me['date'] = pd.to_datetime(me.date)


plt.plot(d.date, d.ghi)
# plt.plot(ns.date, ns.ghi, label="NSRDB")
plt.plot(ca.date, ca.ghi, label="Heliosat-4")
plt.plot(ds.date, ds.ghi, label="DSR")
plt.plot(ls.date, ls.ghi, label="LSA-SAF")
plt.plot(er.date, er.ghi,label="ERA-5")
plt.plot(me.date, me.ghi, label="MERRA-2")
plt.grid()
plt.legend()



dates = d.dropna().date

d = (d.set_index('date')
      .reindex(dates)
      .rename_axis(['date'])
      #.fillna(0)
      .reset_index())


ca = (ca.set_index('date')
      .reindex(dates)
      .rename_axis(['date'])
      #.fillna(0)
      .reset_index())


ls = (ls.set_index('date')
      .reindex(dates)
      .rename_axis(['date'])
      #.fillna(0)
      .reset_index())

ds = (ds.set_index('date')
      .reindex(dates)
      .rename_axis(['date'])
      #.fillna(0)
      .reset_index())


er = (er.set_index('date')
      .reindex(dates)
      .rename_axis(['date'])
      #.fillna(0)
      .reset_index())


me = (me.set_index('date')
      .reindex(dates)
      .rename_axis(['date'])
      #.fillna(0)
      .reset_index())




d['ghica'] = ca.ghi.values
d['ghils'] = ls.ghi.values
d['ghids'] = ds.ghi.values
d['ghier'] = er.ghi.values
d['ghime'] = me.ghi.values
s = d.dropna()
s['n'] = s.date.dt.dayofyear


m.rrmsd(s.ghi, s.ghica) 
m.rrmsd(s.ghi, s.ghils) 
m.rrmsd(s.ghi, s.ghids)
m.rrmsd(s.ghi, s.ghier) 
m.rrmsd(s.ghi, s.ghime) 
