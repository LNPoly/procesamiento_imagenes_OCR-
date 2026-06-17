import os
import pytesseract 
from PIL import Image
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from src.procesador_imagen.estandarizador import Estandarizador
from src.procesador_imagen.OCR_Procesador import OCRProcesador
from src.procesador_imagen.filtros_manuales.orquestador_filtros import OpenCVProcessor
from src.servicios import gestor_archivos, validaciones, motor_filtros
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
def previsualizar_filtros(): #modularizar esta función
    
    if 'image' not in request.files:
        return jsonify({'success': False, 'error': 'Falta el archivo de imagen'}), 400
        
    archivo = request.files['image']
    efectos_solicitados = request.form.get('efectos', '')
    lista_efectos = efectos_solicitados.split(',') if efectos_solicitados else []
    
    if not archivo or archivo.filename == '':
        return jsonify({'success': False, 'error': 'No se seleccionó ninguna imagen'}), 400
        
    try:
        nombre_seguro = secure_filename(archivo.filename)
        ruta_temporal_entrada = os.path.join(app.config['UPLOAD_FOLDER'], f"tmp_in_{nombre_seguro}")
        archivo.save(ruta_temporal_entrada)
        
        procesador_manual = OpenCVProcessor()
        procesador_manual.load_image(ruta_temporal_entrada)
        procesador_manual = motor_filtros.MotorFiltros.aplicar_lista_filtros(procesador_manual, lista_efectos)
        
        nombre_temporal_salida = f"tmp_out_{nombre_seguro}"
        ruta_temporal_salida = os.path.join(app.config['PROCESSED_FOLDER'], nombre_temporal_salida)
        procesador_manual.save(ruta_temporal_salida)

        if os.path.exists(ruta_temporal_entrada):
            os.remove(ruta_temporal_entrada)
            
        url_preview = f"/imagenes/procesadas/{nombre_temporal_salida}"
        return jsonify({'success': True, 'url_preview': url_preview}), 200
        
    except Exception as e:
        if 'ruta_temporal' in locals() and os.path.exists(ruta_temporal):
            os.remove(ruta_temporal)
        return jsonify({'success': False, 'error': str(e)}), 500

# Ruta principal para procesar la imagen y analizar el texto.
# Seguido de la función que maneja la carga de archivos, procesamiento de imágenes y análisis de texto.
@app.route('/procesar', methods=['POST'])
def procesar_archivo(): 

    es_valido, mensaje_error = validaciones.Validaciones.validar_archivo(request.files, app.config['ALLOWED_EXTENSIONS'])
    if not es_valido:
        return jsonify({'error': mensaje_error}), 400
    
    archivo = request.files['image']
    
    efectos_solicitados = request.form.get('efectos', '')
    lista_efectos = efectos_solicitados.split(',') if efectos_solicitados else []
    
    try:
        imagen_nombre, ruta_entrada = gestor_archivos.guardar_imagen_original(
            archivo, app.config['UPLOAD_FOLDER']
        )
        # efectos manuales. Modularizarlos despues para achicar la funcion principal.
        if lista_efectos:
            try:
                procesador_manual = OpenCVProcessor()
                procesador_manual.load_image(ruta_entrada)

                for efecto in lista_efectos:
                    match efecto:
                        case 'grayscale':
                            procesador_manual.to_grayscale()
                        case 'binarize':
                            procesador_manual.binarize()
                        case 'noise_reduction':
                            procesador_manual.reduce_noise()
                        case 'contrast':
                            procesador_manual.apply_brightness_contrast(alpha=1.5, beta=20)
                        case _:
                            print(f"Advertencia: El efecto '{efecto}' no está reconocido.")

                nombre_intermedio = f"manual_{imagen_nombre}"
                ruta_intermedia = os.path.join(app.config['UPLOAD_FOLDER'], nombre_intermedio)
                procesador_manual.save(ruta_intermedia)
                
                # Reasignamos la ruta para el OCR
                ruta_entrada = ruta_intermedia
                
            except Exception as e:
                print(f"Advertencia: Falló la aplicación de filtros manuales: {e}")
        
        nombre_final_ocr = f"proc_{imagen_nombre}"
        ruta_procesada = os.path.join(app.config['PROCESSED_FOLDER'], nombre_final_ocr)
        procesador_ocr = OCRProcesador()
        procesador_ocr.proces(ruta_entrada, ruta_procesada)
        imagen_pil = Image.open(ruta_procesada)
        configuracion_ocr = '-l spa --psm 6'
        texto_real = pytesseract.image_to_string(imagen_pil, config=configuracion_ocr)
    
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