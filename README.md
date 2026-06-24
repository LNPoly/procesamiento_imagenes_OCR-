<img width="1780" height="383" alt="image" src="https://github.com/user-attachments/assets/abb75db6-b36a-4fd9-98ab-e3a9a0df7b81" />

## Objetivo y característica general

El procesador evalúa, analiza y extrae el texto que se encuentra plazmado en una imagen a través de distintos métodos de procesamiento de imagenes en el cual convierten cada pixel de la imagen en un parametro legible para poder identificar palabras u oraciones que son guardadas en un archivo de texto listo para su uso.

## **Enfoque Arquitectónico** 
Programación Orientada a Objetos (POO), Arquitectura Modular, Pipeline de Procesamiento Lineal y Desacoplado.  

---

## STACK TECNOLÓGICO (DEPENDENCIAS)

El proyecto utiliza un ecosistema robusto basado en **Python 3.x** enfocado en el desarrollo web y la visión por computadora. A continuación se detallan las librerías principales y sus dependencias de soporte según el archivo `requirements.txt`:

| Tecnología / Librería | Versión | Categoría | Descripción / Rol en el Proyecto |
| :--- | :--- | :--- | :--- |
| **Flask** | `3.1.3` | Servidor / Web Framework | Framework principal encargado de levantar el servidor web, gestionar las rutas HTTP y la API del pipeline. |
| **OpenCV (`opencv-python`)** | `4.13.0.92` | Visión Artificial / Core | Motor principal para la manipulación densa de matrices de píxeles, binarización adaptativa, deskew y filtros manuales. |
| **Pillow (`pillow`)** | `12.2.0` | Procesamiento de Imágenes | Utilizada para la carga/guardado nativo y la estandarización estructural de dimensiones con remuestreo de alta fidelidad (`LANCZOS`). |
| **PyTesseract** | `0.3.13` | Extracción de Texto (OCR) | Interfaz de comunicación encargada de enviar la imagen final optimizada hacia el motor Tesseract OCR. |
| **NumPy** | `2.4.4` | Computación Científica | Soporte matemático fundamental para manejar y procesar las imágenes como arrays/matrices multidimensionales. |
| **Werkzeug** | `3.1.8` | Infraestructura Web | Librería subyacente de Flask que maneja el enrutamiento WSGI, la seguridad de nombres de archivos (`secure_filename`) y depuración. |
| **Jinja2** | `3.1.6` | Motor de Plantillas | Motor de Flask encargado de renderizar dinámicamente las vistas HTML en el frontend. |
| **Click** | `8.4.1` | Utilidades de Consola | Herramienta interna para la creación de interfaces de línea de comandos integradas con Flask. |
| **Itsdangerous** | `2.2.0` | Seguridad criptográfica | Permite el firmado seguro de tokens de datos y cookies para resguardar la integridad de las peticiones HTTP. |
| **MarkupSafe** | `3.0.3` | Seguridad Web | Se encarga de escapar caracteres especiales en el HTML para prevenir vulnerabilidades de inyección de código (XSS). |
| **Blinker** | `1.9.0` | Utilidades del Core | Proporciona un sistema rápido de emisión y suscripción de señales internas dentro del ciclo de vida de Flask. |
| **Colorama** | `0.4.6` | Utilidades de Terminal | Añade soporte tipográfico de colores a los logs del sistema en la terminal, agilizando el proceso de *debugging*. |
| **Packaging** | `26.2` | Utilidades del Core | Gestiona internamente las directivas de compatibilidad de metadatos y versiones entre los paquetes instalados. |

---

## 3. GUÍA DE INSTALACIÓN Y CONFIGURACIÓN

Seguí estos pasos en orden para configurar el proyecto en tu entorno local. El sistema requiere la instalación de un motor externo de OCR y la preparación de un entorno aislado de Python.

### Paso 1: Prerrequisitos del Sistema (Tesseract OCR)

PyTesseract es una interfaz, pero requiere que el motor ejecutable de **Tesseract OCR** esté instalado en tu sistema operativo.

#### En Windows:
1. Descargá el instalador de 64 bits desde el repositorio oficial de [UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki).
2. Durante la instalación, asegurate de marcar la casilla de **"Additional script data"** y **"Additional language data"** seleccionando **Spanish** (español) para que reconozca correctamente los caracteres con tildes y eñes (`spa`).
3. Anotá la ruta donde se instaló (por defecto suele ser `C:\Program Files\Tesseract-OCR\tesseract.exe`).

#### En Linux (Ubuntu/Debian):
Ejecutá en la terminal el comando para instalar el motor y el paquete de idioma en español:
```bash
sudo apt update
sudo apt install tesseract-ocr tesseract-ocr-spa
```
### Paso 2: Clonación del repo y la creación del entorno virtual (.env)

```bash
git clone <URL_DE_TU_REPOSITORIO>
cd <NOMBRE_DE_LA_CARPETA_DEL_PROYECTO>

python -m venv venv
````
Activá el entorno virtual según tu sistema operativo:
- Windows (CMD)
````
venv\Scripts\activate
````
- Windows powerShell
````
.\venv\Scripts\activate
````
- En Linux o macOS
````
source venv/bin/activate
````
### Paso 3: Instalación de dependencias
```
pip install --upgrade pip
pip install -r requirements.txt
```
### Paso 4: Vinculación con Tesseract
Para que el servidor Flask sepa exactamente dónde encontrar el motor de OCR, abrí el archivo de configuración del proyecto (src/config.py o donde se encuentre tu objeto config) y editá la variable TESSERACT_CMD con la ruta de tu instalación:
- En Windows
```
TESSERACT_CMD = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```
- En Linux
  (por lo general se detecta automáticamente si está en el PATH, pero podés forzarlo):
````
TESSERACT_CMD = "/usr/bin/tesseract"
````

### Paso 5: Ejecución de la aplicación:
Una vez completados los pasos anteriores, ya podés levantar el servidor local de Flask ejecutando el archivo principal:
````
python main.py
````
Abrí tu navegador web e ingresá a la dirección de localhost:5000

---

# Modo de uso del programa

#### **Selección de imagen a analizar**
Dentro de la página donde dice **"selecciona una imágen para analizar"**, puedes hacer click en *"seleccinar archivo"* para poder elegir una imagen dentro del explorador de archivos.
- Las imágenes que se utilizaron para éste proyecto están en la ruta: /data/img_originales

**Aplicación de filtros manuales (opcionales)**

Una vez elegida la imagen, se da una vista previa de la imagen elegida y un menú desplegable para poder aplicar, o no, los filtros manuales como *escala de grises*, *binarización*, *reducción de ruido* y el *brillo/contraaste*, a éste último filtro usarlo con precaución ya que puede afectar al resultado del procesamiento si la imagen es muy clara.

La confirmación de la aplicación del filtro se puede visualizar en la vista previa de imagen y debajo del botón descargar, el cual también puede elegir guardar la versión de la imagen con el filtro/os aplicados.

**Resultado final**

Una vez que se hayan aplicado los filtros se procede a accionar el botón de **"terminar de editar"** y acto seguido hacer click nuevamente en el botón **"subir y procesar"** para poder visualizar el resultado del OCR más la imagen final con la descripcion de metricas y el texto identificado.


