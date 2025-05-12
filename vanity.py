import mnemonicphrases
import argparse

def guardar_en_archivo(nombre_archivo, contenido):
    with open(nombre_archivo, 'a') as archivo:
        archivo.write(contenido + '\n')

def generate_vanity_address2(tipobusqueda ,prefix,prefix2,prefix3,palabras,gruposMinimos,deCantidad,sobreTotal,callback,cantidadDireccionesPorLog):
    conteo =0

    if(tipobusqueda==1):
        if not(prefix.startswith('1') and prefix2.startswith('1') and prefix3.startswith('1')):
            return 'Error Recuerda que legacy inicia con 1'
            
    elif(tipobusqueda==2):
        if not (prefix.startswith('3') and prefix2.startswith('3') and prefix3.startswith('3')):
            return 'Error Recuerda que segwit inicia con 3'
            
    elif(tipobusqueda==3):
        if not (prefix.startswith('bc') and prefix2.startswith('bc') and prefix3.startswith('bc')):
            return 'Error Recuerda que native_segwit inicia con bc'  
                       
    else:
        return 'Error: Tipo de búsqueda no válido.'

    while True:
        conteo = conteo+1
        walletInfo = mnemonicphrases.crearDireccion(palabras,gruposMinimos,deCantidad,sobreTotal)
        if conteo % cantidadDireccionesPorLog == 0:
            #print(f'{conteo} direcciones')
            callback(conteo)                
        if tipobusqueda==1:
            #legacy 
            if (walletInfo['legacy']['address'].startswith(prefix) or walletInfo['legacy']['address'].startswith(prefix2) or walletInfo['legacy']['address'].startswith(prefix3)):
                return walletInfo
        elif tipobusqueda==2:
            #segwit 
            if (walletInfo['segwit']['address'].startswith(prefix) or walletInfo['segwit']['address'].startswith(prefix2) or walletInfo['segwit']['address'].startswith(prefix3)):
                return walletInfo   
        elif tipobusqueda==3:
            #native_segwit 
            if (walletInfo['native_segwit']['address'].startswith(prefix) or walletInfo['native_segwit']['address'].startswith(prefix2) or walletInfo['native_segwit']['address'].startswith(prefix3)):
                return walletInfo       
        
def crearBilleteraDireccion(desired_prefix,desired_prefix2,desired_prefix3,tipoBusqueda,palabras,guardar_archivo,gruposMinimos,deCantidad,sobreTotal,nombreArchivoDireccion,callback,cantidadDireccionesPorLog):
    # Configura el prefijo que deseas
    #1: legacy, #2:segwit, #3:native_segwit
    informacionWallet = generate_vanity_address2(tipoBusqueda,desired_prefix,desired_prefix2,desired_prefix3,palabras,gruposMinimos,deCantidad,sobreTotal,callback,cantidadDireccionesPorLog)

    if guardar_archivo ==1:
        informacionWalletAlmacenar = {
        "legacy": {
            "address": informacionWallet['legacy']['address']
        },
        "segwit": {
            "address": informacionWallet['segwit']['address']
        },
        "native_segwit": {
            "address": informacionWallet['native_segwit']['address']
        },
        "ethereum": {
            "address": informacionWallet['ethereum']['address']
        },
        "tron": {
            "address": informacionWallet['tron']['address']
        }
    }

        contenido = f"""{informacionWalletAlmacenar}\n"""
        # Guardar en archivo
        guardar_en_archivo(nombreArchivoDireccion, contenido)
    
    return informacionWallet


def recuperarBilletera(seed_phrase,gruposMinimos,deCantidad,sobreTotal):
    infoRecover = mnemonicphrases.recuperarWallet(seed_phrase,gruposMinimos,deCantidad,sobreTotal)
    return infoRecover

def recuperarBilleteraShamir(array_shamir,gruposMinimos,deCantidad,sobreTotal):
    
    # Paso 1: Eliminar los saltos de línea y espacios extras si los hubiera
    cadena = array_shamir.replace("\n", "").replace("'", "").strip()

    # Paso 2: Separar los elementos por comas
    array = array_shamir.split(",")

    # Paso 3: Eliminar espacios adicionales al inicio o fin de cada elemento (opcional)
    array_shamir_final = [element.strip() for element in array]
    

    infoRecover = mnemonicphrases.recuperarWalletShamir(array_shamir_final,gruposMinimos,deCantidad,sobreTotal)
    return infoRecover 

def recuperarBilleteraShamirKeys(array_shamir,gruposMinimos,deCantidad,sobreTotal):
    
    infoRecover = mnemonicphrases.recuperarWalletShamir(array_shamir,gruposMinimos,deCantidad,sobreTotal)
    return infoRecover        


def crearCantidad(isVanity,prefijo1,prefijo2,prefijo3,tipoWallet,cantidadPalabras,cantidadBilleteras,guardar_archivo,gruposMinimos,deCantidad,sobreTotal,nombreArchivoDireccion,callback,cantidadDireccionesPorLog):
    inicio = 1

    if isVanity==0:
        prefijo1 ='1'
        prefijo2 ='1'
        prefijo3 ='1'


    informacionContenido = []
    while(inicio<=cantidadBilleteras):
        creadabilletera = crearBilleteraDireccion(prefijo1,prefijo2,prefijo3,tipoWallet,cantidadPalabras,guardar_archivo,gruposMinimos,deCantidad,sobreTotal,nombreArchivoDireccion,callback,cantidadDireccionesPorLog)
        if (creadabilletera !=''):
            informacionContenido.append(creadabilletera)
            inicio = inicio+1

    return informacionContenido


    
   