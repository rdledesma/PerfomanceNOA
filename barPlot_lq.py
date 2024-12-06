import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt





# Crear un DataFrame con los datos de RMSE para las distintas escalas temporales
data_rmse = {
    'Escala Temporal': ['10'] * 7 + ['15'] * 7 + ['60'] * 7,
    'Fuente': [ 'ERA-5', 'CAMS', 'NSRDB', 'G-CIM', 'LSA-SAF','MERRA-2','DSR']*3,
    'RMSE': [0,0, 19.3,19.9,0,0,0, 
             0,27.4, 18.1,18.5, 24,0,0,
             22.2,23.3, 13.2, 12.6 , 19.4, 22, 20.5]
}

# Convertir los datos en un DataFrame
df_rmse = pd.DataFrame(data_rmse)

# Graficar usando Seaborn
plt.figure(figsize=(10, 6))
sns.barplot(x='Escala Temporal', y='RMSE', hue='Fuente', data=df_rmse,palette='Set2')
plt.ylabel('RMSE (%)', fontsize=20)
plt.xlabel('Temporal Res (min).', fontsize=20)
plt.legend(title='', fontsize=10, ncol=10, 
           loc="upper center", )
plt.grid()
plt.show()



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
    "gc": [9.8, 10.2, 10.2, 11.3, 11.3, 14.0, 17.2, 24.4],
    "ns": [10.7, 10.8, 10.0, 10.0, 10.0, 13.0, 16.5, 23.2],
    "ca": [19.0, 19.0, 18.4, 17.3, 18.8, 24.2, 33.8, 46.2],
    "ls": [17.4, 17.0, 16.2, 16.3, 15.9, 18.8, 23.1, 29.0],
    "er": [20.8, 21.8, 19.3, 18.8, 17.0, 20.7, 23.1, 27.0],
    "me": [19.5, 20.4, 18.3, 18.6, 17.8, 20.6, 25.6, 31.2],
    "dsr": [19.8, 19.5, 17.0, 18.5, 18.4, 21.6, 29.3, 45.5]
}


df = pd.DataFrame(data)


df.columns = ['Rango SZA',"G-CIM","NSRDB", "CAMS", "LSA-SAF", "ERA-5", "MERRA-2", "DSR"]

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


