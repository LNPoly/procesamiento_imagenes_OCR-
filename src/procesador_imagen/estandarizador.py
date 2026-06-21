from PIL import Image
import cv2
import numpy as np
from src.procesador_imagen.inicializador import Inicializador
class Estandarizador(Inicializador):
    
    """
        Redimensiona la imagen manteniendo su relación de aspecto original.

        Utiliza el algoritmo de interpolación LANCZOS de Pillow, el cual es 
        altamente recomendado para preservar la nitidez de fuentes y caracteres 
        en documentos, facilitando la posterior lectura por OCR.

        Args:
            ancho_objetivo (int): El ancho deseado en píxeles. Por defecto es 1500.

        Returns:
            Estandarizador: Retorna la instancia actual para permitir encadenamiento.
        """
    def estandarizar(self, ancho_objetivo=1500) -> "Estandarizador":
        
        ancho_orig, alto_orig = self._imagen.size
        
        # Si la imagen ya tiene el ancho objetivo ideal, no hace falta reescalarla
        if ancho_orig == ancho_objetivo:
            print(f"La imagen ya posee el ancho estandarizado de {ancho_objetivo}px.")
            return self
            
        proporcion = ancho_objetivo / float(ancho_orig)
        alto_nuevo = int(float(alto_orig) * proporcion)
        
        # Se redimenciona usando un filtro de alta calidad para mantener nitidez en texto
        self._imagen = self._imagen.resize((ancho_objetivo, alto_nuevo), Image.Resampling.LANCZOS)
        
        print(f"Imagen estandarizada mediante Pillow a: {ancho_objetivo}x{alto_nuevo} (Manteniendo proporción)")
        return self