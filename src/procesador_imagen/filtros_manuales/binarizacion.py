def binarize(self, threshold: int = 127):
        """
        Convierte la imagen a blanco y negro absoluto (0 o 255).
        Los píxeles con intensidad superior al umbral se vuelven blancos.
        """
        if self._image is None:
            raise RuntimeError("Operación denegada: No hay ninguna imagen cargada en el procesador.")
            
        # Blindaje: La binarización estricta exige un solo canal.
        # Si la matriz aún tiene 3 dimensiones, la forzamos a grises.
        if len(self._image.shape) == 3:
            matriz_operativa = cv2.cvtColor(self._image, cv2.COLOR_BGR2GRAY)
        else:
            matriz_operativa = self._image
            
        # cv2.threshold retorna una tupla: (umbral_aplicado, matriz_resultante)
        # Ignoramos el primer valor con '_' y reasignamos el estado de la imagen.
        _, self._image = cv2.threshold(matriz_operativa, threshold, 255, cv2.THRESH_BINARY)
        
        return self._image