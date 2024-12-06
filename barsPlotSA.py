#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 10:11:07 2024

@author: dario
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import Metrics as ms

site = 'SA'
rrmsd_results = []

time_scales = [60, 30, 15, 10, 5,1]

for x in time_scales:
    m60 = pd.read_csv(f'measured/{site}/sa_{x}.csv')
    c60 = pd.read_csv(f'cams/{site}/sa_{x}.csv')
    n60 = pd.read_csv(f'nsrdb/{site}/sa_{x}.csv')
    d60 = pd.read_csv(f'DSR/{site}/sa_{x}.csv')
    me = pd.read_csv(f'MERRA-2/{site}/sa_{x}.csv')
    era = pd.read_csv(f'era5/{site}/sa_{x}.csv')
    lsa = pd.read_csv(f'LSA-SAF/{site}/sa_{x}.csv')
    cim = pd.read_csv(f'CIM/{site}/sa_{x}.csv')
    
    
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
    cim['date'] = pd.to_datetime(cim.date)
    
    
    cim = (cim.set_index('date')
          .reindex(d60.date)
          .rename_axis(['date'])
          #.fillna(0)
          .reset_index())

    
    
    df60 = pd.DataFrame()
    df60['date'] = m60.date.values
    df60['ghi'] = m60.ghi.values
    df60['Heliosat-4'] = c60.GHI.values
    df60['NSRDB'] = n60.GHI.values
    df60['DSR'] = d60.GHI.values
    df60['MERRA'] = me.ghi.values
    df60['ERA-5'] = era.ghi.values
    df60['LSA-SAF'] = lsa.ghi.values
    df60['CIM'] = cim.ghiCMI.values
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
    predCim = df60['CIM']
    rrmsd_results.append({
        'time_scale': x,
        'Heliosat-4': ms.rrmsd(true, predHeliosat),
        'NSRDB':      ms.rrmsd(true, predNSRDB),
        'GOES DSR':   ms.rrmsd(true, predDSR),
        'MERRA-2':    ms.rrmsd(true, predMerra),
        'ERA-5':      ms.rrmsd(true, predEra),
        'LSA-SAF':    ms.rrmsd(true, predLsa),
        'G-CIM':      ms.rrmsd(true, predCim)
    })

# Convertir rrmsd_results en un DataFrame para visualización
df_rmsd = pd.DataFrame(rrmsd_results)

df_rmsd = df_rmsd[['time_scale', 'Heliosat-4', 'NSRDB', 'GOES DSR','G-CIM','LSA-SAF','MERRA-2', 'ERA-5']]



# Gráfico de barras para visualizar el RRMSD para cada fuente de datos en cada escala temporal
df_rmsd_melted = df_rmsd.melt(id_vars='time_scale', var_name='Fuente de Datos', value_name='RRMSD')

plt.figure(figsize=(14, 8))
sns.barplot(data=df_rmsd_melted, x='time_scale', y='RRMSD', hue='Fuente de Datos')
#plt.title('RRMSD para diferentes fuentes de datos y escalas temporales')
plt.ylabel('SS4 (W/m²)', fontsize=30)
plt.xlabel('Temporal res. (min)', fontsize=30, )
plt.legend(title='Models', fontsize=12,ncol=7, loc="lower center")
plt.grid()
plt.show()




plt.figure(figsize=(14, 8))
sns.barplot(data=df_rmsd_melted, x='time_scale', y='RRMSD', hue='Fuente de Datos',palette='Paired')
plt.ylabel('RMSE(%)', fontsize=30)
plt.xlabel('Temporal res. (min)', fontsize=30)
plt.legend(title='', fontsize=15, ncol=7, loc="lower center", bbox_to_anchor=(0.5, -0.2), frameon=False, columnspacing=1, handletextpad=0.1)
plt.grid()
plt.show()






plt.figure(figsize=(14, 8))

# Gráfico de líneas
sns.lineplot(data=df_rmsd_melted, x='time_scale', y='RRMSD', hue='Fuente de Datos', palette='Paired', marker='o')

# Etiquetas de los ejes
plt.ylabel('MBE(%)', fontsize=30)
plt.xlabel('Temporal res. (min)', fontsize=30)

# Leyenda
plt.legend(title='', fontsize=15, ncol=7, loc="lower center", bbox_to_anchor=(0.5, -0.2), frameon=False, columnspacing=1, handletextpad=0.1)

# Grid
plt.grid()

# Mostrar el gráfico
plt.show()


