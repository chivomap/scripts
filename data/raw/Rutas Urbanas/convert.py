import geopandas as gpd
from scripts.geo.sh_to_topo import Topology
import time

# Medir el tiempo total
start_time = time.time()

# Cargar el shapefile utilizando geopandas
shapefile_path = "Rutas Urbanas.shp"
start_load = time.time()
gdf = gpd.read_file(shapefile_path)
end_load = time.time()
print(f"Paso 1: Shapefile cargado en {end_load - start_load:.2f} segundos")

# Reproyectar a WGS84 (EPSG:4326)
start_reproject = time.time()
gdf = gdf.to_crs(epsg=4326)
end_reproject = time.time()
print(f"Paso 2: Shapefile reproyectado a WGS84 en {end_reproject - start_reproject:.2f} segundos")

# Convertir a GeoJSON (formato intermedio)
start_geojson = time.time()
geojson = gdf.to_json()
end_geojson = time.time()
print(f"Paso 3: Conversión a GeoJSON completada en {end_geojson - start_geojson:.2f} segundos")

# Crear una topología con la librería topojson
start_topo = time.time()
topo = Topology(geojson)
end_topo = time.time()
print(f"Paso 4: Topología creada en {end_topo - start_topo:.2f} segundos")

# Guardar el resultado como TopoJSON
start_save = time.time()
topojson_output_path = "output_file2.topojson"
with open(topojson_output_path, "w") as f:
    f.write(topo.to_json())
end_save = time.time()
print(f"Paso 5: Archivo TopoJSON guardado en {end_save - start_save:.2f} segundos")

# Tiempo total
total_time = time.time() - start_time
print(f"Proceso completo en {total_time:.2f} segundos")
