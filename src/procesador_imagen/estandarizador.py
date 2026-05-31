from PIL import Image
import cv2
import numpy as np
from src.procesador_imagen.inicializador import Inicializador

class Estandarizador(Inicializador):
    
    def estandarizar(self, ancho_objetivo=1500) -> "Estandarizador":
        ancho_orig, alto_orig = self._imagen.size
        
        proporcion = ancho_objetivo / float(ancho_orig)
        alto_nuevo = int(float(alto_orig) * proporcion)
        
        # Redimensionar usando un filtro de alta calidad
        # Resampling.LANCZOS es el mejor para mantener nitidez en texto
        self._imagen = self._imagen.resize((ancho_objetivo, alto_nuevo), Image.Resampling.LANCZOS)
        
        print(f"Imagen reescalada a: {ancho_objetivo}x{alto_nuevo} (Manteniendo proporción)")
        return self