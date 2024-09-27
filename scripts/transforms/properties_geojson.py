"""
Este script permite al usuario seleccionar un archivo GeoJSON de una carpeta y luego muestra las propiedades de los features en el archivo.
"""
import os
import json

# Función para listar los archivos GeoJSON en la carpeta y permitir seleccionar uno
def elegir_archivo_geojson(geojson_dir):
    archivos = [f for f in os.listdir(geojson_dir) if f.endswith('.geojson')]
    if not archivos:
        print("No se encontraron archivos GeoJSON en la carpeta.")
        return None

    # Mostrar una lista numerada de los archivos
    print("Selecciona un archivo GeoJSON para leer:")
    for i, archivo in enumerate(archivos, 1):
        print(f"{i}. {archivo}")

    # Elegir el archivo basándose en el número
    while True:
        try:
            eleccion = int(input("Elige un número: ")) - 1
            if 0 <= eleccion < len(archivos):
                return os.path.join(geojson_dir, archivos[eleccion])
            else:
                print("Número fuera de rango. Intenta de nuevo.")
        except ValueError:
            print("Entrada no válida. Por favor, ingresa un número.")

# Función para leer las propiedades de los features en el archivo seleccionado
def mostrar_propiedades(archivo_geojson):
    with open(archivo_geojson, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Verificar si el archivo es un FeatureCollection y tiene features
    if data.get("type") == "FeatureCollection" and "features" in data:
        propiedades = data["features"][0]["properties"].keys()
        print("\nPropiedades disponibles en los features:")
        for i, prop in enumerate(propiedades, 1):
            print(f"{i}. {prop}")

        return list(propiedades)
    else:
        print("El archivo no tiene el formato esperado de FeatureCollection.")
        return None

# Función para obtener los valores únicos de una propiedad seleccionada
def obtener_valores_unicos(archivo_geojson, propiedad):
    with open(archivo_geojson, 'r', encoding='utf-8') as f:
        data = json.load(f)

    valores_unicos = set()

    for feature in data["features"]:
        valor = feature["properties"].get(propiedad)
        if valor is not None:
            valores_unicos.add(valor)

    return list(valores_unicos)

# Ruta de la carpeta con los archivos GeoJSON
geojson_dir = '/home/devel/dev/ch1vo/rutas-vmt/data/geo/geojson'

# Paso 1: Elegir archivo GeoJSON
archivo_geojson = elegir_archivo_geojson(geojson_dir)
if archivo_geojson:
    # Paso 2: Mostrar las propiedades de los features
    propiedades = mostrar_propiedades(archivo_geojson)

    if propiedades:
        # Paso 3: Elegir una propiedad
        while True:
            try:
                eleccion_prop = int(input("Elige una propiedad por número: ")) - 1
                if 0 <= eleccion_prop < len(propiedades):
                    propiedad_elegida = propiedades[eleccion_prop]
                    break
                else:
                    print("Número fuera de rango. Intenta de nuevo.")
            except ValueError:
                print("Entrada no válida. Por favor, ingresa un número.")

        # Paso 4: Obtener los valores únicos de la propiedad elegida
        valores_unicos = obtener_valores_unicos(archivo_geojson, propiedad_elegida)
        print(f"\nValores únicos de la propiedad '{propiedad_elegida}':")
        for valor in valores_unicos:
            print(valor)
else:
    print("No se pudo procesar ningún archivo.")
