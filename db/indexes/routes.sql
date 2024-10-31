CREATE INDEX routes_geometry_idx
ON routes
USING GIST (geometry);
