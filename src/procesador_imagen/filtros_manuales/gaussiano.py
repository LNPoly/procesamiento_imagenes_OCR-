import cv2

class FiltroGaussiano:
    def reduccion_ruido(self, kernel_size: int = 5):
            """
            Aplica un desenfoque Gaussiano para atenuar el ruido.
            El kernel de convolución debe ser una matriz cuadrada de dimensión impar.
            """
            self._ensure_image_loaded()
                        
            # Validación matemática inquebrantable: el kernel no puede ser par ni menor a 1.
            if kernel_size % 2 == 0 or kernel_size <= 0:
                raise ValueError("Error de dimensión: El tamaño del kernel debe ser un número impar positivo (ej: 3, 5, 7).")
            
            # cv2.GaussianBlur exige una tupla para las dimensiones del kernel (ancho, alto).
            # El parámetro 0 final indica que la desviación estándar (sigma) se calcula automáticamente
            # a partir del tamaño del kernel.
            self._image = cv2.GaussianBlur(self._image, (kernel_size, kernel_size), 0)
            
            return self._image