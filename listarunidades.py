import platform
#import psutil
#import subprocess
import win32api
import os
import re

def list_windows_drives():
    """Lista las unidades en Windows."""
    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split('\000')[:-1]  # Divide por null terminator y elimina el último elemento vacío
    return drives
'''
def list_linux_partitions():
    """Lista las particiones en Linux."""
    partitions = psutil.disk_partitions()
    partition_list = []
    for partition in partitions:
        partition_list.append({
            'device': partition.device,
            'mountpoint': partition.mountpoint,
            'fstype': partition.fstype
        })
    return partition_list

def list_macos_volumes():
    """Lista los volúmenes en macOS."""
    # Ejecuta el comando 'diskutil list' y captura la salida
    result = subprocess.run(['diskutil', 'list'], stdout=subprocess.PIPE, text=True)
    volumes = result.stdout.splitlines()
    return volumes
'''
def listingDisk():
    system = platform.system()
    if system == 'Windows':
        #print("Estás en Windows")
        return list_windows_drives()
    else:
        #print(f"Sistema operativo no reconocido: {system}")
        return []
    '''    
    elif system == 'Linux':
        #print("Estás en Linux")
        return list_linux_partitions()
    elif system == 'Darwin':
        #print("Estás en macOS")
        return ist_macos_volumes()
    '''       

def write_to_path(path, filename, content):
    """Escribe un archivo de texto en la ruta especificada."""
    # Construye la ruta del archivo
    file_path = os.path.join(path, filename)    
    try:
        # Escribe el contenido en el archivo
        with open(file_path, 'w') as file:
            file.write(content)
        return 'ok'
    except Exception as e:
        #print(f"Error al escribir en el archivo: {e}")    
        return 'error'    

def find_key_files_in_root(drive_letter,nameKeys):
    """Encuentra archivos en la raíz de la unidad especificada que comiencen con 'Key' en su nombre y los retorna como un array."""
    key_files = []
    
    try:
        # Recorre todos los elementos en la raíz de la unidad especificada
        for filename in os.listdir(drive_letter):
            # Verifica si el nombre del archivo comienza con 'Key'
            #print(filename)
            file_path = os.path.join(drive_letter, filename)
            # Asegúrate de que sea un archivo y no una carpeta
            if os.path.isfile(file_path):
                if filename.lower().startswith(nameKeys.lower()):
                    key_files.append(filename)
        return key_files
    except Exception as e:
        # En caso de error, retorna un array vacío o maneja el error según sea necesario
        return []




def filter_files(file_list):
    # Extraer los números únicos de los nombres de archivo
    numbers = set()
    for file in file_list:
        match = re.search(r'(\d+)', file)
        if match:
            numbers.add(int(match.group(1)))
    
    # Crear un set para almacenar los nombres de archivos `.txt`
    txt_files = set()
    for file in file_list:
        if file.endswith('.txt'):
            match = re.search(r'(\d+)', file)
            if match:
                txt_files.add(int(match.group(1)))
    
    # Filtrar los archivos `.png` si existe un `.txt` correspondiente
    result_files = []
    for file in file_list:
        if file.endswith('.png'):
            match = re.search(r'(\d+)', file)
            if match:
                number = int(match.group(1))
                if number not in txt_files:
                    result_files.append(file)
        else:
            result_files.append(file)
    
    return result_files    

def read_key_text(file_path):
    """Lee el contenido de un archivo de texto y retorna el contenido."""
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return 'Error: El archivo no se encuentra.'
    except Exception as e:
        return f'Error: {e}'    

def leer_address(nombreArchivoDireccion):
    archivo = nombreArchivoDireccion   
    if os.path.exists(archivo):
        with open(archivo, 'r') as f:
            contenido = f.read()
        return contenido
    else:
        return ''