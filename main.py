import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from src.procesador_imagen.estandarizador import Estandarizador

app = Flask(__name__)

# Configuración de carpetas y extensiones permitidas

UPLOAD_FOLDER = os.path.join('data', 'img_originales')
PROCESSED_FOLDER = os.path.join('data', 'img_procesada')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)


# Función para verificar si el archivo tiene una extensión permitida
def archivo_permitido(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Rutas de la aplicación
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/imagenes/originales/<filename>')
def imagen_original(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/imagenes/procesadas/<filename>')
def imagen_procesada(filename):
    return send_from_directory(app.config['PROCESSED_FOLDER'], filename)

# Ruta principal para procesar la imagen y analizar el texto.
# Seguido de la función que maneja la carga de archivos, procesamiento de imágenes y análisis de texto.
@app.route('/procesar', methods=['POST'])
def procesar_archivo():
    
    if 'image' not in request.files:
        return jsonify({'error': 'No se envió ninguna imagen'}), 400
    
    archivo = request.files['image']
    if archivo.filename == '':
        return jsonify({'error': 'Nombre de archivo vacío'}), 400
    
    if archivo and archivo_permitido(archivo.filename):
                
        imagen_nombre = secure_filename(archivo.filename)
        ruta_entrada = os.path.join(app.config['UPLOAD_FOLDER'], imagen_nombre)
        archivo.save(ruta_entrada)
        
        nombre_salida = f"estandarizada_{imagen_nombre}"
        ruta_salida = os.path.join(app.config['PROCESSED_FOLDER'], nombre_salida)
                
        try:
            imagen = Estandarizador(ruta_entrada)
            imagen.estandarizar(1500).guardar(ruta_salida)
   
            url_original = f"/imagenes/originales/{imagen_nombre}"
            url_resultado = f"/imagenes/procesadas/{nombre_salida}"
    
            texto_simulado = "Acá iría el resultado del análisis de texto extraído de la imagen procesada."
            
            #Una vez hecho el análisis de texto,
            # crear la lógica para guardar el texto en un archivo .txt y asi poder descargarlo.
            
            return jsonify({
                'success': True,
                'msg': '¡Imagen procesada y analizada con éxito!',
                'url_original': url_original,
                'url_procesada': url_resultado,
                'texto_analisis': texto_simulado
            }), 200
            
        except Exception as e:
            return jsonify({'error': f'Error en el procesamiento: {str(e)}'}), 500
            
    return jsonify({'error': 'Extensión de archivo no permitida'}), 400

if __name__ == "__main__":
    app.run(debug=True)