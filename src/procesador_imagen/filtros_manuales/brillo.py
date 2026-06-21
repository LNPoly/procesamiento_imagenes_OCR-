import cv2
import numpy as np
class BrilloContraste:
    def brillo_contraste(self, alpha, beta):
        # alpha controla el contraste
        # beta controla el brillo
        self._ensure_image_loaded()

        # Invocación correcta a la librería cv2 y al método ScaleAbs
        self._image = cv2.convertScaleAbs(self._image, alpha, beta)
        return self._image