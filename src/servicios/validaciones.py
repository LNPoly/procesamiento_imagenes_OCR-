import os
from src.servicios.gestor_archivos import es_archivo_valido

class Validaciones:
    
    """ Valida el archivo subido por el usuario, asegurándose de que cumpla con los requisitos necesarios para ser procesado.
    """
    
    @staticmethod
    def validar_archivo(files_dict, extensiones_permitidas):
        
        if 'image' not in files_dict:
            return False, 'No se envió ninguna imagen.'
        
        archivo = files_dict['image']
        
        if archivo.filename == '':
            return False, 'Nombre de archivo vacío.'
        
        if not es_archivo_valido(archivo.filename, extensiones_permitidas):
            return False, 'Extensión de archivo no permitida.'
            
        return True, None