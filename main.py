import os
import pytesseract 
from PIL import Image
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from src.procesador_imagen.estandarizador import Estandarizador
from src.procesador_imagen.OCR_Procesador import OCRProcesador
from src.servicios import gestor_archivos
from src.servicios import validaciones
from src import config

app = Flask(__name__)
app.config.from_object(config)

pytesseract.pytesseract.tesseract_cmd = config.TESSERACT_CMD

gestor_archivos.preparar_entorno(app)

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

@app.route('/textos/<filename>')
def descargar_texto(filename):
    return send_from_directory(app.config['TEXT_FOLDER'], filename, as_attachment=True)

# Ruta principal para procesar la imagen y analizar el texto.
# Seguido de la función que maneja la carga de archivos, procesamiento de imágenes y análisis de texto.
@app.route('/procesar', methods=['POST'])
def procesar_archivo():

    es_valido, mensaje_error = validaciones.Validaciones.validar_archivo(request.files, app.config['ALLOWED_EXTENSIONS'])
    if not es_valido:
        return jsonify({'error': mensaje_error}), 400
    
    archivo = request.files['image']
    
    try:
        imagen_nombre, ruta_entrada = gestor_archivos.guardar_imagen_original(
            archivo, app.config['UPLOAD_FOLDER']
        )
        
        texto_real, nombre_salida, nombre_final_ocr = OCRProcesador(
            ruta_entrada, 
            imagen_nombre, 
            app.config['PROCESSED_FOLDER']
        )
    
        nombre_txt = gestor_archivos.guardar_texto_extraido(
            texto_real, imagen_nombre, app.config['TEXT_FOLDER']
        )
        
        return jsonify({
            'success': True,
            'msg': '¡Imagen procesada y analizada con éxito!',
            'url_original': f"/imagenes/originales/{imagen_nombre}",
            'url_procesada': f"/imagenes/procesadas/{nombre_final_ocr}",
            'texto_analisis': texto_real
        }), 200
        
    except Exception as e:
        print(f"Error durante el procesamiento: {e}")
        return jsonify({'error': f'Error en el procesamiento: {str(e)}'}), 500

if __name__ == "__main__":
    app.run(debug=True)