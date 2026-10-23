import sqlite3
from infraestructura.conexion import transaccion, obtener_ruta_bd
from dominio.excepciones import EcoTechError

if __name__ == "__main__":
    try:
        print("Base de datos:", obtener_ruta_bd())
        with transaccion() as conn:
            tablas = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
            print("Tablas:", [tabla[0] for tabla in tablas])
            print("Claves foráneas activas:", conn.execute("PRAGMA foreign_keys").fetchone()[0])
            print("Problemas de integridad:", conn.execute("PRAGMA foreign_key_check").fetchall())
    except (EcoTechError, sqlite3.Error, OSError) as error:
        print("No se pudo verificar la base:", error)
