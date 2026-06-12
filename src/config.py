
import os
import platform

UPLOAD_FOLDER = os.path.join('data', 'img_originales')
PROCESSED_FOLDER = os.path.join('data', 'img_procesada')
TEXT_FOLDER = os.path.join('data', 'textos_extraidos')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

# Verificación de sistema operativo
if platform.system() == 'Windows':
    TESSERACT_CMD = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
else:
    TESSERACT_CMD = '/usr/bin/tesseract'