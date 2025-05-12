import qrcode
import os
import base64
import io

def crearImagen(path,text,filename):    
    try:
        file_path = os.path.join(path, filename)   
        # Texto que deseas convertir en un código QR
        # Crea una instancia de QRCode
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        # Añade el texto al código QR
        qr.add_data(text)
        qr.make(fit=True)
        # Crea una imagen del código QR
        img = qr.make_image(fill='black', back_color='white')
        # Guarda la imagen
        img.save(file_path)
        return 'ok'
    except :
        return 'error'

def ImagenBase64(text):
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(text)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        return img_base64
    except Exception as e:
        return 'error'