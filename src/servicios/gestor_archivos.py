import os
from werkzeug.utils import secure_filename

def preparar_entorno(app):
    
    for folder in [app.config['UPLOAD_FOLDER'], app.config['PROCESSED_FOLDER'], app.config['TEXT_FOLDER']]:
        os.makedirs(folder, exist_ok=True)

def es_archivo_valido(filename, extensiones_permitidas):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensiones_permitidas

def guardar_imagen_original(archivo, upload_folder):
   
    imagen_nombre = secure_filename(archivo.filename)
    ruta_entrada = os.path.join(upload_folder, imagen_nombre)
    archivo.save(ruta_entrada)
    return imagen_nombre, ruta_entrada


def guardar_texto_extraido(texto_real, imagen_nombre, text_folder):
    
    nombre_txt = f"{imagen_nombre.rsplit('.', 1)[0]}.txt"
    ruta_txt = os.path.join(text_folder, nombre_txt)
    
    with open(ruta_txt, 'w', encoding='utf-8') as f:
        f.write(texto_real)
    return nombre_txt