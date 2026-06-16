import cv2
import numpy as np

def brightness_contrast(self, alpha, beta):
    # alpha controla el contraste
    # beta controla el brillo
    
    # Validación innegociable de estado
    if self._image is None:
        raise RuntimeError("Operación denegada: No hay imagen cargada en la memoria.")
        
    # Invocación correcta a la librería cv2 y al método ScaleAbs
    self._image = cv2.convertScaleAbs(self._image, alpha, beta)
    return self._image