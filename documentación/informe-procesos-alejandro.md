# Informe sobre procesos de filtrado manual 
### Descripción General
Este módulo tiene como objetivo aplicar transformaciones de matriz y filtros analógicos a las imágenes antes de pasarlas al motor OCR, el cual se encarga de traducir una imagen de texto a un archivo editable. La calidad de una imagen influye directamente en la capacidad del motor OCR para identificar correctamente letras, números y símbolos. Imágenes con baja iluminación, ruido o canales de color complejos suelen generar errores de reconocimiento, por lo que resulta necesario aplicar una serie de transformaciones previas antes de ejecutar el OCR.

El diseño implementado sigue un enfoque modular basado en clases, donde cada una de ellas posee una responsabilidad específica dentro del proceso, permitiendo mantener una estructura desacoplada, reutilizable y fácilmente extensible. El flujo completo se encuentra coordinado por la clase OpenCVProcessor, que actúa como orquestador del pipeline de procesamiento.

El diseño se basa en agrupar filtros en una clase que transforma las imágenes en aspectos clave como la escala cromática, la reducción de ruido, la iluminación y la binarización, contando con un componente principal:
- **OpenCVProcessor:** encargado del análisis de estado, carga/guardado seguro y aplicación secuencial de efectos visuales.

**Procesamiento general**
1.  Carga de la imagen.
2.	Validación preventiva de existencia.
3.	Conversión a escala de grises.
4.	Reducción de ruido mediante suavizado gaussiano.
5.	Ajuste lineal de brillo y contraste.
6.	Binarización mediante umbral absoluto.
7.	Guardado de la imagen procesada.

Se busca como objetivo general obtener una imagen limpia, de un solo canal, libre de ruido e impurezas, para usar de insumo en el OCR.
## Clase OpenCVProcessor
Esta clase tiene como función coordinar el flujo completo de procesamiento de efectos y resguardar la imagen operativa dentro del atributo privado *self._image*. La estructuración diseñada de esta manera facilita el mantenimiento y permite modificar o ampliar el flujo sin afectar los métodos especializados.
- **Método _ensure_image_loaded():**
Este método actúa como un control de seguridad auxiliar y preventivo de estado antes de ejecutar cualquier filtro.

    - **Funcionamiento:** Evalúa si el atributo interno self._image es equivalente a None. Si la imagen no está cargada en memoria, detiene la ejecución arrojando una excepción de tipo RuntimeError, evitando fallos físicos o excepciones en cascada dentro de la librería OpenCV.
- **Método load_image():**
Este método se encarga de la lectura física del archivo y su alojamiento en el estado del procesador.
    - **Funcionamiento:** Delega la lectura en un componente OpenCVImageReader. Si la ruta provista no existe o el formato de imagen está roto, detecta que la matriz resultante es nula y lanza un ValueError alertando el error de origen en lugar de continuar con datos nulos.
- **Método save():**
Este método exporta los cambios de la matriz interna escribiendo el archivo final en el almacenamiento físico.
    -	**Funcionamiento:** Evalúa el atributo self._image antes de proceder. Si la imagen es nula, arroja un RuntimeError. La escritura física se realiza mediante cv2.imwrite; si la operación falla por falta de permisos o espacio en el disco, el método intercepta la falla y levanta una excepción de tipo IOError.

## Filtros
### Escala de grises
Este método convierte la matriz de la imagen color actual a un espacio monocromático de un solo canal para aislar la lógica de transformación cromática y reducir la complejidad computacional.

- **Lógica de control:**
Se inspecciona la dimensionalidad de la matriz mediante la propiedad len(self._image.shape) == 3. Si posee 3 canales correspondientes al espacio de color BGR, ejecuta la función cv2.cvtColor aplicando la bandera cv2.COLOR_BGR2GRAY. Si la estructura ya es bidimensional (blanco y negro nativo), se omite la conversión automática para evitar un colapso del sistema por incompatibilidad de dimensiones.

### Gaussiano
Este método desarrolla un filtro de limpieza analógica para eliminar perturbaciones visuales microscópicas y granizo digital utilizando un filtro de suavizado.
- **Funcionamiento:** Utiliza el algoritmo de desenfoque cv2.GaussianBlur para suavizar las transiciones de intensidad de la matriz, evitando que el motor OCR confunda pequeñas manchas con signos de puntuación reales.
- **Parámetro kernel_size = 5:** Determina el tamaño de la ventana cuadrada utilizada para promediar los píxeles vecinos. El valor debe ser un número impar positivo para garantizar que exista un píxel central de referencia.
- **Parámetro sigma = 0:** Indica a la librería que la desviación estándar del desenfoque se calcule automáticamente a partir de las dimensiones del kernel.
- **Validación de dimensión:** El código ejecuta un control estricto (kernel_size % 2 == 0 or kernel_size <= 0) arrojando un ValueError si el valor ingresado es par o negativo, lo que impide invocar la función de OpenCV con parámetros incorrectos.
### Brillo
Este método implemente una herramienta de corrección lumínica lineal para resolver defectos de exposición o sombras, incrementando la separación entre la tipografía y el fondo.
- **Funcionamiento:** Utiliza el operador matricial de OpenCV cv2.convertScaleAbs para transformar los píxeles de forma lineal sin desbordar los límites de intensidad, procesando la matriz en paralelo de forma eficiente.
- **Parámetro alpha:** Controla el nivel de contraste actuando como multiplicador de intensidad sobre el valor original del píxel para estirar la brecha entre tonos claros y oscuros.
- **Parámetro beta:** Controla el nivel de brillo actuando como una constante aditiva para iluminar u oscurecer la escena de manera uniforme.

### Binarización
Este método realiza el paso de preparación definitivo de la matriz, eliminando por completo todas las tonalidades grises intermedias para generar una imagen binaria pura.
- **Funcionamiento:** Invoca la función cv2.threshold para realizar la umbralización estricta que requiere el motor OCR para reconocer los caracteres de forma óptima.
- **Parámetro threshold = 127:** Define el límite numérico de corte para evaluar la intensidad. Todo píxel con intensidad superior se convierte en blanco puro (255) y el resto se transforma en negro absoluto (0).
- **Blindaje de canal:** Como resguardo de seguridad, si la imagen retiene 3 canales antes de este método (len(self._image.shape) == 3), se fuerza una conversión interna a escala de grises sobre una matriz_operativa antes de binarizar para asegurar el funcionamiento sin excepciones estructurales.
- 	**Asignación de estado:** El código descarta el primer valor retornado por la función mediante el uso de un guion bajo (_) y reasigna directamente la matriz resultante a self._image para actualizar el estado continuo de la clase.

Al finalizar el procesamiento de una imagen se espera:
- Blindaje preventivo en memoria ante ejecuciones vacías o datos nulos.
- Normalización estructural a un solo canal de grises libre de datos cromáticos redundantes.
- 	Eliminación de ruido visual y granizo digital mediante restricciones de kernel impares.
- 	Optimización de contraste lumínico para separar los caracteres del fondo del papel.
- 	Binarización estricta (valores 0 y 255) idónea para usar de insumo en el motor OCR.

Las transformaciones descritas buscan incrementar significativamente la calidad de entrada de las imágenes al OCR, con un claro objetivo de reducir errores de reconocimiento en los textos y mejorar la precisión general de la conversión de una fotografía de un texto a un archivo editable.
