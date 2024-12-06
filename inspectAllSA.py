#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 17 17:34:17 2024

@author: dario
"""
import matplotlib.pyplot as plt
import pandas as pd
import Metrics as ms
rrmsd_results = []
site = 'SA'

for x in [60,30,15,10,5]:

    m60 = pd.read_csv(f'measured/{site}/sa_{x}.csv')
    c60 = pd.read_csv(f'cams/{site}/sa_{x}.csv')
    n60 = pd.read_csv(f'nsrdb/{site}/sa_{x}.csv')
    d60 = pd.read_csv(f'DSR/{site}/sa_{x}.csv')
    d60['GHI'] = d60.ghi
    
    me = pd.read_csv(f'MERRA-2/{site}/sa_{x}.csv')
    
    
    m60['date'] = pd.to_datetime(m60.date)
    m60 = m60[m60.date.dt.year.isin([2020,2021])]
    c60['date'] = pd.to_datetime(c60.date)
    c60 = c60[c60.date.dt.year.isin([2020,2021])]
    n60['date'] = pd.to_datetime(n60.date)
    n60 = n60[n60.date.dt.year.isin([2020,2021])]
    d60['date'] = pd.to_datetime(d60.date)
    d60 = d60[d60.date.dt.year.isin([2020,2021])]
    
    me['date'] = pd.to_datetime(me.date)
    
    
    
    
    df60 = pd.DataFrame()
    df60['date'] = m60.date.values
    df60['ghi'] = m60.ghi.values
    df60['Heliosat-4'] = c60.GHI.values
    df60['NSRDB'] = n60.GHI.values
    df60['DSR'] = d60.GHI.values
    df60['MERRA-2'] = me.ghi.values
    
    
    df60['sza'] = m60.SZA.values
    
    df60 = df60[df60.sza<90]
    
    df60 = df60.dropna()
    
    true = df60.ghi
    predHeliosat = df60['Heliosat-4']
    predNSRDB = df60['NSRDB']
    predDSR = df60['DSR']
    predMerra = df60['MERRA-2']

    print("####")
    
    print(ms.rrmsd(true, predHeliosat))
    print(ms.rrmsd(true, predNSRDB))
    print(ms.rrmsd(true, predDSR))
    print(ms.rrmsd(true, predMerra))

    print("####")



    rrmsd_results.append({
        'date': df60.date,
        'Heliosat-4': ms.rrmsd(true, predHeliosat),
        'NSRDB': ms.rrmsd(true, predNSRDB),
        'DSR': ms.rrmsd(true, predDSR),
        'MERRA-2': ms.rrmsd(true, predMerra)
    })
    
    
import seaborn as sns
df_rmsd = pd.DataFrame(rrmsd_results)
    
# Box Plot para visualizar la distribución del RRMSD
plt.figure(figsize=(10, 6))
sns.boxplot(data=df_rmsd[['Heliosat-4', 'NSRDB', 'DSR','MERRA-2']])
plt.title('Distribución del RRMSD para diferentes fuentes de datos')
plt.ylabel('RRMSD')
plt.xlabel('Fuente de Datos')
plt.show()





m30 = pd.read_csv(f'measured/{site}/lq_30.csv')
c30 = pd.read_csv(f'cams/{site}/lq_30.csv')
n30 = pd.read_csv(f'nsrdb/{site}/lq_30.csv')
d30 = pd.read_csv(f'DSR/{site}/lq_30.csv')
d30['GHI'] = d30.ghi

m15 = pd.read_csv(f'measured/{site}/lq_15.csv')
c15 = pd.read_csv(f'cams/{site}/lq_15.csv')
n15 = pd.read_csv(f'nsrdb/{site}/lq_15.csv')
d15 = pd.read_csv(f'DSR/{site}/lq_15.csv')
d15['GHI'] = d15.ghi


m60['date'] = pd.to_datetime(m60.date)
c60['date'] = pd.to_datetime(c60.date)
n60['date'] = pd.to_datetime(n60.date)
d60['date'] = pd.to_datetime(d60.date)


m60 = m60[m60.date.dt.year.isin([2021,2022])]
c60 = c60[c60.date.dt.year.isin([2021,2022])]
n60 = n60[n60.date.dt.year.isin([2021,2022])]
d60 = d60[d60.date.dt.year.isin([2021,2022])]




m30['date'] = pd.to_datetime(m30.date)
c30['date'] = pd.to_datetime(c30.date)
n30['date'] = pd.to_datetime(n30.date)
d30['date'] = pd.to_datetime(d30.date)


m30 = m30[m30.date.dt.year.isin([2021,2022])]
c30 = c30[c30.date.dt.year.isin([2021,2022])]
n30 = n30[n30.date.dt.year.isin([2021,2022])]
d30 = d30[d30.date.dt.year.isin([2021,2022])]


m15['date'] = pd.to_datetime(m15.date)
c15['date'] = pd.to_datetime(c15.date)
n15['date'] = pd.to_datetime(n15.date)
d15['date'] = pd.to_datetime(d15.date)


m15 = m15[m15.date.dt.year.isin([2021,2022])]
c15 = c15[c15.date.dt.year.isin([2021,2022])]
n15 = n15[n15.date.dt.year.isin([2021,2022])]
d15 = d15[d15.date.dt.year.isin([2021,2022])]






m60 = m60.dropna()
m60 = m60.dropna()
m60 = m60.dropna()
m60 = m60.dropna()



plt.plot(m60.date, m60.ghi, label="MEAS")
plt.plot(c60.date, c60.GHI, label="CAMS")
plt.plot(n60.date, n60.GHI, label="NSRDB")
plt.plot(d60.date, d60.ghi, label="DSR")
plt.legend()

true = m60.ghi
pred = d60.GHI

ms.rrmsd(true, pred)



#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 17 17:34:17 2024

@author: dario
"""
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import Metrics as ms

site = 'SA'
rrmsd_results = []

time_scales = [60, 30, 15, 10, 5]

for x in time_scales:

    m60 = pd.read_csv(f'measured/{site}/sa_{x}.csv')
    c60 = pd.read_csv(f'cams/{site}/sa_{x}.csv')
    n60 = pd.read_csv(f'nsrdb/{site}/sa_{x}.csv')
    d60 = pd.read_csv(f'DSR/{site}/sa_{x}.csv')
    me = pd.read_csv(f'MERRA-2/{site}/sa_{x}.csv')
    era = pd.read_csv(f'era5/{site}/sa_{x}.csv')
    lsa = pd.read_csv(f'LSA-SAF/{site}/sa_{x}.csv')
    d60['GHI'] = d60.ghi
    
    m60['date'] = pd.to_datetime(m60['date'])
    m60 = m60[m60.date.dt.year.isin([2020, 2021])]
    c60['date'] = pd.to_datetime(c60['date'])
    c60 = c60[c60.date.dt.year.isin([2020, 2021])]
    n60['date'] = pd.to_datetime(n60['date'])
    n60 = n60[n60.date.dt.year.isin([2020, 2021])]
    d60['date'] = pd.to_datetime(d60['date'])
    d60 = d60[d60.date.dt.year.isin([2020, 2021])]
    me['date'] = pd.to_datetime(me.date)
    era['date'] = pd.to_datetime(era.date)
    lsa['date'] = pd.to_datetime(lsa.date)
    
    
    df60 = pd.DataFrame()
    df60['date'] = m60.date.values
    df60['ghi'] = m60.ghi.values
    df60['Heliosat-4'] = c60.GHI.values
    df60['NSRDB'] = n60.GHI.values
    df60['DSR'] = d60.GHI.values
    df60['MERRA'] = me.ghi.values
    df60['ERA-5'] = era.ghi.values
    df60['LSA-SAF'] = lsa.ghi.values
    df60['sza'] = m60.SZA.values
   
    
    
    df60 = df60[df60.sza < 80]
    df60 = df60.dropna()
    
    true = df60.ghi
    predHeliosat = df60['Heliosat-4']
    predNSRDB = df60['NSRDB']
    predDSR = df60['DSR']
    predMerra = df60['MERRA']
    predEra = df60['ERA-5']
    predLsa = df60['LSA-SAF']
    rrmsd_results.append({
        'time_scale': x,
        'Heliosat-4': ms.rrmsd(true, predHeliosat),
        'NSRDB': ms.rrmsd(true, predNSRDB),
        'GOES DSR': ms.rrmsd(true, predDSR),
        'MERRA-2': ms.rrmsd(true, predMerra),
        'ERA-5': ms.rrmsd(true, predEra),
        'LSA-SAF': ms.rrmsd(true, predLsa)
    })

# Convertir rrmsd_results en un DataFrame para visualización
df_rmsd = pd.DataFrame(rrmsd_results)

# Box Plot para visualizar la distribución del RRMSD a través de las escalas temporales
plt.figure(figsize=(10, 6))
sns.boxplot(data=df_rmsd.melt(id_vars='time_scale', value_vars=[
    'Heliosat-4', 
    'NSRDB', 
    'GOES DSR',
    'MERRA-2',
    'ERA-5',
    'LSA-SAF']),
            x='time_scale', y='value', hue='variable')
plt.title('Distribución del RRMSD para diferentes fuentes de datos y escalas temporales')
plt.ylabel('RRMSD')
plt.xlabel('Escala Temporal (min)')
plt.legend(title='Fuente de Datos')
plt.show()

# Gráfico de líneas para visualizar el RRMSD a través de las escalas temporales
plt.figure(figsize=(12, 6))
for col in ['Heliosat-4', 'NSRDB', 'GOES DSR','MERRA-2','ERA-5','LSA-SAF']:
    plt.plot(df_rmsd['time_scale'], df_rmsd[col], label=col, marker='o')
plt.title('RRMSD a través de las escalas temporales en SA')
plt.ylabel('RRMSD')
plt.xlabel('Escala Temporal (min)')
plt.legend(title='Fuente de Datos')
plt.show()






