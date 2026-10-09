from infraestructura.conexion import obtener_conexion

def inicializar_bd():
    with obtener_conexion() as conn:
        conn.execute("DROP TABLE IF EXISTS empleado;")
        conn.execute("DROP TABLE IF EXISTS persona;")
        
        conn.execute("""
            CREATE TABLE IF NOT EXISTS persona (
                rut TEXT PRIMARY KEY,
                nombre TEXT NOT NULL
            );
        """)
        
        conn.execute("""
            CREATE TABLE IF NOT EXISTS empleado (
                rut TEXT PRIMARY KEY,
                fecha_ingreso TEXT NOT NULL,
                sueldo_base REAL NOT NULL,
                FOREIGN KEY (rut) REFERENCES persona(rut) ON DELETE CASCADE
            );
        """)
        conn.commit()
    print("Tablas 'persona' y 'empleado' creadas correctamente.")

if __name__ == "__main__":
    inicializar_bd()