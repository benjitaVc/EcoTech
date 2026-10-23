from infraestructura.conexion import obtener_ruta_bd
from dominio.excepciones import EcoTechError

if __name__ == "__main__":
    try:
        print("Base configurada:", obtener_ruta_bd())
    except (EcoTechError, OSError) as error:
        print("No se pudo leer la configuración:", error)
