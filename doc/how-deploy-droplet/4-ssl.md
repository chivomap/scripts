# Instalar un certificado SSL en Nginx con Let's Encrypt

### **Resumen de pasos**:
1. Verifica los registros DNS para `kedan.tech` y `www.kedan.tech`.
2. Instala **Certbot** y el plugin para **Nginx**.
3. Configura Nginx para servir el contenido en el puerto 80.
4. Usa Certbot para obtener el certificado SSL.
5. Verifica que el sitio funcione con HTTPS.
6. Configura la renovación automática con Certbot.

### **Paso 1: Verificar registros DNS**
Antes de instalar el certificado, asegúrate de que los registros DNS estén configurados correctamente para tu dominio.

1. **Acceder a tu panel de DNS en DigitalOcean**:
   - Ve a la sección de DNS en DigitalOcean.
   - Asegúrate de tener un **registro A** para:
     - `kedan.tech` → Apunta a la dirección IP de tu servidor (por ejemplo, `64.11.228.6`).
     - `www.kedan.tech` → Apunta a la **misma IP** que `kedan.tech`.

2. **Crear el registro A (si no lo tienes)**:
   - En el panel de control de DNS en DigitalOcean, selecciona "Create new record" y elige **A record**.
   - En el campo **Hostname**, escribe:
     - **@** para `kedan.tech`.
     - **www** para `www.kedan.tech`.
   - En el campo **Will direct to**, selecciona la dirección IP de tu servidor (por ejemplo, `64.23.228.6`).
   - Deja el **TTL** en 3600 segundos (1 hora).
   
3. **Esperar a que se propague**:
   - La propagación de DNS puede tardar entre unos minutos y 24-48 horas. Puedes verificar el estado de tus DNS con herramientas como [What's My DNS](https://www.whatsmydns.net).

### **Paso 2: Instalar Certbot y Nginx plugin**
1. Asegúrate de que tu sistema está actualizado:
   ```bash
   sudo apt update
   sudo apt upgrade
   ```

2. Instala **Certbot** y el plugin de **Nginx**:
   ```bash
   sudo apt install certbot python3-certbot-nginx
   ```

### **Paso 3: Configurar Nginx**
Antes de solicitar el certificado, asegúrate de que Nginx esté correctamente configurado para tu dominio.

1. Abre el archivo de configuración de Nginx para tu dominio:
   ```bash
   sudo nano /etc/nginx/sites-available/kedan.tech
   ```

2. Asegúrate de que el bloque de tu servidor esté escuchando en el puerto 80 (HTTP) y que apunte a tu dominio:
   ```nginx
   server {
       listen 80;
       server_name kedan.tech www.kedan.tech;

       root /var/www/kedan.tech/html;
       index index.html;

       location / {
           try_files $uri $uri/ =404;
       }
   }
   ```

3. Guarda y cierra el archivo (`Ctrl + O` para guardar, `Ctrl + X` para salir).

4. Verifica la configuración de Nginx:
   ```bash
   sudo nginx -t
   ```

5. Reinicia Nginx:
   ```bash
   sudo systemctl restart nginx
   ```

### **Paso 4: Solicitar el certificado SSL**
Ahora que todo está listo, usa Certbot para solicitar el certificado SSL.

1. Ejecuta el siguiente comando para solicitar el certificado para ambos dominios `kedan.tech` y `www.kedan.tech`:
   ```bash
   sudo certbot --nginx -d kedan.tech -d www.kedan.tech
   ```

   - Si no tienes el subdominio `www`, puedes ejecutar el comando solo para `kedan.tech`:
     ```bash
     sudo certbot --nginx -d kedan.tech
     ```

2. Sigue las indicaciones:
   - **Correo electrónico**: Introduce tu correo para recibir notificaciones.
   - **Aceptar los términos del servicio**.
   - Opción para compartir tu correo con la EFF (opcional, puedes aceptar o rechazar).
   
3. Certbot hará automáticamente los cambios en Nginx para habilitar HTTPS y redirigir el tráfico HTTP a HTTPS.

### **Paso 5: Verificar la instalación**
Una vez completado, visita tu sitio web en el navegador para confirmar que el certificado SSL está funcionando:

- Visita **https://kedan.tech** (y **https://www.kedan.tech** si lo configuraste).
- Deberías ver un candado de seguridad en la barra de direcciones, lo que indica que el certificado SSL está activo y funcionando.

### **Paso 6: Configurar la renovación automática**
Los certificados SSL de Let's Encrypt caducan cada 90 días, pero Certbot puede renovarlos automáticamente.

1. Para asegurarte de que la renovación automática está configurada, ejecuta:
   ```bash
   sudo certbot renew --dry-run
   ```

   Este comando prueba el proceso de renovación sin realizar cambios reales.

### **Paso 7: Verificar el estado de Nginx**
Finalmente, puedes verificar que Nginx esté funcionando correctamente después de los cambios:

```bash
sudo systemctl status nginx
```

### **Problemas comunes y soluciones**:
- **DNS no propagado**: Si Let's Encrypt te dice que no puede verificar el dominio, asegúrate de que los registros DNS se hayan propagado correctamente.
- **Error de permisos**: Si Nginx no puede acceder a ciertos archivos, asegúrate de que el directorio raíz de tu dominio tenga los permisos correctos.
