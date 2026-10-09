import os
import sqlite3

# Apunta a ecotech.db directamente en la raíz del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "ecotech.db")

def obtener_conexion():
    """Devuelve una conexión a la base de datos SQLite."""
    return sqlite3.connect(DB_PATH)