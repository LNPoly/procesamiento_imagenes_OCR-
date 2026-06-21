import cv2
import numpy as np

# Esta clase se dedica a las transformaciones espaciales de la imagen.
class ProcesadorMorfologico:

    """Procesamiento de transformaciones espaciales y binarización."""
    
    def adaptive_threshold(self, gray):
        
        """
        Aplica un umbral adaptativo para binarizar la imagen.

        Utiliza el método Gaussiano para calcular el umbral localmente, 
        lo cual es ideal para documentos con iluminación desigual.

        Args:
            gray (np.ndarray): La imagen original convertida a escala de grises.

        Returns:
            np.ndarray: Imagen binaria (blanco y negro puro).
        """

        return cv2.adaptiveThreshold(
            gray, # imagen en grises.
            255, # umbral
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C, # calculo del promedio.
            cv2.THRESH_BINARY, # salida -> texto negro/fondo blanco.
            51, # tamaño de la ventana de analisis de los pixeles.
            2 # correción de umbral.
        )
    
    # función para enderezar una imagen.
    def deskew(self, image):
        
        """
        Detecta y corrige la inclinación (skew) de un documento.

        Calcula el ángulo de los pixeles negros para rotar la imagen 
        a una orientación horizontal perfecta, mejorando la precisión del OCR.

        Args:
            image (np.ndarray): Imagen binaria a enderezar.

        Returns:
            np.ndarray: Imagen enderezada.
        """

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