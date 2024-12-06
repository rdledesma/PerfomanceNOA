#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 10:20:36 2024

@author: dario
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import Metrics as ms
import numpy as np
# Definir una función para asignar estaciones
def get_season(date):

    
    m = date.month
    x = m%12 // 3 + 1
    if x == 1:
      season = "Invierno"
    if x == 2:
      season = "Primavera"
    if x == 3:
      season = "Verano"
    if x == 4:
      season = "Otoño"
    return season


site = 'SA'
rrmsd_results = []
rmae_results = []
rmbe_results = []
time_scales = [60]

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
   df60['G-CIM'] = cim.ghiCMI.values
   df60['sza'] = m60.SZA.values
      
   df60['season'] = 'Summer'
   df60['season'] = np.where((df60.date.dt.dayofyear>=81) & (df60.date.dt.dayofyear<173),'Autumn', df60.season )
   df60['season'] = np.where((df60.date.dt.dayofyear>=173) & (df60.date.dt.dayofyear<265),'Winter',df60.season )
   df60['season'] = np.where((df60.date.dt.dayofyear>=265) & (df60.date.dt.dayofyear<356),'Spring',df60.season )



    
   df60 = df60[df60.sza < 80]
   df60 = df60.dropna()
   
   
   true = df60.ghi
   predHeliosat = df60['Heliosat-4']
   predNSRDB = df60['NSRDB']
   predDSR = df60['DSR']
   predMerra = df60['MERRA']
   predEra = df60['ERA-5']
   predLsa = df60['LSA-SAF']
   predCim = df60['G-CIM']
   rrmsd_results.append({
       'time_scale': x,
       'Heliosat-4': ms.rrmsd(true, predHeliosat),
       'NSRDB':      ms.rrmsd(true, predNSRDB),
       'GOES DSR':   ms.rrmsd(true, predDSR),
       'MERRA-2':    ms.rrmsd(true, predMerra),
       'ERA-5':      ms.rrmsd(true, predEra),
       'LSA-SAF':    ms.rrmsd(true, predLsa),
       'G-CIM':        ms.rrmsd(true, predCim)
   })
   
   df60['season'] = 'Summer'
   df60['season'] = np.where((df60.date.dt.dayofyear>=81) & (df60.date.dt.dayofyear<173),'Autumn', df60.season )
   df60['season'] = np.where((df60.date.dt.dayofyear>=173) & (df60.date.dt.dayofyear<265),'Winter',df60.season )
   df60['season'] = np.where((df60.date.dt.dayofyear>=265) & (df60.date.dt.dayofyear<356),'Spring',df60.season )
   
   
   df60 = df60[df60.sza < 80]
   df60 = df60.dropna()

   for season in df60['season'].unique():
       df_season = df60[df60['season'] == season]
       true = df_season.ghi
       predHeliosat = df_season['Heliosat-4']
       predNSRDB = df_season['NSRDB']
       predDSR = df_season['DSR']
       predGCIM = df_season['G-CIM']
       predMerra = df_season['MERRA']
       predEra = df_season['ERA-5']
       predLsa = df_season['LSA-SAF']
       rrmsd_results.append({
           'time_scale': x,
           'season': season,
           'Heliosat-4': ms.rrmsd(true, predHeliosat),
           'NSRDB': ms.rrmsd(true, predNSRDB),
           'GOES DSR': ms.rrmsd(true, predDSR),
           'G-CIM': ms.rrmsd(true, predGCIM),
           'MERRA-2': ms.rrmsd(true, predMerra),
           'ERA-5': ms.rrmsd(true, predEra),
           'LSA-SAF': ms.rrmsd(true, predLsa)
       })
       
       rmae_results.append({
           'time_scale': x,
           'season': season,
           'Heliosat-4': ms.rmae(true, predHeliosat),
           'NSRDB': ms.rmae(true, predNSRDB),
           'GOES DSR': ms.rmae(true, predDSR),
           'G-CIM': ms.rmae(true, predGCIM),
           'MERRA-2': ms.rmae(true, predMerra),
           'ERA-5': ms.rmae(true, predEra),
           'LSA-SAF': ms.rmae(true, predLsa)
       })
       
       rmbe_results.append({
           'time_scale': x,
           'season': season,
           'Heliosat-4': ms.rmbe(true, predHeliosat),
           'NSRDB': ms.rmbe(true, predNSRDB),
           'GOES DSR': ms.rmbe(true, predDSR),
           'G-CIM': ms.rmbe(true, predGCIM),
           'MERRA-2': ms.rmbe(true, predMerra),
           'ERA-5': ms.rmbe(true, predEra),
           'LSA-SAF': ms.rmbe(true, predLsa)
       })
   
   
   
   


# Convertir rrmsd_results en un DataFrame para visualización
df_rmsd = pd.DataFrame(rrmsd_results)
# df_rmae = pd.DataFrame(rmae_results)
# df_rmbe = pd.DataFrame(rmbe_results)

df_rmsd = df_rmsd[['season','Heliosat-4', 'NSRDB', 'GOES DSR','G-CIM','LSA-SAF','MERRA-2', 'ERA-5']]
# df_rmae = df_rmae[['season','Heliosat-4', 'NSRDB', 'GOES DSR','G-CIM','LSA-SAF','MERRA-2', 'ERA-5']]
# df_rmbe = df_rmbe[['season','Heliosat-4', 'NSRDB', 'GOES DSR','G-CIM','LSA-SAF','MERRA-2', 'ERA-5']]


# Gráfico de barras para visualizar el RRMSD para cada fuente de datos, escala temporal y estación
df_rmsd_melted = df_rmsd.melt(id_vars=['season'], var_name='Fuente de Datos', value_name='RRMSD')

# Gráfico de barras agrupado por estación con la leyenda desactivada
g = sns.catplot(data=df_rmsd_melted, y='RRMSD', hue='Fuente de Datos', 
                col='season', kind='bar', col_wrap=2, ci=None, palette='Paired')

# Cambiar las etiquetas de las columnas para mostrar solo el nombre de la estación
for ax in g.axes.flat:
    ax.set_title(ax.get_title().split('=')[1])

# Añadir la leyenda personalizada usando Matplotlib debajo del gráfico
# Ajustar los márgenes para dar espacio a la leyenda
plt.subplots_adjust(bottom=0.05)
sns.move_legend(g, "lower center", bbox_to_anchor=(.45, 0), title='', ncol=7)
plt.show()







# Gráfico de barras agrupado por estación
g = sns.catplot(data=df_rmsd_melted, x='time_scale', y='RRMSD', hue='Fuente de Datos', col='season', kind='bar', col_wrap=2, ci=None)
# g.fig.suptitle('RRMSD para diferentes fuentes de datos, escalas temporales y estaciones')
#g.set_axis_labels("Escala Temporal (min)", "RMSE (%)", fontsize=30)
#g.add_legend(title='Fuente de Datos', fontsize=30)


# Cambiar las etiquetas de las columnas para mostrar solo el nombre de la estación
for ax in g.axes.flat:
    ax.set_title(ax.get_title().split('=')[1])

#g.fig.suptitle('RMSE(%) para diferentes fuentes de datos, escalas temporales y estaciones', y=1.05)
g.set_axis_labels("Escala Temporal (min)", "RMSE (%)", fontsize=15)
#g.add_legend(title='Fuente de Datos', fontsize=30)
plt.yticks(fontsize=15)
plt.xticks(fontsize=15)
plt.show()





# Gráfico de barras para visualizar el 
#RMAE para cada fuente de datos, escala temporal y estación
df_rmae_melted = df_rmae.melt(id_vars=['time_scale', 'season'], 
                              var_name='Fuente de Datos', 
                              value_name='MAE')

plt.figure(figsize=(14, 8))
sns.barplot(data=df_rmae_melted, x='time_scale', y='MAE', hue='Fuente de Datos', ci=None)
#plt.title('MAE(%) para diferentes fuentes de datos y escalas temporales')
plt.ylabel('MAE(%)', fontsize=30)
plt.xlabel('Escala Temporal (min)', fontsize=30)
plt.legend(title='Fuente de Datos', fontsize=30)
plt.show()

# Gráfico de barras agrupado por estación
g = sns.catplot(data=df_rmae_melted, x='time_scale', y='MAE', hue='Fuente de Datos', col='season', kind='bar', col_wrap=2, ci=None)
# g.fig.suptitle('RRMSD para diferentes fuentes de datos, escalas temporales y estaciones')
g.set_axis_labels("Escala Temporal (min)", "MAE(%)", fontsize=30)
g.add_legend(title='Fuente de Datos', fontsize=30)
plt.show()



# Cambiar las etiquetas de las columnas para mostrar solo el nombre de la estación
for ax in g.axes.flat:
    ax.set_title(ax.get_title().split('=')[1])

#g.fig.suptitle('MAE(%) para diferentes fuentes de datos, escalas temporales y estaciones', y=1.05)
g.set_axis_labels("Escala Temporal (min)", "MAE (%)", fontsize=30)
g.add_legend(title='Fuente de Datos', fontsize=30)
plt.show()



# Gráfico de barras para visualizar el 
#RMBE para cada fuente de datos, escala temporal y estación
df_rmbe_melted = df_rmbe.melt(id_vars=['time_scale', 'season'], 
                              var_name='Fuente de Datos', 
                              value_name='MBE')

plt.figure(figsize=(14, 8))
sns.barplot(data=df_rmbe_melted, x='time_scale', y='MBE', hue='Fuente de Datos', ci=None)
#plt.title('MBE(%) para diferentes fuentes de datos y escalas temporales')
plt.ylabel('MBE(%)', fontsize=30)
plt.xlabel('Escala Temporal (min)', fontsize=30)
plt.legend(title='Fuente de Datos', fontsize=20)
plt.yticks(fontsize=15)
plt.xticks(fontsize=15)
plt.show()





# Gráfico de barras agrupado por estación
g = sns.catplot(data=df_rmbe_melted, x='time_scale', y='MBE', hue='Fuente de Datos', col='season', kind='bar', col_wrap=2, ci=None)
# g.fig.suptitle('RRMSD para diferentes fuentes de datos, escalas temporales y estaciones')
g.set_axis_labels("Escala Temporal (min)", "MBE(%)", fontsize=30)
g.add_legend(title='Fuente de Datos', fontsize=30)
plt.show()



# Cambiar las etiquetas de las columnas para mostrar solo el nombre de la estación
for ax in g.axes.flat:
    ax.set_title(ax.get_title().split('=')[1])

#g.fig.suptitle('MBE(%) para diferentes fuentes de datos, escalas temporales y estaciones', y=1.05)
g.set_axis_labels("Escala Temporal (min)", "MBE (%)", fontsize=30)
g.add_legend(title='Fuente de Datos', fontsize=30)
plt.show()
