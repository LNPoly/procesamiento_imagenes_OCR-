
import os
import cv2
import base64
from src.procesador_imagen.filtros_manuales.orquestador_filtros import OpenCVProcessor
from src.procesador_imagen.OCR_Procesador import OCRProcesador
from src.procesador_imagen.estandarizador import Estandarizador
from src.servicios import motor_filtros, gestor_archivos
from PIL import Image
import pytesseract

class PipelineProcesamiento:
    
    @staticmethod
    def previsualizar_imagen(ruta_origen, lista_efectos):
        """
        Aplica filtros y devuelve la imagen codificada en Base64 para el frontend.
        """
        procesador = OpenCVProcessor()
        procesador.load_image(ruta_origen)

        motor_filtros.MotorFiltros.aplicar_lista_filtros(procesador, lista_efectos)
        imagen_cv2 = procesador._image
        
        _, buffer = cv2.imencode('.jpg', imagen_cv2)
        imagen_b64 = base64.b64encode(buffer).decode('utf-8')
        
        return f"data:image/jpeg;base64,{imagen_b64}"
    
    @staticmethod
    def preparar_imagen_para_ocr(ruta_original, ruta_intermedia, lista_efectos):
        """
        Orquesta el flujo de preprocesamiento necesario antes de ejecutar el OCR.

        Aplica primero la estandarización de dimensiones y, posteriormente, 
        los filtros manuales solicitados por el usuario para maximizar el contraste
        y reducir el ruido de la imagen.

        Args:
            ruta_original (str): Path de la imagen original subida.
            ruta_intermedia (str): Path donde se guardará el resultado del preprocesamiento.
            lista_efectos (list): Lista de nombres de efectos a aplicar.

        Returns:
            str: La ruta del archivo resultante listo para ser procesado por Tesseract.
        """
        estandarizador = Estandarizador(ruta_original)
        estandarizador.estandarizar(ancho_objetivo=1500)
        estandarizador.guardar(ruta_intermedia)
        
        if lista_efectos and len(lista_efectos) > 0:
            procesador = OpenCVProcessor()
            procesador.load_image(ruta_intermedia)
            motor_filtros.MotorFiltros.aplicar_lista_filtros(procesador, lista_efectos)
            procesador.save(ruta_intermedia)
        
        return ruta_intermedia
    