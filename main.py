from src.procesador_imagen.procesador_imagen import Inicializador, Estandarizador

def main():
    #IMPORTANTE:
    # por ahora estas rutas estan hardcodeadas, despues cuando haga la interfaz, vamos a probar desde ahi.
    
    ruta_entrada = "./data/img_original/texto1.jpg"
    ruta_salida = "./data/img_procesada/estandarizada.png"

    imagen = Estandarizador(ruta_entrada)
    imagen.estandarizar(1500).guardar(ruta_salida)
    
    print("Proceso completado con éxito.")

if __name__ == "__main__":
    main()