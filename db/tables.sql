-- Table: roles
CREATE TABLE roles (
  id SERIAL PRIMARY KEY,
  role_name VARCHAR(255)
);

-- Table: users
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255),
  google_id VARCHAR(255),
  email VARCHAR(255),
  image_url VARCHAR(255),
  role_id INT REFERENCES roles(id)
);

-- Table: departments
CREATE TABLE departments (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255),
  geometry GEOMETRY(Polygon, 4326),  -- Representa el área geopolítica del departamento
  area_km DECIMAL(10, 2),            -- Área en kilómetros cuadrados
  perimeter_km DECIMAL(10, 2),       -- Perímetro en kilómetros
  "order" INT                        -- Orden específico del departamento
);

-- Table: type_buses
CREATE TABLE type_buses (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255)
);

-- Table: subtype_buses
CREATE TABLE subtype_buses (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255)
);

-- Table: terminals
CREATE TABLE terminals (
  id SERIAL PRIMARY KEY,
  direction VARCHAR(255),
  terminal_name VARCHAR(255),
  location GEOMETRY(Point, 4326),  -- Representa la ubicación del terminal
  photo_url VARCHAR(255)
);

-- Table: buses
CREATE TABLE buses (
  id SERIAL PRIMARY KEY,
  number_route VARCHAR(255),
  code_route VARCHAR(255),
  has_special BOOLEAN,
  fees DOUBLE PRECISION,
  special_fees DOUBLE PRECISION,
  first_trip TIMESTAMP,
  last_trip TIMESTAMP,
  frequency INTERVAL,
  approx_travel_time INTERVAL,
  photo_url VARCHAR(255),
  type_id INT REFERENCES type_buses(id),
  subtype_id INT REFERENCES subtype_buses(id),
  terminal_id INT REFERENCES terminals(id),
  department_id INT REFERENCES departments(id)
);

-- Table: direction_routes
CREATE TABLE direction_routes (
  id SERIAL PRIMARY KEY,
  direction_name VARCHAR(255),
  time_range VARCHAR(255)
);

-- Table: routes
CREATE TABLE routes (
  id SERIAL PRIMARY KEY,
  bus_id INT REFERENCES buses(id),
  direction_id INT REFERENCES direction_routes(id),
  geometry GEOMETRY(LineString, 4326)  -- Representa la ruta de los autobuses
);

-- Table: detours
CREATE TABLE detours (
  id SERIAL PRIMARY KEY,
  route_id INT REFERENCES routes(id),
  reason VARCHAR(255),
  geometry GEOMETRY(LineString, 4326),
  start_date DATE,
  end_date DATE
);

-- Table: stops
CREATE TABLE stops (
  id SERIAL PRIMARY KEY,
  stop_name VARCHAR(255),
  direction VARCHAR(255),
  location GEOMETRY(Point, 4326),  -- Representa la ubicación geoespacial de la parada
  photo_url VARCHAR(255)
);

-- Table: bus_stops
CREATE TABLE bus_stops (
  id SERIAL PRIMARY KEY,
  bus_id INT REFERENCES buses(id),
  stop_id INT REFERENCES stops(id)
);

-- Table: fav_routes
CREATE TABLE fav_routes (
  id SERIAL PRIMARY KEY,
  route_id INT REFERENCES routes(id),
  user_id INT REFERENCES users(id)
);
