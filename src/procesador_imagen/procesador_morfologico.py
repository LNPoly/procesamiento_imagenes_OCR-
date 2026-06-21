import cv2
import numpy as np

# Esta clase se dedica a las transformaciones espaciales de la imagen.
class ProcesadorMorfologico:

    # función para hacer la imagen binaria.
    def adaptive_threshold(self, gray):

        return cv2.adaptiveThreshold(
            gray, # imagen en grises.
            255, # umbral
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C, # calculo del promedio.
            cv2.THRESH_BINARY, # salida -> texto negro/fondo blanco.
            11, # tamaño de la ventana de analisis de los pixeles.
            2 # correción de umbral.
        )
    
    # función para enderezar una imagen.
    def deskew(self, image):

        # calcula posición y ángulo de los pixeles negros.
        coords = np.column_stack(np.where(image > 0))
        angulo = float(cv2.minAreaRect(coords)[-1])

        # ajuste del angulo
        if angulo < -45:
            angulo = -(90 + angulo)
        else:
            angulo = -angulo

        (height, width) = image.shape[:2] # el tamaño de la imagen.
        centro = (width // 2, height // 2) # calculo centro de la imagen.

        # se crea matriz de rotación.
        Matriz = cv2.getRotationMatrix2D(
            centro, # el centro.
            angulo, # el ángulo.
            1.0 # la escala(no cambia)
        )

        # Se aplica la correción.
        return cv2.warpAffine(
            image, # imagen
            Matriz, # la matriz
            (width, height), # el tamaño.
            # se usan para mentener cálidad.
            flags=cv2.INTER_CUBIC, 
            borderMode=cv2.BORDER_REPLICATE 
        )