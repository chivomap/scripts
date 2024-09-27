import json
import os
from db_connection import get_db_connection

# Obtener la conexión a la base de datos
conn = get_db_connection()
cur = conn.cursor()

# Ruta del archivo donde se guardarán los errores
error_log_path = os.path.join(os.path.dirname(__file__), 'errores_insercion_rutas.txt')

# Crear o limpiar el archivo de errores
with open(error_log_path, 'w') as f:
    f.write("Log de advertencias y errores de inserción de rutas:\n")

# Función para escribir advertencias/errores en el archivo
def log_warning(message):
    with open(error_log_path, 'a') as f:
        f.write("WARNING: " + message + "\n")

# Obtener la ruta del proyecto y la ubicación del archivo GeoJSON
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
geojson_path = os.path.join(project_root, 'data', 'geo', 'geojson', 'Rutas Urbanas.geojson')

# Leer el archivo GeoJSON
with open(geojson_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Diccionarios para mapear los valores del JSON con los de la base de datos
sentido_map = {
    "REGRESO": "Vuelta",
    "Regreso": "Vuelta",
    "IDA": "Ida",
    "Ida": "Ida"
}

# Contadores para el resumen final
inserted_count = 0
skipped_count = 0
warning_count = 0

# Función para obtener el ID de un autobús por su código y número de ruta
def get_bus_id(code_route, number_route):
    query = """
    SELECT id FROM buses WHERE code_route = %s AND number_route = %s
    """
    cur.execute(query, (code_route, number_route))
    result = cur.fetchone()
    return result[0] if result else None

# Función para obtener el ID de la dirección de la ruta (sentido)
def get_direction_id(sentido):
    query = """
    SELECT id FROM direction_routes WHERE name = %s
    """
    cur.execute(query, (sentido,))
    result = cur.fetchone()
    return result[0] if result else None

# Función para verificar si una ruta ya existe en la base de datos
def route_exists(bus_id, direction_id):
    query = """
    SELECT id FROM routes WHERE bus_id = %s AND direction_id = %s
    """
    cur.execute(query, (bus_id, direction_id))
    result = cur.fetchone()
    return result is not None  # Retorna True si la ruta ya existe

# Función para convertir una geometría en formato GeoJSON a WKT (Well-Known Text)
def geometry_to_wkt(geometry):
    geom_type = geometry['type']
    coordinates = geometry['coordinates']

    if geom_type == "LineString":
        # Convertir LineString a WKT
        wkt_geom = 'LINESTRING(' + ', '.join([f'{coord[0]} {coord[1]}' for coord in coordinates]) + ')'
    elif geom_type == "MultiLineString":
        # Convertir MultiLineString a WKT
        wkt_geom = 'MULTILINESTRING('
        wkt_geom += ', '.join(['(' + ', '.join([f'{coord[0]} {coord[1]}' for coord in line]) + ')' for line in coordinates])
        wkt_geom += ')'
    else:
        return None  # Tipo de geometría no soportado

    return wkt_geom

# Procesar los datos de cada característica en el GeoJSON
for feature in data['features']:
    properties = feature['properties']
    
    # Obtener los valores del GeoJSON
    code_route = properties.get("C\u00f3digo_de")
    number_route = properties.get("Nombre_de_")
    sentido = properties.get("SENTIDO")
    geometry = feature.get("geometry")
    
    # Verificar si el autobús existe
    bus_id = get_bus_id(code_route, number_route)
    if not bus_id:
        log_warning(f"El autobús con código de ruta {code_route} y número de ruta {number_route} no se encontró. Saltando inserción de ruta.")
        warning_count += 1
        continue

    # Obtener el ID de la dirección de la ruta (sentido)
    sentido_db = sentido_map.get(sentido)
    direction_id = get_direction_id(sentido_db)
    if not direction_id:
        log_warning(f"No se encontró el ID para el sentido '{sentido_db}' en la ruta {code_route}. Se insertará NULL.")
        direction_id = None
        warning_count += 1

    # Verificar que exista geometría y sea válida
    if not geometry:
        log_warning(f"No se encontró geometría para la ruta {code_route}. Saltando inserción.")
        warning_count += 1
        continue

    # Convertir la geometría a formato WKT
    wkt_geom = geometry_to_wkt(geometry)
    if not wkt_geom:
        log_warning(f"Geometría de tipo {geometry['type']} no soportada para la ruta {code_route}. Saltando inserción.")
        warning_count += 1
        continue

    # Verificar si la ruta ya existe
    if route_exists(bus_id, direction_id):
        print(f"La ruta para el autobús {code_route} y sentido {sentido_db} ya existe. Saltando...")
        skipped_count += 1
        continue

    # Insertar la ruta en la tabla routes
    sql = """
    INSERT INTO routes (bus_id, direction_id, geometry)
    VALUES (%s, %s, ST_GeomFromText(%s, 4326))
    RETURNING id
    """
    try:
        cur.execute(sql, (bus_id, direction_id, wkt_geom))
        route_id = cur.fetchone()[0]  # Obtener el ID de la ruta recién insertada
        print(f"Ruta insertada con ID: {route_id}")
        inserted_count += 1
    except Exception as e:
        error_message = f"Error al insertar la ruta con código {code_route} y número {number_route}: {e}"
        print(error_message)
        log_warning(error_message)
        conn.rollback()
        continue
    
    # Commit de los cambios después de insertar cada ruta
    conn.commit()

# Cerrar la conexión
cur.close()
conn.close()

# Mostrar el resumen final
print("\n--- Resumen de la Operación ---")
print(f"Rutas insertadas: {inserted_count}")
print(f"Rutas saltadas (ya existentes): {skipped_count}")
print(f"Advertencias registradas: {warning_count}")

# Mostrar ruta del archivo de advertencias
print(f"Advertencias registradas en: {error_log_path}")
