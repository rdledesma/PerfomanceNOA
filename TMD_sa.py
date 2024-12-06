import pandas as pd
import matplotlib.pyplot as plt 
import Metrics as m

import pandas as pd
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 08:57:23 2024
@author: rdledesma
"""

import numpy as np
import pandas as pd
import pvlib
from scipy import interpolate
import matplotlib.pyplot as plt
import Metrics as m

# Cálculo de la función de distribución acumulada empírica (CDF)
def ecdf(x): 
    # Ordena el array de datos de menor a mayor
    xs = np.sort(x)
    # Genera un array de probabilidades que corresponde a la posición relativa de cada valor
    ys = np.arange(1, len(xs)+1) / float(len(xs))
    # Devuelve los datos ordenados y las probabilidades asociadas (CDF)
    return xs, ys

import pandas as pd
import matplotlib.pyplot as plt 
import Metrics as m


med = 491.9
site = 'sa'
for f in [60]:
    freq = f
    d = pd.read_csv(f'measured/SA/{site}_{freq}.csv')
    d['date'] = pd.to_datetime(d.date)
    # d=d[d.date.dt.year == 2021]
    print(d.ghi.mean())
    
gc = pd.read_csv(f'CIM/SA/{site}_{freq}.csv')
ca = pd.read_csv(f'cams/SA/{site}_{freq}.csv')
ds = pd.read_csv(f'DSR/SA/{site}_{freq}.csv')
ls = pd.read_csv(f'LSA-SAF/SA/{site}_{freq}.csv')
ns= pd.read_csv(f'nsrdb/SA/{site}_{freq}.csv')
er = pd.read_csv(f'era5/SA/{site}_{freq}.csv')
me = pd.read_csv(f'MERRA-2/SA/{site}_{freq}.csv')

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           

d['date'] = pd.to_datetime(d.date)
ns['date'] = pd.to_datetime(ns.date)
ca['date'] = pd.to_datetime(ca.date)
ds['date'] = pd.to_datetime(ds.date)
ls['date'] = pd.to_datetime(ls.date)
gc['date'] = pd.to_datetime(gc.date)
er['date'] = pd.to_datetime(er.date)
me['date'] = pd.to_datetime(me.date)

plt.figure()
plt.plot(d.ghi.values)
#plt.plot(ns.date, ns.ghi.values, label="NSRDB")
plt.plot(ds.ghi.values, label="G-CIM")

# # # plt.plot(ca.date, ca.ghi, label="Heliosat-4")
# # # plt.plot(ds.date, ds.ghi, label="DSR")
# # # plt.plot(ls.date, ls.ghi, label="LSA-SAF")
# # # plt.plot(er.date, er.ghi,label="ERA-5")
# # # plt.plot(me.date, me.ghi, label="MERRA-2")
# plt.grid()
# plt.legend()



dates = d.dropna().date

d = (d.set_index('date')
      .reindex(dates)
      .rename_axis(['date'])
      #.fillna(0)
      .reset_index())

# ns = (ns.set_index('date')
#       .reindex(dates)
#       .rename_axis(['date'])
#       #.fillna(0)
#       .reset_index())


ca = (ca.set_index('date')
      .reindex(dates)
      .rename_axis(['date'])
      #.fillna(0)
      .reset_index())

ds = (ds.set_index('date')
      .reindex(dates)
      .rename_axis(['date'])
      #.fillna(0)
      .reset_index())

ls = (ls.set_index('date')
      .reindex(dates)
      .rename_axis(['date'])
      #.fillna(0)
      .reset_index())


gc = (gc.set_index('date')
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


# plt.plot(d.date, d.ghi)
# plt.plot(ds.date, ds.ghi)



# d['ghins'] = ns.ghi.values
d['ghica'] = ca.ghi.values
d['ghils'] = ls.ghi.values
d['ghigc'] = gc.ghi.values
d['ghids'] = ds.ghi.values
d['ghier'] = er.ghi.values
d['ghime'] = me.ghi.values



import datetime


s = d.dropna()

s = s[s.date.dt.date != datetime.datetime(2023,2,22).date() ]

s = s[s.date.dt.date != datetime.datetime(2023,2,16).date() ]


#s = s[s.sza<80]
# s = s[(s.ghi / s.argp)<1.3]



# s = d.dropna()
# s = s[s.sza<80]
# s = s[(s.ghi / s.argp)<1.3]


s['H'] = s.date.dt.hour

sHorario = s.groupby(by=['H']).mean().reset_index()

cdfMean = ecdf(sHorario.ghi.values)


plt.plot(cdfMean[0],cdfMean[1])

import Metrics as m
days = []
error = []
for day in s.date.dt.date.unique():
    dact = d[d.date.dt.date == day]
    
    cdfact = ecdf(dact.ghi.values)[1]
    days.append(day)
    error.append(m.rrmsd(cdfMean[1], cdfact[1]))


tpd = s[s.date.dt.date == datetime.datetime(2022,10,27).date() ]



# plt.plot(tpd.argp, label="ARGPv2")
plt.plot(tpd.ghi, label="MEAS")
plt.plot(tpd.ghigc, label="GCIM")
# plt.plot(tpd.ghins, label="NSRDB")
plt.plot(tpd.ghids, label="DSR")
plt.plot(tpd.ghils, label="LSA-SAF")
plt.plot(tpd.ghica, label="CAMS")
plt.legend()


