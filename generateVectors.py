#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 10 16:58:10 2024

@author: dario
"""

import pandas as pd 
import cupy as cp
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import numpy as np
import matplotlib.pyplot as plt
import Metrics as m

errors = []

for i in [1,5,15,30,60]:

    d = pd.read_csv(f'process/LQ/{i}.csv')
    d['date'] = pd.to_datetime(d.date)
    
    d['train'] = d.date.dt.year<=2021
    
    
    
    
    d['mak:alpha'] = d.mak * d.alpha
    d['kt:kc'] = d.ktmod * d.kcmod
    d['kt:mak'] =d.ktmod* d.mak 
    d['kc:mak'] = d.ktmod* d.mak 
    
    
    regVars = ['GHI', 'sza', 'mak', 'alpha', 'argp2', 'ghicc', 'ktmod',
           'kcmod', 'kcmodargp',  'mak:alpha', 'kt:kc', 'kt:mak',
           'kc:mak']
    
    
    modelo = LinearRegression()
    scaler = StandardScaler()
    
    
    X = d[d.sza<85].dropna()
    X = X[X.train][regVars]
    X = scaler.fit_transform(X)
    y = d[(d.sza<85) & (d.train)].dropna().ghi
    modelo.fit(X, y)
    
    
    Xtest = d[(~d.train) & (d.sza<85)].dropna()[regVars]
    Xtest = scaler.transform(Xtest)
    
    y_pred   = modelo.predict(Xtest)
    y_true = d[(~d.train) & (d.sza<85)].dropna().ghi
    
    
    
    r = m.rrmsd(y_true, y_pred)
    r = round(r, 2)
    plt.figure()
    plt.title(i)
    plt.plot(y_true, y_pred, '.', label=f"RMSD {r}%", markersize=0.5)
    plt.legend()
    plt.xlabel("GHI Meas")
    plt.xlabel("GHI Adapted")
    plt.show()


    errors.append(r)




# Lista de errores (por ejemplo)


# Crear una lista de índices para representar cada error
indices = range(1, len(errors) + 1)

# Crear un gráfico de barras
plt.bar(indices, errors, tick_label=indices)

# Etiquetas y título
plt.xlabel('Índice del error')
plt.ylabel('Valor del error')
plt.title('Errores')

# Mostrar el gráfico
plt.show()





modelo = LinearRegression()
X = np.array([1,5,15,30,60])
y = errors

modelo.fit(X.reshape(-1, 1), y)


ypred = 23.81  -0.134*X


plt.plot(ypred)


