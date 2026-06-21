import cv2
from src.procesador_imagen.filtros_manuales.orquestador_filtros import OpenCVProcessor
class MotorFiltros:
    @staticmethod
    def aplicar_lista_filtros(procesador: OpenCVProcessor, lista_efectos: list):
        
        """
        Recorre una lista de efectos solicitados y los aplica secuencialmente.

        Args:
            procesador (OpenCVProcessor): Instancia del procesador con la imagen cargada.
            lista_efectos (list): Lista de strings (ej: ['gris', 'binarizar']).
        
        Returns:
            OpenCVProcessor: La instancia con los filtros aplicados.
        """
        
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
                case _:
                    print(f"Advertencia: El efecto '{efecto}' no está reconocido.")

        return procesador