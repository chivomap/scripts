## **1. Instalación de PostgreSQL y PostGIS**
PostGIS es una extensión de PostgreSQL que agrega soporte para datos geoespaciales. Para instalar PostGIS, primero necesitas tener PostgreSQL instalado en tu sistema.

### **Instalación en Ubuntu/Debian**:
```bash
sudo apt update
sudo apt install postgresql postgis postgresql-16-postgis-3 postgresql-16-postgis-3-scripts
```

### **Instalación en CentOS/RHEL**:
```bash
sudo yum install postgis postgresql16-postgis
```

### **Instalación en macOS**:
```bash
brew install postgis
```

### **Instalación en Docker**:
Si estás utilizando un contenedor de Docker con PostgreSQL, primero accede al contenedor:
```bash
docker exec -it <nombre_contenedor> bash
```

Luego instala PostGIS dentro del contenedor:
```bash
apt update
apt install postgis postgresql-16-postgis-3 postgresql-16-postgis-3-scripts
```

### **Habilitar PostGIS en PostgreSQL**:

1. **Conéctate a la base de datos**:
   ```bash
   psql -U myuser -d mydatabase
   ```

2. **Crear la extensión PostGIS**:
   ```sql
   CREATE EXTENSION postgis;
   ```

3. **Verificar que PostGIS esté habilitado**:
   ```sql
   SELECT PostGIS_Version();
   ```

---

## **2. Creación de una tabla geoespacial con PostGIS**

### **Crear una tabla con columnas geométricas**:
Aquí crearemos una tabla que almacena puntos geoespaciales representando ubicaciones:

```sql
CREATE TABLE lugares (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    ubicacion GEOMETRY(Point, 4326) -- Especifica que esta columna almacenará un punto geográfico
);
```

- **GEOMETRY(Point, 4326)**: Indica que la columna `ubicacion` almacenará puntos en el sistema de coordenadas EPSG:4326 (WGS84, sistema de coordenadas geográficas).

---

## **3. Inserción de datos geoespaciales**

Vamos a insertar datos geoespaciales en la tabla `lugares`. Para esto, usamos la función `ST_GeomFromText` que convierte datos en formato **WKT (Well-Known Text)** en geometrías de **PostGIS**.

### **Ejemplo de inserción**:

```sql
INSERT INTO lugares (nombre, ubicacion)
VALUES ('Parque Central', ST_GeomFromText('POINT(-74.006 40.7128)', 4326));
```

- **POINT(-74.006 40.7128)**: Representa la latitud y longitud de Nueva York (en formato WKT).
- **ST_GeomFromText**: Convierte la representación WKT en un tipo de datos geoespacial que PostGIS entiende.

---

## **4. Consultas geoespaciales con PostGIS**

### **Consulta básica de selección**:

Para obtener todos los lugares y sus coordenadas, simplemente usamos una consulta **SELECT**:

```sql
SELECT id, nombre, ST_AsText(ubicacion) AS coordenadas FROM lugares;
```

- **ST_AsText(ubicacion)**: Convierte la geometría de **PostGIS** de nuevo al formato WKT para que sea más legible.

### **Consulta geoespacial: Encontrar lugares cercanos a un punto**:

Imaginemos que queremos encontrar todos los lugares que están a menos de 10 km de una ubicación específica (por ejemplo, un punto en latitud y longitud):

```sql
SELECT nombre, ST_Distance(ubicacion, ST_GeomFromText('POINT(-74.0059 40.7128)', 4326)) AS distancia
FROM lugares
WHERE ST_DWithin(ubicacion, ST_GeomFromText('POINT(-74.0059 40.7128)', 4326), 10000);
```

- **ST_Distance**: Calcula la distancia entre dos puntos geoespaciales.
- **ST_DWithin**: Verifica si la distancia entre dos geometrías es menor que un valor dado (en este caso, 10,000 metros o 10 km).

---

## **5. Actualización de datos geoespaciales**

Si deseas actualizar las coordenadas de un lugar específico, puedes hacerlo con una consulta **UPDATE**:

```sql
UPDATE lugares
SET ubicacion = ST_GeomFromText('POINT(-74.0059 40.7128)', 4326)
WHERE nombre = 'Parque Central';
```

---

## **6. Otras funciones útiles de PostGIS**

### **1. ST_Contains**:
Verifica si una geometría contiene a otra. Por ejemplo, para saber si un punto está dentro de un polígono:
```sql
SELECT ST_Contains(poligono, punto);
```

### **2. ST_Intersection**:
Devuelve la intersección entre dos geometrías.
```sql
SELECT ST_Intersection(geom1, geom2);
```

### **3. ST_Buffer**:
Crea un área de influencia alrededor de una geometría.
```sql
SELECT ST_Buffer(ubicacion, 1000); -- Crea un buffer de 1000 metros alrededor de "ubicacion"
```

---

## **Resumen de funciones clave de PostGIS**

- **ST_GeomFromText**: Convierte WKT a geometrías PostGIS.
- **ST_AsText**: Convierte geometrías PostGIS a WKT para que sean legibles.
- **ST_Distance**: Calcula la distancia entre dos geometrías.
- **ST_DWithin**: Verifica si dos geometrías están dentro de una cierta distancia.
- **ST_Contains**: Verifica si una geometría contiene a otra.
- **ST_Intersection**: Calcula la intersección de dos geometrías.
- **ST_Buffer**: Crea un área de influencia alrededor de una geometría.

---

Este manual actualizado está optimizado para **PostgreSQL 16** y **PostGIS**.