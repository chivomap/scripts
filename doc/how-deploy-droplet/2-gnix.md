
# Cómo instalar Nginx en Ubuntu 20.04

### Resumen:
- Actualiza tu sistema.
- Instala Nginx.
- Verifica que Nginx esté corriendo.
- Configura el firewall (si es necesario).
- Verifica Nginx en tu navegador.

### Paso 1: Actualizar el sistema
Antes de instalar cualquier paquete, es una buena práctica asegurarse de que tu sistema esté actualizado.

1. Conéctate a tu VPS (si no lo has hecho ya).
   
2. Luego, actualiza los paquetes instalados en tu sistema ejecutando:

   ```bash
   sudo apt update
   sudo apt upgrade
   ```

### Paso 2: Instalar Nginx
1. Ahora instala Nginx con el siguiente comando:

   ```bash
   sudo apt install nginx
   ```

2. Confirma la instalación cuando se te pida.

### Paso 3: Verificar el estado de Nginx
Una vez que Nginx esté instalado, puedes verificar si está corriendo correctamente con este comando:

```bash
sudo systemctl status nginx
```

Deberías ver algo como "active (running)", lo que significa que el servicio Nginx está activo y funcionando.

### Paso 4: Configurar el firewall (opcional)
Si tienes un firewall habilitado en tu VPS, debes permitir el tráfico HTTP (puerto 80) y HTTPS (puerto 443) para Nginx. Aquí están los comandos si usas `ufw` (Uncomplicated Firewall):

1. Para permitir tráfico HTTP:

   ```bash
   sudo ufw allow 'Nginx HTTP'
   ```

2. Si también quieres permitir HTTPS (para un certificado SSL en el futuro):

   ```bash
   sudo ufw allow 'Nginx Full'
   ```

### Paso 5: Probar Nginx en tu navegador
1. Abre tu navegador y escribe la dirección IP de tu VPS (`http://64.23.228.6`, por ejemplo).
   
2. Si todo está correcto, deberías ver la página de bienvenida de Nginx que dice **"Welcome to Nginx!"**.

---
