CREATE TABLE IF NOT EXISTS departamento (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS persona (
    rut TEXT PRIMARY KEY NOT NULL CHECK (length(trim(rut)) > 0),
    nombre TEXT NOT NULL CHECK (length(trim(nombre)) > 0)
);

CREATE TABLE IF NOT EXISTS empleado (
    rut TEXT PRIMARY KEY NOT NULL,
    fecha_ingreso TEXT NOT NULL,
    sueldo_base REAL NOT NULL CHECK (sueldo_base >= 0),
    FOREIGN KEY (rut) REFERENCES persona(rut) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS registro_tiempo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    empleado_rut TEXT NOT NULL,
    fecha TEXT NOT NULL,
    horas REAL NOT NULL CHECK (horas > 0 AND horas <= 24),
    FOREIGN KEY (empleado_rut) REFERENCES empleado(rut) ON DELETE RESTRICT
);
