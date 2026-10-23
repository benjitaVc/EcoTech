import os
import sqlite3
from pathlib import Path
from contextlib import contextmanager
from dominio.excepciones import ErrorConexionError

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = None  # La demo y las pruebas pueden elegir una base temporal.


def obtener_ruta_bd():
    if DB_PATH is not None:
        return str(DB_PATH)
    nombre = os.getenv("DB_NOMBRE")
    archivo_env = BASE_DIR / ".env"
    if nombre is None and archivo_env.exists():
        # Solo se necesita una variable; no se ejecuta el contenido del archivo.
        for linea in archivo_env.read_text(encoding="utf-8-sig").splitlines():
            linea = linea.strip()
            if linea and not linea.startswith("#") and "=" in linea:
                clave, valor = linea.split("=", 1)
                if clave.strip() == "DB_NOMBRE":
                    nombre = valor.strip().strip("\"'")
    if nombre is None:
        nombre = "ecotech.db"
    if not nombre.strip() or nombre.strip() == ":memory:":
        raise ErrorConexionError("DB_NOMBRE debe indicar un archivo SQLite.")
    ruta = Path(nombre.strip())
    if not ruta.is_absolute():
        ruta = BASE_DIR / ruta
    return str(ruta)


def obtener_conexion():
    conn = None
    try:
        conn = sqlite3.connect(obtener_ruta_bd())
        conn.execute("PRAGMA foreign_keys = ON")
        return conn
    except (sqlite3.Error, OSError) as error:
        if conn is not None:
            conn.close()
        raise ErrorConexionError(
            "No se pudo abrir la base. Revise DB_NOMBRE, la carpeta y sus permisos."
        ) from error


@contextmanager
def transaccion():
    conn = obtener_conexion()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
