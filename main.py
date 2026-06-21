import os
import pytesseract 
from PIL import Image
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from src.procesador_imagen.estandarizador import Estandarizador
from src.procesador_imagen.OCR_Procesador import OCRProcesador
from src.procesador_imagen.filtros_manuales.orquestador_filtros import OpenCVProcessor
from src.servicios import gestor_archivos, validaciones, motor_filtros
from src.servicios.pipeline_procesamiento import PipelineProcesamiento
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

@app.route('/preview', methods=['POST'])
def previsualizar_filtros():
    
    if 'image' not in request.files:
        return jsonify({'error': 'No se recibió ninguna imagen'}), 400
    archivo = request.files['image']
    efectos = request.form.get('efectos', '')
    
    if archivo.filename == '':
        return jsonify({'error': 'El archivo no tiene nombre'}), 400
    nombre_seguro = secure_filename(archivo.filename)
    ruta_original = os.path.join(app.config['UPLOAD_FOLDER'], nombre_seguro)
    archivo.save(ruta_original)

    try:
        lista_efectos = efectos.split(',') if efectos else []

        imagen_b64_string = PipelineProcesamiento.previsualizar_imagen(
            ruta_original, 
            lista_efectos
        )
        return jsonify({
            'success': True,
            'imagen_b64': imagen_b64_string
        }), 200

    except Exception as e:
        print(f"Error en previsualización: {e}")
        return jsonify({'error': str(e)}), 500

# Ruta principal para procesar la imagen y analizar el texto.
@app.route('/procesar', methods=['POST'])
def procesar_archivo(): 
    
    if 'image' not in request.files:
        return jsonify({'error': 'No se recibió ninguna imagen'}), 400
    
    archivo = request.files['image']
    efectos = request.form.get('efectos', '')
    
    if archivo.filename == '':
        return jsonify({'error': 'El archivo no tiene nombre'}), 400
    
    nombre_seguro = secure_filename(archivo.filename)

    ruta_original = os.path.join(app.config['UPLOAD_FOLDER'], nombre_seguro)
    ruta_intermedia = os.path.join(app.config['PROCESSED_FOLDER'], f"temp_{nombre_seguro}")
    
    try:
        lista_efectos = efectos.split(',') if efectos else []
        ruta_a_procesar = PipelineProcesamiento.preparar_imagen_para_ocr(
            ruta_original, 
            ruta_intermedia, 
            lista_efectos
        )

        nombre_final_ocr = f"proc_{nombre_seguro}"
        ruta_procesada = os.path.join(app.config['PROCESSED_FOLDER'], nombre_final_ocr)
        
        procesador_ocr = OCRProcesador()
        datos_analisis = procesador_ocr.proces(ruta_a_procesar, ruta_procesada)
        
        imagen_pil = Image.open(ruta_procesada)
        configuracion_ocr = '-l spa --psm 6'
        texto_real = pytesseract.image_to_string(imagen_pil, config=configuracion_ocr)
    
        nombre_txt = gestor_archivos.guardar_texto_extraido(
            texto_real, nombre_seguro, app.config['TEXT_FOLDER']
        )
        
        return jsonify({
            'success': True,
            'msg': '¡Imagen procesada y analizada con éxito!',
            'url_original': f"/imagenes/originales/{nombre_seguro}",
            'url_procesada': f"/imagenes/procesadas/{nombre_final_ocr}",
            'texto_analisis': texto_real,
            'datos_analisis': datos_analisis
        }), 200

    except Exception as e:
        print(f"Error crítico en proceso: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)