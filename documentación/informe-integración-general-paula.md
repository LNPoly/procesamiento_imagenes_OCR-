## INFORME TÉCNICO
### REFACTORIZACIÓN, MODULARIZACIÓN E INTEGRACIÓN DEL PIPELINE DE PROCESAMIENTO DE IMÁGENES Y OPTIMIZACIÓN DE OCR

Fecha: 23 de junio de 2026

#### Proyecto
Sistema de Procesamiento de Documentos y Reconocimiento Óptico de Caracteres (OCR)

#### Estado
Integrado y Listo para Producción (Production-Ready)

## INTRODUCCIÓN Y OBJETIVOS
El presente informe detalla las actividades de refactorización estructural, desacoplamiento de componentes e integración arquitectónica realizadas sobre el sistema de procesamiento de imágenes. El objetivo principal de esta fase fue unificar dos esfuerzos de desarrollo paralelos para construir una línea de procesamiento (pipeline) sólida, escalable y de alta precisión para el motor de OCR (Tesseract).

A través de esta intervención se logró mitigar problemas de degradación tipográfica, eliminar la redundancia de código, optimizar la transferencia de datos en memoria entre el backend (Flask) y el frontend (JavaScript) mediante Base64, e implementar documentación y diseño de software limpio.

### 1- COMPONENTE DE FILTROS MANUALES (CONTRIBUCIÓN: ALEJANDRO)
El primer pilar de la reestructuración consistió en la incorporación y ordenamiento del ecosistema de filtros manuales desarrollados por Alejandro. Este módulo otorga flexibilidad al usuario final, permitiéndole limpiar la imagen de forma interactiva antes de enviarla al motor de análisis morfológico.

**Arquitectura de Archivos Adheridos**

Se estructuró una suite de filtros atómicos y específicos basados en la librería OpenCV, organizados bajo el patrón de diseño de herencia múltiple y composición:

- *escala_de_grises.py:* Simplifica la matriz cromática eliminando los canales RGB innecesarios y convirtiendo la imagen a un solo canal de intensidades (0-255).

- *brillo.py (BrilloContraste):* Regula las ganancias tipográficas y lumínicas mediante transformaciones lineales sobre los píxeles.

- *binarizacion.py:* Modula cortes binarios puros para aislar de forma tajante el fondo del texto.

- *gaussiano.py:* Suaviza imperfecciones de alta frecuencia y ruido digital.

**Centralización mediante el Orquestador**

Para evitar llamadas cruzadas y proteger el estado del archivo original, se implementó la clase OpenCVProcessor dentro de:

- *orquestador_filtros.py:* Esta clase actúa como la interfaz unificada del sistema de filtros. Hereda de todos los filtros atómicos (BrilloContraste, EscalaGrises, Binarizar, FiltroGaussiano) y gestiona de manera interna la lectura física (OpenCVImageReader) y el almacenamiento seguro de la matriz _image.

### 2- MODULARIZACIÓN DEL MOTOR DE OCR (CONTRIBUCIÓN: JUAN MANUEL)
En paralelo, Juan Manuel lideró el proceso de descomposición y modularización de la clase original OCRProcesador (anteriormente monolítica) que él mismo habia iniciado en primera instancia, separándola en subcomponentes especializados bajo el Principio de Responsabilidad Única (SRP).

**Estructura del Ecosistema Modular de OCR**

La lógica de procesamiento profundo para visión artificial se dividió en tres archivos especializados e independientes:

- *procesador_imagen.py (ProcesadorImagen):* Dedicado exclusivamente al diagnóstico y tratamiento del aspecto visual. Calcula de manera automatizada las métricas de calidad de la imagen: brillo promedio y nitidez/desenfoque (utilizando la varianza del Laplaciano). Asimismo, contiene las herramientas de rescate adaptativo como apply_clahe (ecualización adaptativa del contraste por bloques) y denoise (filtro de mediana).

- *procesador_morfologico.py (ProcesadorMorfologico):* Especializado en las alteraciones geométricas y espaciales del documento. Implementa adaptive_threshold (binarización Gaussiana local para hojas con iluminación heterogénea) y deskew (detección del ángulo de los píxeles y rotación automática para enderezar el texto inclinado).

- *OCR_Procesador.py (OCRProcesador):* Redefinido como un Orquestador de Alto Nivel. Su único rol actual es coordinar el orden de ejecución de los métodos de las clases anteriores tras instanciarlas en su constructor (self.procesador_imagen y self.procesador_morfologico).

### 3- INTEGRACIÓN GENERAL Y REFACTORIZACIONES CLAVE (CONTRIBUCIÓN PAULA)
El mayor desafío técnico radicó en acoplar de forma armónica los módulos de Alejandro y Juan Manuel dentro de la clase coordinadora PipelineProcesamiento (dentro de pipeline_procesamiento.py). Durante este proceso de integración se detectaron e intervinieron dos puntos críticos:

**Transición a Comunicación en Memoria vía Base64**

Se eliminó el cuello de botella físico en las previsualizaciones en vivo (Live Preview). Anteriormente, la aplicación guardaba archivos temporales en disco de forma constante, provocando bloqueos de lectura/escritura (I/O) y degradando la performance del frontend (script.js).

**Solución:** Se implementó cv2.imencode('.jpg', imagen_cv2) para compilar los cambios directamente en un búfer de la memoria RAM, codificándolos a cadenas de texto Base64 transferibles a través de JSON. El navegador ahora renderiza los filtros en tiempo real sin tocar el almacenamiento secundario.

**Centralización Dimensional: Estandarizador vs. Upscale**

Se detectó un conflicto de redimensionamiento doble: 
OCRProcesador intentaba ejecutar un reescalado correctivo de emergencia (upscale_image multiplicando de forma fija por fx=2) si el ancho era menor a 1200px, mientras que existía una clase Estandarizador inactiva en el flujo.

**Solución y Justificación Técnica:** Se determinó que modificar las dimensiones en dos puntos distintos pixelaba la tipografía y falseaba los umbrales adaptativos de OpenCV. Se procedió a comentar completamente el método upscale_image de procesador_imagen.py.

En su lugar, se activó y priorizó de forma obligatoria la clase Estandarizador (derivada de Inicializador) al inicio de la función preparar_imagen_para_ocr. Esta clase opera bajo Pillow aplicando el filtro LANCZOS para unificar el ancho de cualquier documento a un estándar de 1500px. El uso de LANCZOS en esta etapa preventiva garantiza la conservación de bordes tipográficos limpios, estabilizando los cálculos de CLAHE y filtros morfológicos subsiguientes.

### ADHESIÓN DE BUENAS PRÁCTICAS DE INGENIERÍA DE SOFTWARE
Para asegurar que el sistema sea mantenible y cumpla con estándares profesionales de desarrollo de software, se implementaron de forma transversal las siguientes directrices:

- *Desacoplamiento de Librerías:*
Se respetó la especialización de herramientas; Pillow se configuró exclusivamente para la entrada estructural, lectura nativa y normalización dimensional rápida de archivos (Estandarizador), mientras que OpenCV absorbió en su totalidad la manipulación densa de matrices de píxeles y operaciones binarias.

- *Encadenamiento de Métodos (Method Chaining):* Métodos como estandarizar() en la clase Estandarizador devuelven la instancia de la propia clase (return self), permitiendo una sintaxis limpia y fluida durante el flujo del pipeline.

- *Documentación Bajo Estándar Google Style:* Se eliminaron los comentarios redundantes en el código y se sustituyeron por bloques formales de Docstrings en todas las funciones principales del pipeline, detallando contextualmente la intención del algoritmo, sus parámetros (Args:) y sus salidas (Returns:).

### CONCLUSIONES E IMPACTO TÉCNICO
La arquitectura final del proyecto ha quedado segmentada en una línea de producción predecible y robusta:

- *Estandarización (Preventiva - Pillow):* Normaliza el documento a 1500px de ancho preservando la tipografía con LANCZOS.

- *Filtros Manuales (Interactivo - Alejandro):* Permite al usuario limpiar visualmente el lienzo en memoria (Base64).

- *Inspección de Calidad (Diagnóstico - Juan Manuel):* Analiza brillo y ruido de forma matemática.

- *Optimización Morfológica (Geométrica - Juan Manuel):* Binariza de forma adaptativa y endereza el documento.

- *Extracción (OCR - Tesseract):* Procesa un documento de alto contraste, libre de ruido y perfectamente horizontal.

Los resultados experimentales demostraron que al procesar las imágenes bajo esta jerarquía estricta, la tasa de falsos positivos en el reconocimiento de caracteres disminuye drásticamente, erradicando la lectura de "ruido o basura digital" y transformando el código en un activo de software escalable y eficiente.
