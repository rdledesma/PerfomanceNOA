import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.patches import Circle

# Coordenadas de los puntos de estudio
salta_coords = (-65.4095, -24.7288)  # (longitud, latitud)
la_quiaca_coords = (-65.60125, -22.1038)  # (longitud, latitud)

# Tamaños de los radios en grados (aproximación)
radius_km = 15  # para CAMS y LSA-SAF
radius_deg = 0.5  # para MERRA-2 y GOES-DSR

# Crear la figura y los ejes con una proyección
fig, ax = plt.subplots(figsize=(10, 10), subplot_kw={'projection': ccrs.PlateCarree()})

# Añadir detalles de tierra y océanos para mapa físico
ax.add_feature(cfeature.LAND, facecolor='lightgray')
ax.add_feature(cfeature.OCEAN, facecolor='lightblue')
ax.add_feature(cfeature.BORDERS, linestyle=':', linewidth=1)
ax.add_feature(cfeature.LAKES, edgecolor='black')
ax.add_feature(cfeature.RIVERS, edgecolor='blue')

ax.set_extent([-67, -64, -26, -21], crs=ccrs.PlateCarree())  # Extensión de mapa para Argentina Norte


plt.show()
