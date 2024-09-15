# Cómo generar una clave SSH y usarla en tu servidor

En esta guía rápida, aprenderemos a generar una clave SSH en Windows y cómo usarla para conectarnos a un servidor VPS. ¡Súper útil si eres nuevo en DevOps!

## 1. Abrir PowerShell

Primero, vamos a abrir **PowerShell** en modo administrador.

1. Ve al menú de inicio y busca "PowerShell".
2. Haz clic derecho y selecciona **Ejecutar como administrador**.

## 2. Generar la clave SSH

Ahora, vamos a crear la clave SSH usando un simple comando:

```bash
ssh-keygen
```

Te pedirá que elijas una ubicación para guardar la clave. La ruta por defecto es algo como `C:\Users\TuUsuario\.ssh\id_rsa`. Si ya tienes una clave con ese nombre, puedes hacer una de dos cosas:

- **No sobrescribir la clave existente**: Escribe `n` para no sobrescribirla.
- **Crear una nueva clave**: Escribe un nombre diferente, por ejemplo, `id_rsa_kedan`.

También te pedirá que pongas una frase de contraseña. Esto es opcional, pero si no quieres una, simplemente presiona **Enter**.

## 3. Verificar que la clave fue creada

Para verificar que la clave fue creada correctamente, puedes ir a la ruta donde la guardaste, o correr este comando en PowerShell:

```bash
ls ~/.ssh
```

Deberías ver los archivos `id_rsa` (la clave privada) y `id_rsa.pub` (la clave pública). Si usaste un nombre diferente, verás algo como `id_rsa_kedan` y `id_rsa_kedan.pub`.

## 4. Ver tu clave pública

La clave pública es lo que compartirás con los servidores para poder conectarte. Para verla, puedes usar este comando:

```bash
cat C:\Users\eliseo\.ssh\id_rsa_kedan.pub
```

Esto te mostrará el contenido de tu clave pública, que se verá algo como esto:

```
ssh-rsa AAAAB3NzaC1yc2EAAAADAQAB... eliseo@DESKTOP-GFGRG4H
```
## 5. Conectar a tu servidor VPS con la clave SSH
> IMPORTANTE: Si ya pegaste tu clave pública en el servidor, salta a este paso)  
 
> Ejemplo pudiste hacerlo con digital ocean, craendo el droplet y pegando la clave publica en el servidor

### Paso 1: Copia la clave pública al servidor (si no lo has hecho ya)

1. En tu VPS, necesitas asegurarte de que tu clave pública (la que terminaba en `.pub`) esté en el archivo `authorized_keys` en el servidor. Para eso, sigue estos pasos:

2. **Si puedes conectarte a tu VPS con contraseña**: Ingresa con tu usuario, probablemente `root`, así:
   ```bash
   ssh root@138.197.200.62
   ```

3. Una vez dentro del servidor, asegúrate de que haya una carpeta `.ssh` en tu directorio de usuario (normalmente `~` o `/root`):
   ```bash
   mkdir -p ~/.ssh
   ```

4. Luego, edita o crea el archivo `authorized_keys` donde pegarás tu clave pública:
   ```bash
   nano ~/.ssh/authorized_keys
   ```

5. Ahora, en tu computadora local, abre tu **clave pública** que generaste (en este caso `id_rsa_kedan.pub`). Usa este comando en tu PowerShell o CMD para verla:
   ```bash
   cat C:\Users\eliseo\.ssh\id_rsa_kedan.pub
   ```

6. Copia el contenido que aparece en pantalla.

7. Regresa a tu VPS y pega la clave pública copiada dentro del archivo `authorized_keys`.

8. Guarda el archivo (`Ctrl + O` para guardar y luego `Ctrl + X` para salir del editor nano).

### Paso 2: Ajusta los permisos en el servidor

Para que funcione correctamente, asegúrate de que los permisos de la carpeta `.ssh` y el archivo `authorized_keys` estén configurados correctamente:

```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```

### Paso 3: Conéctate a tu VPS desde tu computadora usando la clave SSH

1. En tu computadora local, abre **PowerShell** o el **CMD**.

2. Usa este comando para conectarte a tu VPS usando la clave privada que generaste (la que termina en `id_rsa_kedan`):

   ```bash
   ssh -i C:\Users\eliseo\.ssh\id_rsa_kedan root@138.197.200.62
   ```

   - `-i C:\Users\eliseo\.ssh\id_rsa_kedan`: Especifica el archivo de clave privada.
   - `root@138.197.200.62`: Es tu nombre de usuario (`root` en este caso) y la IP pública de tu VPS.

3. Si todo está configurado correctamente, te conectará sin pedir contraseña.

### Resumen

- **Generaste una clave SSH.**
- **Copiaste la clave pública a tu servidor en el archivo `authorized_keys`.**
- **Te conectas usando la clave privada desde tu computadora con `ssh -i`.**

Prueba estos pasos y si te encuentras con algún error o algo no queda claro, ¡dímelo y lo resolveremos!