# Informe sobre consultas a la IA y recomendaciones

Se realizaron distintas consultas en distintos momentos del desarrollo del proyecto. A consitunación se describe las consultas principales:

## Estructura
Se le pidió asesoramiento acerca de la estructura actual del proyecto y recomendó empezar a delegar responsabilidades ya que el proyecto iba a aumentar de tamaño.
Decisión tomada en cuenta posteriormente debido a que el proyecto ya tenia módulos de procesamiento importantes y saturaban visualmente por la cantidad de líneas de Código.

## Fraccionamiento
Se le consultó sobre buenas prácticas para el fraccionamiento del main.py.
Recomendó gestionar las rutas y creaciones de carpetas y archivos permitidos en un módulo con un archivo config.py el cual fue tenido en cuenta ya que ayudó a alivianar de forma visual parte del código main. 
Se tomó n cuenta el archivo config.py que estaba creado pero vacío desde un primer momento y con la recomendación de la IA se aceptó usarlo para la gestión de constantes y rutas.
## Tesseract
Se le consulto y pidió información sobre la instalación de Tesseract en un entorno Linux. Mostró diferencias entre rutas y resalto una de ellas como la “opción” más segura para la instalación.
Se tomó en cuenta la ruta “mas segura” para el entorno Linux y además se le consulto al docente por el asesoramiento y que no tuviera problemas al ejecutar el proyecto.
## Integración
Se le consulto acerca de cómo integrar el trabajo realizado por otro integrante del grupo con buenas prácticas, además de explicarle la idea o propuesta de la función que iban a cumplir el trabajo que realizó el compañero de equipo.
Recomendó usar clases abstractas para que el “orquestador” no ejecute métodos incorrectos.

A razón de esta nueva recomendación se le pidió lo siguiente:
## Información comparativa (Clase abstracta vs Clase estática)
Se le pidió que explique el uso de las clases abstractas y estáticas ya que al inicio se optó por esta última y así poder entender las diferencias entre las clases / métodos. 
Se continuó con las clases estáticas y se tuvo en cuenta la información que brindó para una posible modificación a futuro.

## Configuración de Tesseract y ejemplo
Se le pidió que explique acerca de cómo se puede lograr exactitud con Tesseract al momento de realizar la detección de texto en las imágenes. Como tenía desconocimiento acerca de qué tipo de sintaxis utilizar, es aquí en donde se le pidió un ejemplo para poder entender como establecer el parámetro de configuración correcta de la variable para el proyecto. 
## Parametro Threshold
Se tuvo en cuenta la explicación que brindó acerca de establecer un umbral adaptativo para poder reducir el ruido de la imagen limpiándola.
## Modificación de imagen en Preview
Tras una serie de modificaciones en el código que nos obligo a armar una carpeta de imágenes previas, decidimos pedir asesoramiento con el fin de poder evitar el guardado de imágenes que no van a ser utilizadas por el OCR.
En este caso nos recomendó usar base64 con el fin de evitar ocupar mas espacio. Se tuvo en cuenta esta opción para así evitar la creación de mas variables.

## Consultas extra 
Además se armó otro chat para centralizar las consultas e información sobre la interfaz también se le consultó sobre el armado y configuración de la interfaz informandole sobre la estética a utilizar con paleta de color específica.

Se le consulta sobre el armado de un background combinado con gradientes si la tecnica que se iba a utilizar estaba correcta y además sobre el uso del z-index para poder aplicarlo de forma correcta.


# Links

**Conversación general sobre código**
https://share.gemini.google/iheoVD6oZMdJ

**Conversación sobre la interfaz**
https://share.gemini.google/DHzS8Zjz7yvg
