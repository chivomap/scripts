# ChivoMap - Script

Documentación de script de transformación y utilidades para trabajar con datos geoespaciales para ChivoMap.

Al día de hoy se ha logrado transofrmar la data geoespacial en shapefile de [VMT](https://www.vmt.gob.sv/transporte-colectivo-en-el-salvador/) para la creación de mapas y rutas de transporte público en El Salvador.


## Estructura del proyecto

- **data-vmt/**: Carpeta que contiene los archivos **Shapefile** organizados en subdirectorios.
  - **Limites departamentales/**: Contiene los archivos `.shp` y sus componentes relacionados para los límites departamentales.
  - **Paradas Transporte Colectivo AMSS/**: Contiene los datos de paradas de transporte colectivo.
  - **Rutas Interdepartamentales/**: Contiene las rutas interdepartamentales.
  - **Rutas Interurbanas/**: Contiene las rutas interurbanas.
  - **Rutas Urbanas/**: Contiene las rutas urbanas.
  - **Transporte Colectivo El Salvador/**: Contiene datos de transporte colectivo en El Salvador.

- **topojson/**: Carpeta donde se almacenan los archivos **TopoJSON** generados a partir de los **Shapefiles**.


## Uso de los scripts

### Requerimientos

- Python 3.x
- Dependencias: 
  - geopandas
  - topojson
  - time

Para instalar las dependencias requeridas:

```bash
pip install -r requirements.txt
```

### Cómo usar el script

1. Clona el repositorio:

   ```bash
   git clone https://github.com/chivomap/scripts.git
   ```

2. Navega al directorio del proyecto:

   ```bash
   cd scripts
   ```

3. Dentro de src/ están los diferentes scripts de transformación de datos geoespaciales:

   ```bash
   python src/properties_geojson.py
   ```

