import cv2
import numpy as np

from .binarizacion import Binarizar
from .brillo import BrilloContraste
from .escala_de_grises import EscalaGrises
from .gaussiano import FiltroGaussiano


class OpenCVImageReader:
    def open(self, path):
        return cv2.imread(path)
class OpenCVProcessor(BrilloContraste,EscalaGrises,Binarizar,FiltroGaussiano):
    
    def __init__(self):
        self._image = None
        self.reader = OpenCVImageReader()

    def _ensure_image_loaded(self):
        
        """Método auxiliar para validación de estado."""
        
        if self._image is None:
            raise RuntimeError("Operación denegada: No hay ninguna imagen cargada.")
        
    def load_image(self, path):
        
        """Carga la imagen y la almacena en el estado del procesador."""
        
        self._image = self.reader.open(path)
        if self._image is None:
            raise ValueError(f"No se pudo cargar la imagen en: {path}")
        
    def save(self, output_path: str):
      
        if self._image is None:
            raise RuntimeError("Operación denegada: No hay imagen para guardar.")

        success = cv2.imwrite(output_path, self._image)
        
        if not success:
            raise IOError(f"Error: No se pudo guardar la imagen en {output_path}")
            
        print(f"Imagen guardada exitosamente en: {output_path}")
