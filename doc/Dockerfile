# Usar la imagen oficial de PostgreSQL 16
FROM postgres:16

# Definir variables de entorno para la configuración inicial de PostgreSQL
ENV POSTGRES_USER=myuser
ENV POSTGRES_PASSWORD=mypassword
ENV POSTGRES_DB=mydatabase

# Instalar PostGIS
RUN apt-get update && apt-get install -y postgis postgresql-16-postgis-3 postgresql-16-postgis-3-scripts

# Exponer el puerto 5432 para PostgreSQL
EXPOSE 5432
