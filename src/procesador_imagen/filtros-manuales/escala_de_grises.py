def to_grayscale(self):
        #  Convierte la matriz de la imagen actual a escala de grises
        #aplicando la transformación de luminancia ITU-R BT.601.
        
        if self._image is None:
            raise RuntimeError("No hay ninguna imagen cargada en el procesador.")
        
        # Se verifica que la imagen tenga 3 dimensiones (Alto, Ancho, Canales)
        # Si ya es bidimensional (blanco y negro nativo), se omite la conversión para evitar un colapso.
        if len(self._image.shape) == 3:
            self._image = cv2.cvtColor(self._image, cv2.COLOR_BGR2GRAY)
        
        return self._image