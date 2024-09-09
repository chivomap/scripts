import os
import geopandas as gpd
from topojson import Topology
import time

# Definir el directorio de salida para los archivos TopoJSON
output_dir = "topojson"

# Crear el directorio de salida si no existe
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Función para convertir un archivo Shapefile a TopoJSON
def convert_shapefile_to_topojson(shapefile_path, output_dir):
    file_name = os.path.splitext(os.path.basename(shapefile_path))[0]  # Nombre sin extensión

    # Medir el tiempo total de procesamiento del archivo
    start_time = time.time()

    # Cargar el Shapefile utilizando geopandas
    start_load = time.time()
    gdf = gpd.read_file(shapefile_path)
    end_load = time.time()
    print(f"Paso 1: Shapefile '{shapefile_path}' cargado en {end_load - start_load:.2f} segundos")

    # Verificar el CRS (sistema de referencia de coordenadas)
    print(f"CRS original: {gdf.crs}")

    # Reproyectar a WGS84 (EPSG:4326) si no está en el sistema correcto
    if gdf.crs != "EPSG:4326":
        start_reproject = time.time()
        gdf = gdf.to_crs(epsg=4326)
        end_reproject = time.time()
        print(f"Paso 2: Shapefile reproyectado a WGS84 en {end_reproject - start_reproject:.2f} segundos")
    else:
        print("No es necesario reproyectar, ya está en WGS84")

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

    # Guardar el resultado como TopoJSON, usando el mismo nombre del archivo de entrada
    start_save = time.time()
    topojson_output_path = os.path.join(output_dir, f"{file_name}.topojson")
    with open(topojson_output_path, "w") as f:
        f.write(topo.to_json())
    end_save = time.time()
    print(f"Paso 5: Archivo TopoJSON guardado como '{topojson_output_path}' en {end_save - start_save:.2f} segundos")

    # Tiempo total de procesamiento del archivo
    total_time = time.time() - start_time
    print(f"Conversión completa para '{file_name}' en {total_time:.2f} segundos\n")

# Función para buscar archivos Shapefile en todos los subdirectorios de una carpeta
def find_and_convert_shapefiles(start_dir):
    total_start_time = time.time()  # Tiempo de inicio global
    for root, dirs, files in os.walk(start_dir):
        for file in files:
            if file.endswith(".shp"):
                shapefile_path = os.path.join(root, file)
                print(f"Convirtiendo archivo: {shapefile_path}")
                convert_shapefile_to_topojson(shapefile_path, output_dir)
    
    total_end_time = time.time()  # Tiempo final global
    print(f"Proceso completo para todos los archivos en {total_end_time - total_start_time:.2f} segundos")

if __name__ == "__main__":
    # Directorio de búsqueda (data-vmt)
    data_vmt_dir = "data-vmt"

    # Verificar si la carpeta data-vmt existe
    if not os.path.exists(data_vmt_dir):
        print(f"Error: No se encontró la carpeta '{data_vmt_dir}'")
    else:
        print(f"Buscando archivos Shapefile en '{data_vmt_dir}' y subdirectorios...")

        # Buscar y convertir todos los archivos Shapefile dentro de data-vmt
        find_and_convert_shapefiles(data_vmt_dir)
