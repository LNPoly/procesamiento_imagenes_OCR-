# INFORME DE RESULTADOS

## 1- Análisis Comparativo: Propuesta vs. Resultados Obtenidos
Al contrastar el documento de la propuesta inicial con la arquitectura y el código fuente entregado, se observa un alto grado de cumplimiento en las etapas fundamentales del proyecto, con algunas desviaciones lógicas propias del ciclo de desarrollo.

### ✅ Objetivos Cumplidos (Implementados con éxito)
- **Preprocesamiento Avanzado:**
La propuesta establecía el uso de bibliotecas como OpenCV y Pillow para la mejora de calidad (escala de grises, binarización, eliminación de ruido y ajuste de contraste). Esto se logró exitosamente a través de una arquitectura modular sólida, evidenciada en las clases ProcesadorImagen (para contraste CLAHE y Denoise), ProcesadorMorfologico (para binarización adaptativa y deskew) y el Estandarizador (para normalización de dimensiones con LANCZOS).

- **Implementación del Motor OCR:** Se cumplió con el objetivo de integrar Tesseract OCR para la extracción del texto. El pipeline actual toma la imagen limpia y genera los resultados esperados.

- **Generación de Archivos (.txt):** El sistema cumple con el objetivo general de convertir las imágenes en formatos digitales editables (.txt). La estructura del proyecto demuestra que los resultados se almacenan correctamente en el directorio /uploads/textos/.

### ⚠️ Objetivos Parciales o Pendientes

- **Interfaz Gráfica:** Si bien la propuesta indicaba que no se contemplaba una interfaz gráfica avanzada en esta etapa, el equipo logró implementar una vista web funcional (Flask + HTML/JS). No obstante, aún requiere ajustes de usabilidad (como el botón de descarga) y adaptabilidad.

- **Etapa 3 Postprocesamiento de texto con IA:** La propuesta mencionaba la aplicación de técnicas de Inteligencia Artificial para corregir errores ortográficos y estructurar el texto. En el código backend actual, el foco principal estuvo en el tratamiento previo de la imagen, quedando la corrección semántica posterior como un área potencial para futuras integraciones.

## 2- Oportunidades de Mejora y Trabajo Futuro

Al evaluar la problemática inicial y contrastarla con el estado actual del sistema al momento de la entrega, se han identificado las siguientes áreas de optimización para futuras iteraciones del proyecto:

- **Descarga directa de resultados desde la interfaz:** Actualmente, el sistema procesa la imagen y almacena de forma automática el texto extraído en un archivo .txt (conservando el nombre original de la imagen) dentro del servidor. Debido a los tiempos de desarrollo, queda pendiente la implementación de un botón en el frontend que permita al usuario descargar este archivo directamente desde su navegador de forma intuitiva.

- **Ampliación del soporte multilingüe:** El motor de reconocimiento óptico se encuentra configurado y focalizado exclusivamente en la detección de texto en idioma español. Como evolución natural del sistema, se proyecta integrar nuevos diccionarios de datos en Tesseract para habilitar el soporte a múltiples idiomas, ampliando así el alcance de la herramienta.

- **Diseño Adaptativo (Responsive Design):** Se requieren correcciones generales en las hojas de estilo de la interfaz web para garantizar que la aplicación sea completamente responsive, asegurando una experiencia de usuario óptima independientemente del tamaño de pantalla o dispositivo utilizado.

## 3- Conclusión

Este proyecto demuestra cómo la integración estratégica de técnicas de visión artificial (OpenCV), procesamiento nativo de imágenes (Pillow) y motores de reconocimiento óptico (PyTesseract) puede transformar datos visuales estáticos en información digital estructurada, editable y de calidad.

A lo largo del desarrollo, logramos evolucionar de un sistema monolítico a una **arquitectura modular y escalable**. Al separar las responsabilidades —desde la estandarización preventiva hasta la limpieza interactiva y la binarización adaptativa— construimos un *pipeline* que garantiza que el motor de OCR reciba siempre la mejor versión posible del documento, maximizando así la precisión de lectura y minimizando los falsos positivos por "ruido digital".

Para cerrar, esta aplicación no solo representa una solución funcional y lista para operar, sino que sienta unas bases arquitectónicas sólidas para futuras iteraciones, como la incorporación de soporte multilingüe y el postprocesamiento semántico con Inteligencia Artificial.