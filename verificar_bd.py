import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()
nombre_bd = os.getenv("DB_NOMBRE")

conn = sqlite3.connect(nombre_bd)
cursor = conn.cursor()

# Consultar las tablas existentes en la base de datos
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tablas = cursor.fetchall()

print("Tablas encontradas en la base de datos:")
for tabla in tablas:
    print(f"- {tabla[0]}")

conn.close()