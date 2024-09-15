### ¿Qué hacer ahora?
Lo siguiente sería configurar Nginx para que sirva tu propia página HTML o sitio web en lugar de la página de bienvenida. Te explico cómo hacerlo.

### Paso 1: Crear una página HTML propia

1. Crea un directorio donde almacenarás tu sitio web:
   ```bash
   sudo mkdir -p /var/www/kedan.tech/html
   ```

2. Cambia los permisos para poder modificarlo fácilmente:
   ```bash
   sudo chown -R $USER:$USER /var/www/kedan.tech/html
   ```

3. Crea un archivo `index.html` dentro del directorio:
   ```bash
   nano /var/www/kedan.tech/html/index.html
   ```

4. Escribe el contenido de tu página HTML. Por ejemplo:
   ```html
   <html>
   <head>
       <title>Kedan.tech</title>
   </head>
   <body>
       <h1>¡Bienvenido a Kedan.tech!</h1>
   </body>
   </html>
   ```

5. Guarda y cierra el archivo (`Ctrl + O`, luego `Enter`, y después `Ctrl + X`).

### Paso 2: Configurar Nginx para tu dominio

1. Crea un archivo de configuración para tu sitio:
   ```bash
   sudo nano /etc/nginx/sites-available/kedan.tech
   ```

2. Agrega la siguiente configuración para que Nginx sepa cómo servir tu sitio:
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

3. Guarda y cierra el archivo.

### Paso 3: Activar la configuración del sitio

1. Crea un enlace simbólico del archivo de configuración en `sites-available` hacia `sites-enabled`:
   ```bash
   sudo ln -s /etc/nginx/sites-available/kedan.tech /etc/nginx/sites-enabled/
   ```

2. Verifica que la configuración de Nginx sea correcta:
   ```bash
   sudo nginx -t
   ```

3. Si todo está bien, reinicia Nginx para aplicar los cambios:
   ```bash
   sudo systemctl restart nginx
   ```

### Paso 4: Actualizar tu DNS

Si aún no lo has hecho, asegúrate de que el dominio `kedan.tech` apunte a la IP de tu VPS, ya que en este momento solo podrás acceder mediante la IP. Si ya tienes el DNS configurado, entonces deberías poder acceder a tu sitio visitando `http://kedan.tech`.
