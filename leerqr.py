import cv2

def read_qr_code(image_path):
    try:
        # Cargar la imagen que contiene el código QR
        img = cv2.imread(image_path)

        # Crear el detector de código QR
        detector = cv2.QRCodeDetector()

        # Detectar y decodificar el código QR
        data, vertices_array, _ = detector.detectAndDecode(img)

        if vertices_array is not None:
            return data
        else:
            return 'error'
    except :   
        return 'error' 


