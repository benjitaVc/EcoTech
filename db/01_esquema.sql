CREATE TABLE IF NOT EXISTS departamento (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS empleado (
    rut TEXT PRIMARY KEY,
    fecha_ingreso DATE NOT NULL,
    sueldo_base INTEGER NOT NULL,
    departamento_id INTEGER,
    FOREIGN KEY (departamento_id) REFERENCES departamento(id)
);