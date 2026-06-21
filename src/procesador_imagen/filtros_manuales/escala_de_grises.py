import cv2
class EscalaGrises:
    def a_escala_grises(self):
            # Convierte la matriz de la imagen actual a escala de grises
            #aplicando la transformación de luminancia ITU-R BT.601.
            
            self._ensure_image_loaded()
            
            # Se verifica que la imagen tenga 3 dimensiones (Alto, Ancho, Canales)
            # Si ya es bidimensional (blanco y negro nativo), se omite la conversión para evitar un colapso.
            if len(self._image.shape) == 3:
                self._image = cv2.cvtColor(self._image, cv2.COLOR_BGR2GRAY)
            
            return self._image