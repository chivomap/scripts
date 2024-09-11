-- 1. Table: roles
CREATE TABLE roles (
  id SERIAL PRIMARY KEY,
  role_name VARCHAR(255)
);

-- 2. Table: users
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255),
  google_id VARCHAR(255),
  email VARCHAR(255),
  image_url VARCHAR(255),
  role_id INT REFERENCES roles(id)
);

-- 3. Table: departments
CREATE TABLE departments (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255),
  geometry GEOMETRY(MultiPolygon, 4326),  -- Representa el área geopolítica del departamento
  area_km DECIMAL(10, 2),            -- Área en kilómetros cuadrados
  perimeter_km DECIMAL(10, 2),       -- Perímetro en kilómetros
  "order" INT                        -- Orden específico del departamento
);

-- 4. Table: type_buses
CREATE TABLE type_buses (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255)                   -- Tipo de bus (ej. Autobús, Microbus)
);

-- 5. Table: subtype_buses
CREATE TABLE subtype_buses (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255)                   -- Subtipo de bus (ej. Urbano, Interdepartamental)
);

-- 6. Table: terminals
CREATE TABLE terminals (
  id SERIAL PRIMARY KEY,
  direction VARCHAR(255),                   -- Dirección del terminal (ej. Norte, Sur)
  terminal_name VARCHAR(255),               -- Nombre del terminal
  location GEOMETRY(Point, 4326),           -- Ubicación del terminal
  photo_url VARCHAR(255)                    -- URL de la foto del terminal
);

-- 7. Table: buses
CREATE TABLE buses (
  id SERIAL PRIMARY KEY,
  number_route VARCHAR(255),          -- Número de ruta del autobús
  code_route VARCHAR(255),            -- Código de la ruta
  has_special BOOLEAN,                -- Indica si tiene rutas especiales
  fees DOUBLE PRECISION,              -- Tarifa normal
  special_fees DOUBLE PRECISION,      -- Tarifa especial
  first_trip TIMESTAMP,               -- Hora del primer viaje
  last_trip TIMESTAMP,                -- Hora del último viaje
  frequency INTERVAL,                 -- Frecuencia del viaje (ej. cada 10 min)
  approx_travel_time INTERVAL,        -- Tiempo aproximado de viaje
  photo_url VARCHAR(255),             -- URL de la foto del autobús
  type_id INT REFERENCES type_buses(id),      -- Relación con el tipo de bus
  subtype_id INT REFERENCES subtype_buses(id),-- Relación con el subtipo de bus
  terminal_id INT REFERENCES terminals(id),   -- Relación con la terminal de salida
  department_id INT REFERENCES departments(id) -- Relación con el departamento
);

-- 8. Table: direction_routes
CREATE TABLE direction_routes (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255)                   -- Nombre de la dirección (ej. IDA, VUELTA)
);

-- 9. Table: routes
CREATE TABLE routes (
  id SERIAL PRIMARY KEY,
  bus_id INT REFERENCES buses(id),          -- Relación con el autobús
  direction_id INT REFERENCES direction_routes(id),  -- Relación con la dirección de la ruta
  geometry GEOMETRY(LineString, 4326)       -- Representa la geometría de la ruta
);

-- 10. Table: stops
CREATE TABLE stops (
  id SERIAL PRIMARY KEY,
  stop_name VARCHAR(255),                   -- Nombre de la parada
  direction VARCHAR(255),                   -- Dirección (ej. IDA, VUELTA)
  location GEOMETRY(Point, 4326),           -- Ubicación de la parada (coordenadas)
  photo_url VARCHAR(255)                    -- URL de la foto de la parada
);

-- 11. Table: bus_stops
CREATE TABLE bus_stops (
  id SERIAL PRIMARY KEY,
  bus_id INT REFERENCES buses(id),          -- Relación con el autobús
  stop_id INT REFERENCES stops(id)          -- Relación con la parada
);

-- 12. Table: detours
CREATE TABLE detours (
  id SERIAL PRIMARY KEY,
  route_id INT REFERENCES routes(id),       -- Relación con la ruta
  reason VARCHAR(255),                      -- Razón del desvío
  geometry GEOMETRY(LineString, 4326),      -- Geometría del desvío
  start_date DATE,                          -- Fecha de inicio del desvío
  end_date DATE                             -- Fecha de finalización del desvío
);

-- 13. Table: fav_routes
CREATE TABLE fav_routes (
  id SERIAL PRIMARY KEY,
  route_id INT REFERENCES routes(id),       -- Relación con la ruta
  user_id INT REFERENCES users(id)          -- Relación con el usuario que ha marcado la ruta como favorita
);
