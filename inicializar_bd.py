import sqlite3
from pathlib import Path
from dominio.excepciones import EcoTechError
from infraestructura.conexion import transaccion


def inicializar_bd():
    """Crea las tablas que faltan sin borrar los datos existentes."""
    archivo = Path(__file__).parent / "db" / "01_esquema.sql"
    with transaccion() as conn:
        for sentencia in archivo.read_text(encoding="utf-8").split(";"):
            if sentencia.strip():
                conn.execute(sentencia)


if __name__ == "__main__":
    try:
        inicializar_bd()
        print("Base de datos inicializada sin borrar registros.")
    except (EcoTechError, sqlite3.Error, OSError) as error:
        print("No se pudo inicializar la base:", error)
        raise SystemExit(1)
