# Preprocesamiento de Imágenes para OCR

### Descripción General

Este tiene como objetivo preparar imágenes para pasarlas a un OCR que se encarga de traducir una imagen de texto a un archivo editable de txt o similar. La calidad de una imagen influye directamente en la capacidad del motor OCR para identificar correctamente letras, números y símbolos. Imágenes con baja iluminación, ruido, desenfoque o inclinación suelen generar errores de reconocimiento, por lo que resulta necesario aplicar una serie de transformaciones previas antes de ejecutar el OCR.

El diseño implementado sigue un enfoque modular basado en clases, donde cada una de ellas posee una responsabilidad específica dentro del proceso, permitiendo mantener una estructura desacoplada, reutilizable y fácilmente extensible. El flujo completo se encuentra coordinado por la clase OCRProcesador, que actúa como orquestador del pipeline de procesamiento.

### El diseño
Se aplicó una lógica de agrupar filtros en clases que transforma la imagenes en ciertos aspectos como es la calidad visual de las misma y en otra las que se enfocan en las transformaciones morfológicas así que tenemos tres componentes principales:

- ### ProcesadorImagen
Encargado del análisis de calidad y mejora visual de la imagen.

- ### ProcesadorMorfologico
Responsable de las transformaciones espaciales y la binarización.

- ### OCRProcesador
Coordina el flujo completo de procesamiento.

La separación permite llevar adelante la responsabilidad única donde cada clase se ocupa exclusivamente de una tarea específica dentro del sistema.

# Procesamiento general

- Carga de la imagen.
- Análisis de calidad visual.
- Corrección adaptativa de contraste.
- Reducción de ruido.
- Binarización mediante umbral adaptativo.
- Corrección de inclinación del documento.
- Guardado de la imagen procesada.

Se busca como objetivo general  obtener una imagen limpia, con alto contraste, libre de ruido e inclinaciones, para usar de insumo en el OCR.

## En éste proyecto se utiliza

- clipLimit = 2.0:  valor aconsejado para obtener un equilibrio adecuado entre mejora visual y estabilidad.

- Parámetro tileGridSize:
El parámetro tileGridSize determina en cuántas regiones se divide la imagen para realizar la corrección local.

- tileGridSize = (8,8):
La imagen se divide en una cuadrícula de ocho filas por ocho columnas, permitiendo corregir de forma independiente diferentes zonas del documento.

- Método denoise():
Este método elimina el ruido utilizando el algoritmo Non-Local Means.
La técnica compara regiones similares de la imagen para eliminar pequeñas perturbaciones visuales sin destruir los detalles importantes del texto.

- Parámetro h:
El parámetro h controla la intensidad de la reducción de ruido, valores bajos realizan una limpieza ligera mientra que altos eliminan más ruido, pero pueden borrar detalles finos de los caracteres.

## Clase ProcesadorImagen

La clase ProcesadorImagen tiene como función analizar las características visuales de la imagen y aplicar mejoras cuando sea necesario.

Antes de modificar una imagen, se evalúa su calidad por medio de métricas objetivas, permitiendo que las transformaciones se realicen únicamente cuando son realmente necesarias.

- *Método analizar_imagen():*
Este método entrega diferentes métricas que describen la calidad de la imagen al inicio del proceso.

- *Brillo (Brightness):*
El brillo se calcula obteniendo el promedio de intensidad de todos los píxeles de la imagen en escala de grises siendo 0=negro y 255=blanco, indicando un valor bajo una imagen oscura y alto iluminada. Esta métrica se utilizará posteriormente para decidir si es necesario aplicar técnicas de mejora de contraste.

- *Nitidez (Blur):*
La nitidez se mide mediante la varianza del operador Laplaciano.
El Laplaciano es un detector de bordes. Las imágenes nítidas presentan muchos cambios bruscos de intensidad y, por lo tanto, generan valores altos de varianza. Las imágenes desenfocadas presentan menos bordes definidos y producen valores menores. Con esta métrica se estima el nivel de desenfoque de la imagen.

- *Dimensiones:*
Se registran el ancho y alto de la imagen para controlar que el archivo de origen posea una resolución adecuada para el OCR.

- *Método apply_clahe():*
Este método aplica CLAHE (Contrast Limited Adaptive Histogram Equalization).
El objetivo principal es aumentar el contraste entre el texto y el fondo de la imagen: A diferencia de una ecualización tradicional, CLAHE trabaja por regiones independientes de la imagen, permitiendo corregir zonas con iluminación desigual.

- *Parámetro clipLimit:*
El parámetro clipLimit controla la intensidad máxima del aumento de contraste.
Valores bajos generan mejoras suaves, mientras que valores altos pueden producir resultados artificiales o amplificar el ruido existente.


## Clase ProcesadorMorfologico

La clase ProcesadorMorfologico realiza transformaciones espaciales sobre la imagen para facilitar el reconocimiento de caracteres.

Sus principales funciones son:

- Convertir la imagen en blanco y negro.
- Corregir inclinaciones del documento.

### Método adaptive_threshold()

Este método transforma una imagen en escala de grises en una imagen binaria.

La binarización consiste en convertir cada píxel en uno de dos únicos valores 0 para negro  255 para blanco, la eliminación de tonos intermedios es altamente recomendada para trabajar  en OCR.

#### Parámetro maxValue

Se utiliza el valor 255 que representa el color blanco en la imagen resultante.

#### Parámetro adaptiveMethod

Se emplea:

- cv2.ADAPTIVE_THRESH_GAUSSIAN_C :
Este método calcula el umbral utilizando una media ponderada de los píxeles vecinos los píxeles más cercanos tienen mayor influencia que los más alejados, generando resultados más robustos ante variaciones de iluminación.

- Parámetro thresholdType = cv2.THRESH_BINARY :
Todo píxel superior al umbral calculado se convierte en blanco y el resto en negro.

- Parámetro blockSize = 51 :
Este parámetro define el tamaño de la ventana local utilizada para calcular el umbral adaptativo donde cada píxel es evaluado considerando una región de 51 × 51 píxeles alrededor suyo y el valor debe ser impar para garantizar que exista un píxel central.

- Parámetro C = 2 :
Este valor se resta del promedio local calculado y permite ajustar la sensibilidad del umbral adaptativo y mejorar la separación entre texto y fondo.

### Método deskew()

Las imágenes suelen presentar pequeñas inclinaciones y estas inclinaciones reducen considerablemente la precisión cuando son enviadas al OCR. El método deskew() detecta automáticamente el ángulo dominante del texto y corrige la distorsión.

- Detección del ángulo:
La detección se realiza identificando todos los píxeles pertenecientes al contenido de la imagen y calculando el rectángulo mínimo que los contiene, a partir de este rectángulo se obtiene el ángulo de inclinación.

- Rotación: 
La corrección se realiza mediante una matriz de transformación afín donde una matriz describe matemáticamente cómo debe rotarse la imagen alrededor de su centro.

- Interpolación:
Durante la rotación se utiliza: 
    - cv2.INTER_CUBIC :
Este método genera nuevos píxeles mediante interpolación cúbica, produciendo resultados de alta calidad y preservando mejor los detalles de los caracteres.

    - Manejo de Bordes: utiliza cv2.BORDER_REPLICATE
Cuando una imagen rota aparecen espacios vacíos en los bordes y esta configuración llena dichos espacios replicando los píxeles vecinos, evitando la aparición de franjas negras que deterioran la calidad buscada.

## Clase OCRProcesador

La clase OCRProcesador actúa como coordinador general pipeline u orquestador y su responsabilidad consiste en decidir qué transformaciones deben aplicarse y en qué orden. La estructuración diseñada de esta manera facilita el mantenimiento y permite modificar o ampliar el flujo sin afectar las clases especializadas.

### Parámetros de Configuración

- min_width = 1200: píxeles se utiliza para controlar el ancho mínimo aceptable de una imagen.
La funcionalidad de reescalado se encuentra deshabilitada debido a que esta tarea es realizada previamente por la clase Estandarizador.

- dark_threshold:
Valor umbral para determinar si una imagen es considerada oscura.
    - Configuración: 100 si el brillo promedio es inferior a este valor, se aplica CLAHE automáticamente.

- blur_threshold:
Valor umbral utilizado para determinar si una imagen posee una nitidez insuficiente.

    - Configuración: 80 si la nitidez es inferior a este valor, se ejecuta el proceso de reducción de ruido.

Al finalizar el procesamiento de una imagen se espera:

- Mejor contraste entre texto y fondo.
- Menor presencia de ruido visual.
- Binarización optimizada para usar en OCR.
- Corrección automática de inclinación.
- Conservación de detalles relevantes de los caracteres.

Las transformaciones descriptas buscan incrementar significativamente la calidad de entrada de las imágenes al OCR, con un claro objetivo de reducir errores de reconocimiento en los textos y mejorar la precisión general de la conversión de una fotografía de un texto a un archivo editable.
