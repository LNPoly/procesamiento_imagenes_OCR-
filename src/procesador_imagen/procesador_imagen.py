# aqui va la logica del procesamiento de imagenes, se pueden agregar funciones para mejorar la calidad de la imagen,
# eliminar ruido, etc.
from PIL import Image

class Inicializador:
    
    def __init__(self, url: str) :
        self._url = url
        self._imagen = Image.open(url)

    def guardar(self, new_url:str):        
        self._imagen.save(new_url)
        return self
    
    def reseteo(self):
        self._imagen = Image.open(self._url)
        return self


#Estandarización de tamaños. 
#Esta función toma una imagen y la redimensiona a un tamaño específico, manteniendo la relación de aspecto original.

class Estandarizador(Inicializador):
    
    def estandarizar(self, ancho_objetivo=1500) -> "Estandarizador":
        ancho_orig, alto_orig = self._imagen.size
        
        proporcion = ancho_objetivo / float(ancho_orig)
        alto_nuevo = int(float(alto_orig) * proporcion)
        
        # Redimensionar usando un filtro de alta calidad
        # Resampling.LANCZOS es el mejor para mantener nitidez en texto
        self._imagen = self._imagen.resize((ancho_objetivo, alto_nuevo), Image.Resampling.LANCZOS)
        
        print(f"Imagen reescalada a: {ancho_objetivo}x{alto_nuevo} (Manteniendo proporción)")
        return self
