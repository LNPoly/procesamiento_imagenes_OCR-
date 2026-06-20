import cv2
import numpy as np

# Se crea 2 clases diferentes de modulos para en tratamiento de imagen
# según una función general. Esta se dedica a la imagen en tanto a su aspecto
# visual.
# Se quiere por medio de un proceso llevar la imagen la más optima posible
# para procesarla en el OCR.

class ProcesadorImagen:
    
    # función de analisis de la imagen.
    def analisar_image(self, img):
        
        # a escala de grises
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # promedio de brillo 0=Negro, 255=Blanco.
        brightness = np.mean(gray)

        # mide la nítidez de la imagen.
        blur = cv2.Laplacian(gray, cv2.CV_64F).var()

        # dimensiones de la imagen.
        height, width = img.shape[:2]

        # devuelde el resultado en un diccionario.
        return {
            "brightness": brightness,
            "blur": blur,
            "width": width,
            "height": height
        }
    
    # Función que agranda la imagen para ayudar al OCR
    def upscale_image(self, img):
        
        # Aumenta la imagen al doble y rellena si falta pixeles.
        return cv2.resize(
            img,
            None,
            fx=2, # duplica tamaño.
            fy=2, # duplica tamaño.
            interpolation=cv2.INTER_CUBIC # ideal para OCR para el relleno
            # de pixeles faltante.
        )
    
    # Función de mejora el contraste entre figura y fondo.
    def apply_clahe(self, gray):
        
        clahe = cv2.createCLAHE(
            clipLimit=2.0, # marca el nivel del contraste.
            tileGridSize=(8, 8) # crea cuadriculas independiente.
        )

        return clahe.apply(gray) # lo aplica en la escala de grises.
    
    # Función para eliminar ruido de imagenes poco claras.
    def denoise(self, gray):

        return cv2.fastNlMeansDenoising(
            gray, # la imagen en escala de grises
            None, # crea una nueva imagen
            h=10  # controla la reducción del ruido.
        )
