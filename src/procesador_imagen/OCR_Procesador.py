import cv2
import numpy as np
from src.procesador_imagen.inicializador import Inicializador

# La idea es no dejar al usuario la parametrización de los filtros. 
# Se parte de una optimización estandar de los parametros ideales para el objetivo del trabajo
# y en función de eso, lo primero que se hace se evalua la imagen de ingreso si se ajusta a ese molde ideal,
# y en función de los resultados de ese analisis se procedera a realizarles cambios que la acerquen al modelo ideal. 

class OCRProcesador(Inicializador):

    def __init__(self):

        # Configuración base de las imagenes que se usaran para el posterior procesamiento

        self.min_width = 1200
        self.dark_threshold = 100
        self.blur_threshold = 80

    def analisar_image(self, img):

        # Esta función tiene la función de analizar la imagen de entrada para evaluar la calidad de la misma
        # Convertir a escala de grises
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        brightness = np.mean(gray)
        blur = cv2.Laplacian(gray, cv2.CV_64F).var()
        height, width = img.shape[:2]

        return {
            "brightness": brightness,
            "blur": blur,
            "width": width,
            "height": height
        }

    def upscale_image(self, img):

        # Regulamos el tamaño de la imagen
        upscaled = cv2.resize(
            img,
            None,
            fx=2,
            fy=2,
            interpolation=cv2.INTER_CUBIC
        )

        return upscaled

    def apply_clahe(self, gray):

        # Mejoramos el contraste en imagenes oscuras o muy luminosas
        clahe = cv2.createCLAHE(
            clipLimit=2.0,
            tileGridSize=(8, 8)
        )

        return clahe.apply(gray)

    def denoise(self, gray):

        # Quitamos el ruido para mejorar imagenes borrosas
        denoised = cv2.fastNlMeansDenoising(
            gray,
            None,
            h=10
        )
        return denoised

    def adaptive_threshold(self, gray):

        # Conversión una imagen en escala de grises a binaria con un umbral.
        thresh = cv2.adaptiveThreshold(
            gray,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            11,
            2
        )
        return thresh

    def deskew(self, image):

        # Corrige las inclinaciones en las imagenes
        coords = np.column_stack(np.where(image > 0))
        angle = cv2.minAreaRect(coords)[-1]

        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle
            
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(
            image,
            M,
            (w, h),
            flags=cv2.INTER_CUBIC,
            borderMode=cv2.BORDER_REPLICATE
        )
        return rotated
    
    # PIPELINE PRINCIPAL
    def proces(self, input_path, output_path):

        img = cv2.imread(input_path)

        if img is None:
            print("Error cargando imagen")
            return

        # Analisis de imagen
        analysis = self.analisar_image(img)
        
        print("\n=== ANALISIS ===")
        print(f"Brightness: {analysis['brightness']:.2f}")
        print(f"Blur: {analysis['blur']:.2f}")
        print(f"Width: {analysis['width']}")
        print(f"Height: {analysis['height']}")

        # Corrigiendo tamaño
        
        if analysis["width"] < self.min_width:

            print("Aplicando upscale...")
            img = self.upscale_image(img)

        # Escala de grise
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Binarización
        if analysis["brightness"] < self.dark_threshold:
            print("Aplicando CLAHE...")
            gray = self.apply_clahe(gray)

        # Corrigiendo ruido
        if analysis["blur"] < self.blur_threshold:
            print("Aplicando denoise...")
            gray = self.denoise(gray)

        # Binarización de la imagen
        print("Aplicando threshold adaptativo...")
        processed = self.adaptive_threshold(gray)
        
        # Corrigiendo las inclinaciones problemáticas   
        print("Corrigiendo inclinacion...")
        processed = self.deskew(processed)

        # GUARDAR RESULTADO     
        cv2.imwrite(output_path, processed)
        print("\nImagen procesada guardada:")
        print(output_path)# aqui va la logica del procesamiento de imagenes, se pueden agregar funciones para mejorar la calidad de la imagen, eliminar ruido, etc.