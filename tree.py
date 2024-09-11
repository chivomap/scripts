import os

def print_directory_tree(startpath, indent=''):
    for root, dirs, files in os.walk(startpath):
        # Filtrar carpetas que empiezan con '.'
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        # Obtener el nivel de profundidad del directorio
        level = root.replace(startpath, '').count(os.sep)
        
        # Crear la indentación para mostrar las carpetas
        indent = ' ' * 4 * level
        print(f"{indent}{os.path.basename(root)}/")
        
        # Imprimir archivos con una indentación adicional
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print(f"{subindent}{f}")

# Define el directorio raíz que deseas explorar
start_directory = '.'  # Directorio actual o puedes cambiarlo a cualquier ruta

# Imprimir la estructura de carpetas
print_directory_tree(start_directory)
