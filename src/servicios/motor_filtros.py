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
                    procesador.a_escala_grises()
                case 'binarizar':
                    procesador.binarizar(threshold=127)
                case 'brillo' | 'contraste':
                    procesador.brillo_contraste(alpha=1.0, beta=30)
                case 'desenfoque':
                    procesador.reduccion_ruido(kernel_size=5)

        return procesador