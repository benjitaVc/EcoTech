import sqlite3
import os
from dotenv import load_dotenv

# Cargar configuración desde .env
load_dotenv()

nombre_bd = os.getenv("DB_NOMBRE")

# Conectar a la base de datos
conn = sqlite3.connect(nombre_bd)

# Leer y ejecutar el archivo del esquema SQL
with open("db/01_esquema.sql", "r", encoding="utf-8") as f:
    esquema_sql = f.read()

conn.executescript(esquema_sql)
conn.close()

print("Base de datos e infraestructura de tablas creadas correctamente.")