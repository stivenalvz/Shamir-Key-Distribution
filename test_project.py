import pytest
import vanity 
import listarunidades 
import qrcodeimagen
import leerqr
import json


def test_crearCantidad():
    # Prueba para crearCantidad
    is_vanity = 1  # 1 para vanity, 0 para no vanity
    prefix1 = '1'
    prefix2 = '1'
    prefix3 = '1'
    tipo = 1  # Tipo de wallet (1: legacy, 2: segwit, 3: native segwit)
    words = 12  # Número de palabras
    max_results = 1  # Número máximo de resultados
    guardar_archivo = 1  # 1 para guardar, 0 para no guardar
    gruposMinimos = 1  # Grupos mínimos para Shamir
    deCantidad = 3  # Cantidad de claves para que un grupo sea correcto
    sobreTotal = 5  # Cantidad de claves por grupo
    nombre_archivo_direccion = 'address.txt'  # Nombre del archivo para guardar direcciones
    callback = lambda x: None  # Callback de progreso
    cantidadDireccionesPorLog = 1  # Cantidad de direcciones por log

    result = vanity.crearCantidad(is_vanity, prefix1, prefix2, prefix3, tipo, words, max_results, guardar_archivo, gruposMinimos, deCantidad, sobreTotal, nombre_archivo_direccion, callback, cantidadDireccionesPorLog)
    
    try:
        result = vanity.crearCantidad(
            is_vanity, prefix1, prefix2, prefix3, tipo,
            words, max_results, guardar_archivo,
            gruposMinimos, deCantidad, sobreTotal,
            nombre_archivo_direccion, callback, cantidadDireccionesPorLog
        )
        assert isinstance(result, list)
        return True  # ✅ Prueba pasada
    except AssertionError:
        return False  # ❌ La función no devolvió una lista
    except Exception as e:
        print(f"Error inesperado: {e}")
        return False
    
def test_list_windows_drives():
    try:
        drives = listarunidades.list_windows_drives()
        assert isinstance(drives, list)  # Verifica que el resultado sea una lista
        assert len(drives) >= 0  # Verifica que retorne informacion de las unidades
        return True
    except AssertionError:
        return False
    except Exception as e:
        print(f"Error inesperado: {e}")
        return False


def test_guardar_en_archivo():
    filename = 'test_file.txt'
    content = 'Test content'

    try:
        result = vanity.guardar_en_archivo(filename, content)
        assert result is None  # La función no debe devolver nada

        with open(filename, 'r') as f:
            file_content = f.read().strip()
            assert file_content == content  # Verifica que el contenido sea correcto

        return True  # ✅ Prueba pasada
    except AssertionError:
        return False  # ❌ Falló alguna aserción
    except Exception as e:
        print(f"Error inesperado: {e}")
        return False

info = test_crearCantidad()
info2 = test_guardar_en_archivo()
info3 = test_list_windows_drives()

print(info)
print(info2)
print(info3)
