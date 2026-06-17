import cv2
import base64
from src.procesador_imagen.filtros_manuales.orquestador_filtros import OpenCVProcessor
class MotorFiltros:
    @staticmethod
    def aplicar_lista_filtros(procesador: OpenCVProcessor, lista_efectos: list):
        
        """Aplica una secuencia de filtros manuales sobre el procesador."""
        
        for efecto in lista_efectos:
            efecto = efecto.strip().lower()
            match efecto:
                case 'gris':
                    procesador.to_grayscale()
                case 'binarizar':
                    procesador.binarize(threshold=127)
                case 'brillo' | 'contrast':
                    procesador.apply_brightness_contrast(alpha=1.0, beta=30)
                case 'desenfoque':
                    procesador.reduce_noise(kernel_size=5)

        return procesador