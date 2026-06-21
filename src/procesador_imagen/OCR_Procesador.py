import cv2
from src.procesador_imagen.inicializador import Inicializador
from src.procesador_imagen.procesador_imagen import ProcesadorImagen
from src.procesador_imagen.procesador_morfologico import ProcesadorMorfologico

# Se encarga de orquestar todas las tareas:
# 1) Cargar, 2) Analizar calidad, 3) Aplicar mejoras, 
# 4) Aplicar cambios morfológicos, 5) Guardar los resultados.

class OCRProcesador(Inicializador):
    
    """Orquestador de filtros manuales mediante composición de clases."""

    def __init__(self):
        
        # se definen los parametros del proceso
        self.min_width = 1200
        self.dark_threshold = 100
        self.blur_threshold = 80
        
        # se crea el objeto de procesadores
        self.procesador_imagen = ProcesadorImagen()
        self.procesador_morfologico = ProcesadorMorfologico()

    def proces(self, input_path, output_path):
        
        """
        Ejecuta la secuencia completa de procesamiento de imagen para OCR.

        Esta función realiza:
        1. Análisis de calidad (brillo, ruido, dimensiones).
        2. Aplicación de filtros adaptativos (CLAHE, denoise) basados en el análisis.
        3. Procesamiento morfológico (binarización, deskew).

        Args:
            input_path (str): Ruta de la imagen de entrada (pre-estandarizada).
            output_path (str): Ruta donde se guardará la imagen final limpia.

        Returns:
            dict: Diccionario con las métricas de calidad analizadas (brightness, blur, etc.).
        """

        img = cv2.imread(input_path)# se carga la imagen.

        if img is None:
            print("Error cargando imagen")# se verifica la carga.
            return

        # se analisa la imagen.
        analysis = self.procesador_imagen.analizar_imagen(img)

        # se muestra el resultado del analisis.
        print("\n=== ANALISIS ===")
        print(f"Brightness: {analysis['brightness']:.2f}")
        print(f"Blur: {analysis['blur']:.2f}")
        print(f"Width: {analysis['width']}")
        print(f"Height: {analysis['height']}")

        #Se comenta esta parte porque ya está aplicada con la clase Estandarizador.
        # corrección del tamaño.
        # if analysis["width"] < self.min_width:
        #     print("Aplicando upscale...")
        #     img = self.procesador_imagen.upscale_image(img)
        
        # se pasa a escala de grises.
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # se mejora el contraste.
        if analysis["brightness"] < self.dark_threshold:

            print("Aplicando CLAHE...")
            gray = self.procesador_imagen.apply_clahe(gray)

        # se mejora el ruido.
        if analysis["blur"] < self.blur_threshold:

            print("Aplicando denoise...")
            gray = self.procesador_imagen.denoise(gray)

        # se binariza la imagen.
        print("Aplicando threshold adaptativo...")
        processed = self.procesador_morfologico.adaptive_threshold(gray)

        # correción de inclinación.
        print("Corrigiendo inclinacion...")
        processed = self.procesador_morfologico.deskew(processed)

        cv2.imwrite(output_path, processed) # guardado de imagen procesada.

        print("\nImagen procesada guardada:")
        print(output_path)
        return analysis