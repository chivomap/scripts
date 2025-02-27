import json
import os
from db_connection import get_db_connection

# Obtener la conexión a la base de datos
conn = get_db_connection()
cur = conn.cursor()

# Ruta del archivo donde se guardarán los errores
error_log_path = os.path.join(os.path.dirname(__file__), 'errores_insercion_buses.txt')

# Crear o limpiar el archivo de errores
with open(error_log_path, 'w') as f:
    f.write("Log de advertencias y errores de inserción de autobuses:\n")

# Función para escribir advertencias/errores en el archivo
def log_warning(message):
    with open(error_log_path, 'a') as f:
        f.write("WARNING: " + message + "\n")

# Obtener la ruta del proyecto y la ubicación del archivo GeoJSON
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
geojson_path = os.path.join(project_root, 'data', 'geo', 'geojson', 'Rutas Interdepartamentales.geojson')

# Leer el archivo GeoJSON
with open(geojson_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Diccionarios para mapear los valores del JSON con los de la base de datos
tipo_bus_map = {
    "POR AUTOBUS": "AutoBus",
    "POR MICROBUS": "MicroBus",
    "POR MICROBUSES": "MicroBus",
}

sentido_map = {
    "REGRESO": "Regreso",
    "Regreso": "Regreso",
    "IDA": "Ida",
    "Ida": "Ida"
}

subtipo_bus_map = {
    "INTERDEPARTAMENTAL": "Interdepartamental",
    "URBANO": "Urbano",
    "INTERURBANO": "Interurbano"
}

# Contadores para el resumen final
inserted_count = 0
skipped_count = 0
warning_count = 0

# Función para obtener el ID de una tabla por su nombre
def get_id_by_name(table, column, value):
    query = f"SELECT id FROM {table} WHERE {column} = %s"
    cur.execute(query, (value,))
    result = cur.fetchone()
    return result[0] if result else None

# Función para verificar si un autobús ya existe en la base de datos
def bus_exists(code_route, number_route):
    query = """
    SELECT id FROM buses WHERE code_route = %s AND number_route = %s
    """
    cur.execute(query, (code_route, number_route))
    result = cur.fetchone()
    return result is not None  # Retorna True si el autobús existe

# Procesar los datos de cada característica en el GeoJSON
for feature in data['features']:
    properties = feature['properties']
    
    # Obtener los valores del GeoJSON
    code_route = properties.get("C\u00f3digo_de")
    number_route = properties.get("Nombre_de_")
    sentido = properties.get("SENTIDO")
    tipo = properties.get("TIPO")
    subtype = properties.get("SUBTIPO")
    department = properties.get("DEPARTAMEN")
    
    # Mapeo de valores
    tipo_bus_db = tipo_bus_map.get(tipo)
    sentido_db = sentido_map.get(sentido)
    subtype_bus_db = subtipo_bus_map.get(subtype)
    
    # Verificar si el autobús ya existe
    if bus_exists(code_route, number_route):
        print(f"El autobús con código de ruta {code_route} y número de ruta {number_route} ya existe. Saltando...")
        skipped_count += 1
        continue
    
    # Obtener los IDs de las tablas relacionadas o registrar advertencia si no se encuentra
    tipo_id = get_id_by_name("type_buses", "name", tipo_bus_db)
    if not tipo_id:
        log_warning(f"No se encontró el ID para el tipo de bus '{tipo_bus_db}' en la ruta {code_route}. Se insertará NULL.")
        tipo_id = None
        warning_count += 1

    subtype_id = get_id_by_name("subtype_buses", "name", subtype_bus_db)
    if not subtype_id:
        log_warning(f"No se encontró el ID para el subtipo de bus '{subtype_bus_db}' en la ruta {code_route}. Se insertará NULL.")
        subtype_id = None
        warning_count += 1

    department_id = get_id_by_name("departments", "name", department)
    if not department_id:
        log_warning(f"No se encontró el ID para el departamento '{department}' en la ruta {code_route}. Se insertará NULL.")
        department_id = None
        warning_count += 1
    
    # Insertar el autobús en la tabla buses
    sql = """
    INSERT INTO buses (number_route, code_route, type_id, subtype_id, department_id)
    VALUES (%s, %s, %s, %s, %s)
    RETURNING id
    """
    try:
        cur.execute(sql, (number_route, code_route, tipo_id, subtype_id, department_id))
        bus_id = cur.fetchone()[0]  # Obtener el ID del autobús recién insertado
        print(f"Autobús insertado con ID: {bus_id}")
        inserted_count += 1
    except Exception as e:
        error_message = f"Error al insertar el autobús con código {code_route} y número {number_route}: {e}"
        print(error_message)
        log_warning(error_message)
        conn.rollback()
        continue
    
    # Commit de los cambios después de insertar cada autobús
    conn.commit()

# Cerrar la conexión
cur.close()
conn.close()

# Mostrar el resumen final
print("\n--- Resumen de la Operación ---")
print(f"Autobuses insertados: {inserted_count}")
print(f"Autobuses saltados (ya existentes): {skipped_count}")
print(f"Advertencias registradas: {warning_count}")

# Mostrar ruta del archivo de advertencias
print(f"Advertencias registradas en: {error_log_path}")
