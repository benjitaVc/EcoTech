import os
from dotenv import load_dotenv


load_dotenv()


nombre_bd = os.getenv("DB_NOMBRE")

print(f"Base de datos configurada: {nombre_bd}")