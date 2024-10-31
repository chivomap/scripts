import json
import os
from db_connection import get_db_connection

# Obtener la conexión
conn = get_db_connection()
cur = conn.cursor()

# Obtener la ruta de la raíz del proyecto
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))

# Construir la ruta relativa desde la raíz del proyecto
geojson_path = os.path.join(project_root, 'data', 'geo',  'geojson', 'LIM DEPARTAMENTALES.geojson')

# Leer el archivo GeoJSON
with open(geojson_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Función para construir el WKT de un MultiPolygon
def create_multipolygon_wkt(coordinates):
    wkt = 'MULTIPOLYGON('
    for multipolygon in coordinates:
        wkt += '('
        for polygon in multipolygon:
            wkt += '('
            wkt += ', '.join([f'{point[0]} {point[1]}' for point in polygon])
            wkt += ')'
        wkt += '), '
    wkt = wkt.rstrip(', ')  # Eliminar la última coma
    wkt += ')'
    return wkt

# Función para construir el WKT de un Polygon
def create_polygon_wkt(coordinates):
    wkt = 'POLYGON('
    for polygon in coordinates:
        wkt += '('
        wkt += ', '.join([f'{point[0]} {point[1]}' for point in polygon])
        wkt += '), '
    wkt = wkt.rstrip(', ')  # Eliminar la última coma
    wkt += ')'
    return wkt

# Insertar datos de cada departamento
for feature in data['features']:
    name = feature['properties']['NA2']
    
    # Ignorar "ZONAS DE FRONTERAS"
    if name == "ZONAS DE FRONTERAS":
        print(f"Ignorando el departamento: {name}")
        continue
    
    area_km = feature['properties']['AREA_KM']
    perimeter_km = feature['properties']['PERIMETRO']
    
    # Manejo del campo 'NA3' para 'sort_order'
    sort_order_value = feature['properties']['NA3']
    try:
        sort_order = int(sort_order_value) if sort_order_value.isdigit() else None  # Si no es numérico, se asigna None
    except ValueError:
        sort_order = None

    # Convertir la geometría en formato WKT
    geometry_type = feature['geometry']['type']
    coordinates = feature['geometry']['coordinates']
    
    # Inicializar wkt_geom
    wkt_geom = None

    # Si es MultiPolygon
    if geometry_type == 'MultiPolygon':
        wkt_geom = create_multipolygon_wkt(coordinates)
    
    # Si es Polygon
    elif geometry_type == 'Polygon':
        wkt_geom = create_polygon_wkt(coordinates)

    # Imprimir el nombre y la geometría en WKT antes de la inserción
    print(f"Procesando departamento: {name}")
    print(f"WKT generado: {wkt_geom}")

    # Asegurarse de que wkt_geom esté definido
    if wkt_geom:
        # Insertar en la tabla
        sql = """
        INSERT INTO departments (name, geometry, area_km, perimeter_km, sort_order)
        VALUES (%s, ST_GeomFromText(%s, 4326), %s, %s, %s)
        """
        try:
            cur.execute(sql, (name, wkt_geom, area_km, perimeter_km, sort_order))
        except Exception as e:
            print(f"Error al insertar el departamento: {name}")
            print(f"Error: {e}")
            conn.rollback()  # Hacer rollback si ocurre un error
    else:
        print(f"No se pudo procesar la geometría para el departamento: {name}")

# Confirmar cambios y cerrar conexión
conn.commit()
cur.close()
conn.close()
