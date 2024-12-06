import pandas as pd
import matplotlib.pyplot as plt 
import Metrics as m



med = 623.0
site = 'lq'
for f in [60]:
    freq = f
    d = pd.read_csv(f'measured/LQ/{site}_{freq}.csv')
    d['date'] = pd.to_datetime(d.date)
    print(d.ghi.mean())
    
gc = pd.read_csv(f'CIM/LQ/{site}_{freq}_mc.csv')
ca = pd.read_csv(f'cams/LQ/{site}_{freq}.csv')
ds = pd.read_csv(f'DSR/LQ/{site}_{freq}.csv')
ls = pd.read_csv(f'LSA-SAF/LQ/{site}_{freq}.csv')
ns= pd.read_csv(f'nsrdb/LQ/{site}_{freq}.csv')

er = pd.read_csv(f'era5/LQ/{site}_{freq}.csv')
me = pd.read_csv(f'MERRA-2/LQ/{site}_{freq}.csv')



d['date'] = pd.to_datetime(d.date)
ns['date'] = pd.to_datetime(ns.date)
ca['date'] = pd.to_datetime(ca.date)
ds['date'] = pd.to_datetime(ds.date)
ls['date'] = pd.to_datetime(ls.date)
gc['date'] = pd.to_datetime(gc.date)
er['date'] = pd.to_datetime(er.date)
me['date'] = pd.to_datetime(me.date)

# plt.figure()
# plt.plot(d.ghi.values)
# plt.plot( ns.ghi.values, label="NSRDB")
# plt.plot(gc.ghi.values, label="G-CIM")

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

ns = (ns.set_index('date')
      .reindex(dates)
      .rename_axis(['date'])
      #.fillna(0)
      .reset_index())


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




d['ghins'] = ns.ghi.values
d['ghica'] = ca.ghi.values
d['ghils'] = ls.ghi.values
d['ghigc'] = gc.ghi.values
d['ghids'] = ds.DSRras.values
d['ghier'] = er.ghi.values
d['ghime'] = me.ghi.values



s = d.dropna()
s = s[s.sza<80]
s = s[(s.ghi / s.argp)<1.3]


true = s.ghi
pred = s.ghime


m.mbe(true, pred) / med * 100
m.mae(true, pred) / med * 100
m.rmsd(true, pred) / med * 100
m.KSI_OVER(true, pred) / med * 100
m.SS4(true, pred)






s['kc'] = s.ghi / s.argp
s = s.sort_values(by=['sza'])

s['n'] = s.date.dt.dayofyear

import numpy as np

s['group'] = np.nan


for i in np.arange(0, 80, 10):
    ds = s[(s.sza>=i) & (s.sza<i+10)]
    # print(ds.ghi.mean())
    print(m.rrmsd(ds.ghi, ds.ghime))
    
    
    
    



# Crear una nueva columna para los grupos de SZA
bins = list(range(0, 100, 10))
labels = [f'{i}-{i+10}' for i in range(0, 90, 10)]
s['sza_group'] = pd.cut(s['sza'], bins=bins, labels=labels, right=False)

rrmsd_results = []

for sza_group in s['sza_group'].unique():
    df_group = s[s['sza_group'] == sza_group]
    true = df_group.ghi
    predHeliosat = df_group['ghica']
    predNSRDB = df_group['ghins']
    predDSR = df_group['ghids']
    predMerra = df_group['ghime']
    predEra = df_group['ghier']
    predLsa = df_group['ghils']
    predcim = df_group['ghigc']
    rrmsd_results.append({
        'sza_group': sza_group,
        'Heliosat-4': m.rrmsd(true, predHeliosat),
        'NSRDB': m.rrmsd(true, predNSRDB),
        'GCIM': m.rrmsd(true, predcim),
        'GOES DSR': m.rrmsd(true, predDSR),
        'MERRA-2': m.rrmsd(true, predMerra),
        'ERA-5': m.rrmsd(true, predEra),
        'LSA-SAF': m.rrmsd(true, predLsa)
    })

import seaborn as sns
# Convertir rrmsd_results en un DataFrame para visualización
df_rmsd = pd.DataFrame(rrmsd_results)

# df_rmsd['NSRDB'] = 0

df_rmsd = df_rmsd[['sza_group','ERA-5', 'Heliosat-4','NSRDB',
                   'GCIM','LSA-SAF', 'MERRA-2','GOES DSR',]]



#df_rmsd = df_rmsd[['sza_group', 'NSRDB', 'GCIM','Heliosat-4' ]]


# Gráfico de barras para visualizar el RRMSD para cada fuente de datos en cada escala temporal
df_rmsd_melted = df_rmsd.melt(id_vars=['sza_group'], 
                              var_name='Fuente de Datos', value_name='RRMSD')

plt.figure(figsize=(14, 8))
sns.barplot(data=df_rmsd_melted,
            x='sza_group',
            y='RRMSD',
            hue='Fuente de Datos',
            palette='Paired')
#plt.title(f'RRMSD {f} mins')
plt.ylabel('RMSE (%)', fontsize=20)
plt.xlabel('SZA (°)', fontsize=20)
plt.legend(title='', fontsize=10, ncol=6, 
           loc="upper center", )
plt.grid()
plt.show()



    
    