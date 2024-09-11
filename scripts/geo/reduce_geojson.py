"""
Este script reduce la estructura de los archivos GeoJSON en una carpeta, manteniendo solo un ejemplo de cada array.
"""
import os
import json

# Función para reducir la estructura JSON, manteniendo un solo ejemplo de cada array
def reduce_structure(data):
    if isinstance(data, dict):
        # Procesa cada clave en el diccionario
        return {key: reduce_structure(value) for key, value in data.items()}
    elif isinstance(data, list):
        # Si es una lista, dejar solo el primer elemento (si existe)
        return [reduce_structure(data[0])] if len(data) > 0 else []
    else:
        # Si es un valor no iterable, devolver el valor real
        return data

# Directorio donde están los archivos geojson
geojson_dir = 'geojson'
output_dir = 'geojson_min'  # Directorio para guardar los archivos con estructura reducida

# Crear el directorio de salida si no existe
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Recorrer todos los archivos en la carpeta geojson
for filename in os.listdir(geojson_dir):
    if filename.endswith('.geojson'):
        file_path = os.path.join(geojson_dir, filename)

        # Leer el contenido del archivo GeoJSON
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Reducir la estructura del JSON
        reduced_data = reduce_structure(data)

        # Guardar el archivo reducido en el directorio de salida
        output_file_path = os.path.join(output_dir, filename)
        with open(output_file_path, 'w', encoding='utf-8') as f_out:
            json.dump(reduced_data, f_out, indent=2)

        print(f"Estructura reducida creada para: {filename}")
