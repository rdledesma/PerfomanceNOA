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

x = 60

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
df60['sza'] = d60.SZA.values
df60['kc'] = d60.ghi / d60.GHIargp2
df60 = df60[df60.sza < 80]
df60 = df60.dropna()

df60 = df60.sort_values(by=['sza'])

# Crear una nueva columna para los grupos de SZA
bins = list(range(0, 90, 10))
labels = [f'{i}-{i+10}' for i in range(0, 80, 10)]
df60['sza_group'] = pd.cut(df60['sza'], bins=bins, labels=labels, right=False)

for sza_group in df60['sza_group'].unique():
    df_group = df60[df60['sza_group'] == sza_group]
    true = df_group.ghi
    predHeliosat = df_group['Heliosat-4']
    predNSRDB = df_group['NSRDB']
    predDSR = df_group['DSR']
    predMerra = df_group['MERRA']
    predEra = df_group['ERA-5']
    predLsa = df_group['LSA-SAF']
    rrmsd_results.append({
        'time_scale': x,
        'sza_group': sza_group,
        'Heliosat-4': ms.rrmsd(true, predHeliosat),
        'NSRDB': ms.rrmsd(true, predNSRDB),
        'GOES DSR': ms.rrmsd(true, predDSR),
        'MERRA-2': ms.rrmsd(true, predMerra),
        'ERA-5': ms.rrmsd(true, predEra),
        'LSA-SAF': ms.rrmsd(true, predLsa)
    })


# Convertir rrmsd_results en un DataFrame para visualización
df_rmsd = pd.DataFrame(rrmsd_results)


df_rmsd = df_rmsd[['sza_group', 'Heliosat-4', 'NSRDB', 'GOES DSR','LSA-SAF', 'MERRA-2', 'ERA-5']]


# Gráfico de barras para visualizar el RRMSD para cada fuente de datos en cada escala temporal
df_rmsd_melted = df_rmsd.melt(id_vars='sza_group', var_name='Fuente de Datos', value_name='RRMSD')



plt.figure(figsize=(14, 8))
sns.barplot(data=df_rmsd_melted, x='sza_group', y='RRMSD', hue='Fuente de Datos')
#plt.title('RRMSD para diferentes fuentes de datos y escalas temporales')
plt.ylabel('RMSE (%)', fontsize=30)
plt.xlabel('Escala Temporal (min)', fontsize=30)
plt.legend(title='Fuente de Datos', fontsize=10,  ncol = 6 )
plt.show()
