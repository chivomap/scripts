

# Tratamiento y Análisis de Rutas de Buses Mediante Grafos en ChivoMap

## Introducción

El objetivo de este documento es explicar el proceso de conversión de datos de rutas de buses, que están disponibles a nivel nacional en formato GeoJSON, en un grafo. Este grafo permite analizar la red de transporte, incluso cuando algunas rutas no cuentan con paradas definidas (como sucede fuera de la capital). Además, se detalla cómo, al consultar rutas en el grafo, se puede identificar si la conexión se estableció mediante paradas reales, por proximidad o a partir del cruce (intersección) de rutas.

## 1. Datos Disponibles

- **Rutas Nacionales en GeoJSON:**  
  Se dispone de la geometría de las rutas de buses en todo el país en formato GeoJSON, las cuales pueden estar representadas como **LineString** o **MultiLineString**.

- **Paradas Definidas en la Capital:**  
  Solo para la capital se cuenta con la ubicación exacta de las paradas. Estas paradas se consideran nodos fijos y confiables en el grafo.

## 2. Conversión de Rutas a Grafo

### 2.1 Extracción de Nodos y Aristas

- **Nodos:**  
  - **Paradas Reales:** Los puntos que definen las paradas en la capital se convierten en nodos con metadatos que indican su origen (p.ej., `tipo: parada_real`).
  - **Puntos Geométricos Clave:** Para las rutas sin paradas definidas, se extraen puntos clave (inicio, fin y puntos de inflexión) que sirven como nodos provisionales.
  - **Intersecciones:** Se identifican los puntos donde se cruzan dos o más rutas. Estos puntos pueden definirse como nodos de intersección.

- **Aristas:**  
  Cada segmento entre dos nodos se define como una arista. La arista puede tener atributos que indiquen:
  - **Origen de Conexión:**  
    - `parada`: si la conexión se da entre dos paradas reales.
    - `proximidad`: si se infiere una conexión debido a que dos nodos (aunque no sean paradas reales) están dentro de un umbral de distancia predefinido.
    - `intersección`: si la conexión se establece en un punto donde dos rutas se cruzan.
  - **Longitud y otros atributos geoespaciales.**

### 2.2 Conexión por Proximidad (Snapping)

Cuando se dispone de rutas sin paradas:
- **Definición del Umbral:**  
  Se establece una distancia umbral (por ejemplo, 50 metros) para determinar si dos puntos en la red pueden conectarse.
- **Proceso de Snapping:**  
  Los nodos extraídos de la geometría se “ajustan” o agrupan si están dentro de este umbral, creando conexiones que simulan una parada o una intersección.
- **Metadatos:**  
  Las aristas resultantes de este proceso se etiquetan con `tipo: proximidad`, lo que permite distinguirlas de las conexiones directas por paradas reales.

### 2.3 Herramientas y Librerías

Para llevar a cabo estos procesos se pueden utilizar:
- **Shapely:**  
  Para el manejo y análisis de geometrías, identificación de intersecciones y cálculo de distancias.
- **GeoPandas:**  
  Para gestionar y transformar los datos geoespaciales de manera eficiente.
- **NetworkX:**  
  Para construir el grafo a partir de nodos y aristas, y realizar análisis de rutas.

## 3. Consulta e Identificación de Conexiones en el Grafo

Una vez construido el grafo, las consultas de rutas (por ejemplo, para obtener el camino más corto entre dos puntos) deben permitir identificar el tipo de conexión en cada segmento. Esto se puede lograr mediante:

### 3.1 Incorporación de Metadatos en el Grafo

- **Atributos en Nodos y Aristas:**  
  Cada nodo y arista incluirá un atributo `tipo` que indica si proviene de:
  - **`parada_real`** (nodos provenientes de paradas definidas)
  - **`proximidad`** (conexiones inferidas mediante snapping)
  - **`intersección`** (nodos creados en el cruce de rutas)
  
- **Documentación Interna:**  
  Se debe mantener una descripción clara en la documentación del proyecto sobre qué significa cada atributo y cómo se calculó.

### 3.2 Ejemplo de Consulta

Al realizar una consulta en el grafo, el resultado puede devolver una secuencia de nodos y aristas. Por ejemplo:

```python
# Pseudocódigo para consulta en NetworkX
ruta = nx.shortest_path(grafo, source=node_inicio, target=node_fin, weight='longitud')

for i in range(len(ruta)-1):
    arista = grafo.get_edge_data(ruta[i], ruta[i+1])
    print(f"Conexión de {ruta[i]} a {ruta[i+1]}: {arista['tipo']}")
```

En este ejemplo, la salida indicará para cada segmento si la conexión fue establecida por:
- **Paradas reales:** Conexión directa entre paradas existentes.
- **Proximidad:** Conexión inferida por cercanía de nodos.
- **Cruce:** Conexión establecida en intersecciones de rutas.

### 3.3 Interpretación de Resultados

Al revisar los resultados de la consulta, se pueden tomar decisiones o mostrar información adicional:
- **Visualización Diferenciada:**  
  Al representar la ruta en un mapa, se puede usar diferentes colores o estilos de línea para cada tipo de conexión.
- **Análisis de Calidad de la Ruta:**  
  Determinar si una ruta que utiliza muchas conexiones por proximidad es menos confiable o requiere validación adicional.
- **Optimización y Ajuste:**  
  Si se observa que un alto porcentaje de conexiones se realiza por proximidad, se puede revisar el umbral de distancia o considerar la inclusión de datos adicionales para mejorar la precisión.

## 4. Conclusiones

Este enfoque permite:
- **Integrar Rutas de Todo el País:**  
  Aunque solo se tengan paradas definidas en la capital, es posible generar un grafo que conecte la red completa mediante nodos derivados de la geometría.
- **Flexibilidad en la Conexión:**  
  Las conexiones se pueden establecer tanto por datos reales (paradas) como por métodos de inferencia (proximidad o intersección), garantizando una red lo más completa posible.
- **Consultas Enriquecidas:**  
  Al incluir metadatos en cada conexión, las consultas en el grafo permiten identificar el origen de cada segmento, facilitando análisis posteriores y la toma de decisiones basadas en la calidad o tipo de conexión.

Este documento ofrece una guía integral para transformar datos de rutas en un grafo robusto, permitiendo un análisis avanzado de la red de buses y facilitando la identificación de conexiones por su origen. Con el uso de herramientas de geoprocesamiento y análisis de grafos, se abre la posibilidad de optimizar rutas y mejorar la gestión del transporte público en un entorno geoespacial complejo.

