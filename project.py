import os
import sys

if getattr(sys, 'frozen', False):
    # Estamos ejecutando en un entorno congelado (por ejemplo, creado con PyInstaller)
    class DummyFile:
        def write(self, *args, **kwargs):
            pass

    sys.stdout = DummyFile()
    sys.stderr = DummyFile()

import eel
import socket
from contextlib import closing
import vanity 
import listarunidades 
import qrcodeimagen
import leerqr
import json


def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]

puertoLibre = find_free_port()
TitleName = 'Chainwave'
TitleCore = 'Chainwave'
VersionCore = "1.0.0"
UrlOrganization = ''
IconRoute = 'gui/images/logoblack.ico'
widthInicial = 800
heightInicial = 500
ServerInicial = 'localhost'
PortInicial = puertoLibre
ArchivoInicio = 'index.html'
nombreClaves = 'Key'
nombre_archivo_direccion = 'address.txt'
cantidadDireccionesPorLog =10000


def CallbackProgreso(progreso):
    eel.actualizarProgreso(progreso)

@eel.expose
def process_vanity(is_vanity, prefix1, prefix2, prefix3, tipo, words, max_results,guardar_archivo,gruposMinimos,deCantidad,sobreTotal):
    info = vanity.crearCantidad(int(is_vanity),prefix1,prefix2,prefix3,int(tipo),int(words),int(max_results),int(guardar_archivo),int(gruposMinimos),int(deCantidad),int(sobreTotal),str(nombre_archivo_direccion),CallbackProgreso,cantidadDireccionesPorLog)
    
    return info

@eel.expose
def process_vanity_recover(frase_palabras,gruposMinimos,deCantidad,sobreTotal):
    info = vanity.recuperarBilletera(frase_palabras,int(gruposMinimos),int(deCantidad),int(sobreTotal))
    return info    

@eel.expose
def process_vanity_shamir(array_shamir,gruposMinimos,deCantidad,sobreTotal):
    info = vanity.recuperarBilleteraShamir(str(array_shamir),int(gruposMinimos),int(deCantidad),int(sobreTotal))
    return info 

@eel.expose
def process_vanity_shamir_keys(array_shamir,gruposMinimos,deCantidad,sobreTotal):
    info = vanity.recuperarBilleteraShamirKeys(array_shamir,int(gruposMinimos),int(deCantidad),int(sobreTotal))
    return info 

@eel.expose
def validarUnidadDisponibles():
    info = listarunidades.listingDisk()
    return info 

@eel.expose
def guardarEnUnidadClave(index, phrase, selectedUnit):
    KeyNumber = int(index)+1
    filename = str(nombreClaves)+str(KeyNumber)+'.txt'
    filenameImg = str(nombreClaves)+str(KeyNumber)+'.png'
    phrase = str(phrase)
    content = f"""{phrase}"""
    path = str(selectedUnit)
    escribir = listarunidades.write_to_path(path, filename, content)
    qrImagen = qrcodeimagen.crearImagen(path,phrase,filenameImg) 
    if(escribir=='ok' and qrImagen=='ok'):
        resultado = 'ok'
    else:
        resultado = 'error'    
    return resultado 

@eel.expose
def obtenerKeyUnidadInformacionKey(selectedUnit,arrayClavesActuales):
    info = ''
    lecturaArchivos = listarunidades.find_key_files_in_root(selectedUnit,nombreClaves)
    arrayArchivoFinal = listarunidades.filter_files(lecturaArchivos)

    index = 0
    encontrada = False
    # Procesar el array utilizando un bucle while
    while index < len(arrayArchivoFinal) and encontrada == False:
        # Obtener el archivo actual
        current_file = arrayArchivoFinal[index]
        full_path = os.path.join(selectedUnit, current_file)

        if current_file.endswith('.txt'):
            obtenerClave = listarunidades.read_key_text(full_path) 
            # Realizar operación específica para archivos .txt
        elif current_file.endswith('.png'):
            obtenerClave = leerqr.read_qr_code(full_path)

        if not obtenerClave in arrayClavesActuales:    
            info = obtenerClave
            encontrada = True
        # Incrementar el índice
        index += 1

    return info 

@eel.expose
def obtenerBilleterasIniciales():
    info = listarunidades.leer_address(str(nombre_archivo_direccion))
    info_correcta = info.replace("'", '"')
    wallets_text = info_correcta.strip().split('\n\n')
    
    try:
        wallets_dicts = [json.loads(wallet) for wallet in wallets_text]
    except json.JSONDecodeError as e:
        return []
    
    for wallet in wallets_dicts:
        wallet['legacy']['qr_image'] = qrcodeimagen.ImagenBase64(wallet['legacy']['address'])
        wallet['segwit']['qr_image'] = qrcodeimagen.ImagenBase64(wallet['segwit']['address'])
        wallet['native_segwit']['qr_image'] = qrcodeimagen.ImagenBase64(wallet['native_segwit']['address'])
        wallet['ethereum']['qr_image'] = qrcodeimagen.ImagenBase64(wallet['ethereum']['address'])
        wallet['tron']['qr_image'] = qrcodeimagen.ImagenBase64(wallet['tron']['address'])

    wallets_json = json.dumps(wallets_dicts, indent=4)
    return wallets_dicts

def main():
    eel.init('web')
    eel.start(ArchivoInicio, port=PortInicial, host=ServerInicial, title=TitleCore,size=(widthInicial,heightInicial))


if __name__ == "__main__":
    main()
    

# Crear Instalador 
'''
onedir
pyinstaller --onedir --add-data "web;web" --add-data "wordlist.txt;shamir_mnemonic" --add-data "address.txt;."  --icon="web/images/logoblack.ico" --name Chainwave project.py --noconsole

onefile 
pyinstaller --onefile --add-data "web;web" --add-data "wordlist.txt;shamir_mnemonic" --add-data "address.txt;."  --icon="web/images/logoblack.ico" --name Chainwave project.py --noconsole


'''
