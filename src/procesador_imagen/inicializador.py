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
