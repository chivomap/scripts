```json
{
  "type": "FeatureCollection",
  "name": "Rutas Interdepartamentales",
  "crs": {
    "type": "name",
    "properties": {
      "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
    }
  },
  "features": [
    {
      "type": "Feature",
      "properties": {
        "C\u00f3digo_de": "AB202A0AH", // buses.code_route
        "Nombre_de_": "202-A", // buses.number_route
        "SENTIDO": "IDA", // routes.direction_id (hay una tabla direction_routes)
        "TIPO": "POR AUTOBUS", // buses.type_route
        "SUBTIPO": "INTERDEPARTAMENTAL", // buses.subtype_route
        "DEPARTAMEN": "AHUACHAPAN", // buses.departament_id 
        "Kil\u00f3metro": "93.9116153540628", // 
        "CANTIDAD_D": 1,
        "Shape_Leng": 93905.6840846
      },
      "geometry": {
        "type": "LineString",
        "coordinates": [
          [
            -89.84495759380023
          ]
        ]
      }
    }
  ]
}
```