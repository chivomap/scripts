# ChivoMap Rutas - VMT

Este repositorio tiene el objetivo de documentar el proceso de extracción de infomración de [VMT](https://www.vmt.gob.sv/transporte-colectivo-en-el-salvador/) para la creación de mapas y rutas de transporte público en El Salvador.


## Estructura del proyecto

- **data-vmt/**: Carpeta que contiene los archivos **Shapefile** organizados en subdirectorios.
  - **Limites departamentales/**: Contiene los archivos `.shp` y sus componentes relacionados para los límites departamentales.
  - **Paradas Transporte Colectivo AMSS/**: Contiene los datos de paradas de transporte colectivo.
  - **Rutas Interdepartamentales/**: Contiene las rutas interdepartamentales.
  - **Rutas Interurbanas/**: Contiene las rutas interurbanas.
  - **Rutas Urbanas/**: Contiene las rutas urbanas.
  - **Transporte Colectivo El Salvador/**: Contiene datos de transporte colectivo en El Salvador.

- **topojson/**: Carpeta donde se almacenan los archivos **TopoJSON** generados a partir de los **Shapefiles**.

- **main.py**: Script principal que realiza la conversión de los **Shapefiles** a **TopoJSON**.

## Uso del script

### Requerimientos

- Python 3.x
- Dependencias: 
  - geopandas
  - topojson
  - time

Para instalar las dependencias requeridas:

```bash
pip install geopandas topojson
```

### Cómo usar el script

1. Clona el repositorio:

   ```bash
   git clone https://github.com/kedatech/rutas-vmt.git
   ```

2. Navega al directorio del proyecto:

   ```bash
   cd rutas-vmt
   ```

3. Ejecuta el script **main.py**. Esto buscará todos los archivos **Shapefile** en la carpeta `data-vmt` y convertirá cada uno de ellos a **TopoJSON**, guardando los resultados en la carpeta `topojson`.

   ```bash
   python main.py
   ```

4. El script imprimirá mensajes en la consola sobre el progreso de la conversión, incluyendo el tiempo que toma cada conversión individual y el tiempo total para convertir todos los archivos.

### Ejemplo de ejecución

```bash
$ python main.py
Buscando archivos Shapefile en 'data-vmt' y subdirectorios...
Convirtiendo archivo: data-vmt/Limites departamentales/LIM DEPARTAMENTALES.shp
Paso 1: Shapefile 'LIM DEPARTAMENTALES.shp' cargado en 0.32 segundos
CRS original: EPSG:4326
No es necesario reproyectar, ya está en WGS84
Paso 3: Conversión a GeoJSON completada en 0.71 segundos
Paso 4: Topología creada en 3.75 segundos
Paso 5: Archivo TopoJSON guardado como 'topojson/LIM DEPARTAMENTALES.topojson' en 0.30 segundos
Conversión completa para 'LIM DEPARTAMENTALES' en 5.09 segundos
```
