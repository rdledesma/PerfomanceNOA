import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


[ 'ERA-5', 'CAMS', 'NSRDB', 'G-CIM', 'LSA-SAF','MERRA-2','DSR']


# Crear un DataFrame con los datos de RMSE para las distintas escalas temporales
data_rmse = {
    'Escala Temporal': ['10'] * 7 + ['15'] * 7 + ['60'] * 7,
    'Fuente': [ 'ERA-5', 'CAMS', 'NSRDB', 'G-CIM', 'LSA-SAF','MERRA-2','DSR']*3,
    'RMSE': [0,0,20.3, 21.5,0,0,0, 
             0,31.1,19.1, 20.7, 32.6,0,0,
             32.6,26.7,15.5 , 16, 28.5, 48.8, 35.4]
}

# Convertir los datos en un DataFrame
df_rmse = pd.DataFrame(data_rmse)

# # Graficar usando Seaborn
# plt.figure(figsize=(10, 6))
# sns.barplot(x='Escala Temporal', y='RMSE', hue='Fuente', data=df_rmse,palette='Set2')
# plt.ylabel('RMSE (%)', fontsize=20)
# plt.xlabel('Temporal Res (min).', fontsize=20)
# plt.legend(title='', fontsize=20, ncol=7, 
#            loc="upper center", )
# plt.grid()
# plt.show()



# Convertir los datos en un DataFrame
df_rmse = pd.DataFrame(data_rmse)

plt.figure(figsize=(10, 6))
# Graficar un gráfico de barras
ax = sns.barplot(x='Escala Temporal', y='RMSE', hue='Fuente', data=df_rmse, palette='Paired')

# Remover los palitos (ticks) del eje x
ax.tick_params(length=0,labelsize=14)

plt.ylabel('RMSE (%)', fontsize=20)
plt.xlabel('Temporal Res (min).', fontsize=20)
# plt.title('RMSE por Fuente y Escala Temporal', fontsize=16)
plt.legend(title='', fontsize=12, ncol=7, 
           loc="upper center", )
plt.grid(True)

plt.tight_layout()
plt.show()












import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# Crear el dataframe con los datos
data = {
    "Rango SZA": ["0-10", "10-20", "20-30", "30-40", "40-50", "50-60", "60-70", "70-80"],
    "ns": [13.7, 11.9, 11.2, 12.1, 12.4, 17.4, 24.3, 43.4],
    "gc": [9.0, 9.9, 12.5, 11.5, 12.2, 11.9, 14.8, 30.7],
    "ca": [22.6, 23.0, 19.3, 20.3, 22.4, 27.8, 36.3, 51.5],
    "ls": [26.0, 25.7, 21.3, 22.5, 23.8, 28.3, 32.6, 48.7],
    "er": [29.4, 26.8, 25.1, 27.0, 30.0, 32.1, 35.1, 43.4],
    "me": [37.0, 36.4, 35.0, 41.0, 46.9, 46.9, 59.7, 81.7],
    "dsr": [25.0, 24.1, 20.3, 21.6, 21.6, 26.1, 36.3, 67.7]
}


df = pd.DataFrame(data)


df.columns = ['Rango SZA',"G-CIM","NSRDB",  "CAMS", "LSA-SAF", "ERA-5", "MERRA-2", "DSR"]

# Configurar el gráfico
fig, ax = plt.subplots(figsize=(10, 6))

# Definir ancho de las barras y posiciones para cada grupo
ancho_barra = 0.1
rango_posiciones = np.arange(len(df["Rango SZA"]))

# Usar colores de la paleta 'Paired'
palette = sns.color_palette("Paired", len(data) - 1)  # Usamos len(data)-1 para los modelos (sin la columna 'Rango SZA')

# Graficar cada modelo dentro de cada rango SZA
modelos =[ 'ERA-5', 'CAMS', 'NSRDB', 'G-CIM', 'LSA-SAF','MERRA-2','DSR']
for i, modelo in enumerate(modelos):
    posiciones = rango_posiciones + i * ancho_barra
    ax.bar(posiciones, df[modelo], width=ancho_barra, label=modelo, color=palette[i])



# Etiquetas y formato del gráfico
ax.set_xlabel("SZA(°) range", fontsize=20)
ax.set_ylabel("RMSE (%)",fontsize=20)
#ax.set_title("RMSE por Modelo y Rango SZA")
ax.set_xticks(rango_posiciones + ancho_barra * 3)
ax.set_xticklabels(df["Rango SZA"])
plt.legend(title='', fontsize=12, ncol=7, 
           loc="upper center", )
plt.grid(linewidth=0.5)
# Mostrar gráfico
plt.show()


