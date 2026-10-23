import sqlite3
from datetime import date
from dominio.empleado import Empleado
from dominio.excepciones import RutDuplicadoError, EmpleadoConRegistrosError
from infraestructura.conexion import transaccion


class EmpleadoRepositorio:
    # Clase que se encarga de guardar, buscar y borrar empleados en la base de datos.

    @staticmethod
    def _fila_a_empleado(fila):
        return Empleado(fila[0], fila[1], date.fromisoformat(fila[2]), fila[3])

    def guardar(self, empleado: Empleado) -> Empleado:
        try:
            with transaccion() as conn:
                conn.execute(
                    "INSERT INTO persona (rut, nombre) VALUES (?, ?)",
                    (empleado.rut, empleado.nombre),
                )
                conn.execute(
                    """INSERT INTO empleado (rut, fecha_ingreso, sueldo_base)
                       VALUES (?, ?, ?)""",
                    (empleado.rut, empleado.fecha_ingreso.isoformat(),
                     empleado.get_sueldo_base()),
                )
        except sqlite3.IntegrityError as error:
            if error.sqlite_errorcode in (sqlite3.SQLITE_CONSTRAINT_PRIMARYKEY,
                                          sqlite3.SQLITE_CONSTRAINT_UNIQUE):
                raise RutDuplicadoError(f"El RUT {empleado.rut} ya existe.") from error
            raise
        return empleado

    def obtener(self, rut: str):
        with transaccion() as conn:
            fila = conn.execute(
                """SELECT p.rut, p.nombre, e.fecha_ingreso, e.sueldo_base
                   FROM empleado e JOIN persona p ON p.rut = e.rut
                   WHERE e.rut = ?""", (rut,),
            ).fetchone()
        return self._fila_a_empleado(fila) if fila else None

    def listar(self, nombre_contiene=None):
        sql = """SELECT p.rut, p.nombre, e.fecha_ingreso, e.sueldo_base
                 FROM empleado e JOIN persona p ON p.rut = e.rut"""
        params = []
        if nombre_contiene:
            sql = """SELECT p.rut, p.nombre, e.fecha_ingreso, e.sueldo_base
                     FROM empleado e JOIN persona p ON p.rut = e.rut
                     WHERE p.nombre LIKE ?"""
            params.append(f"%{nombre_contiene}%")
        with transaccion() as conn:
            filas = conn.execute(sql, params).fetchall()
        return [self._fila_a_empleado(f) for f in filas]

    def actualizar(self, empleado: Empleado) -> int:
        # Le cambia el sueldo al empleado. Si no pilla el RUT en la base, devuelve un 0.
        with transaccion() as conn:
            cur = conn.execute(
                "UPDATE empleado SET sueldo_base = ? WHERE rut = ?",
                (empleado.get_sueldo_base(), empleado.rut),
            )
            return cur.rowcount

    def eliminar(self, rut: str) -> bool:
        # Borra al empleado de las dos tablas a la vez. No deja borrar si el empleado ya tiene horas anotadas.
        try:
            with transaccion() as conn:
                cur = conn.execute("DELETE FROM empleado WHERE rut = ?", (rut,))
                if cur.rowcount == 0:
                    return False
                conn.execute("DELETE FROM persona WHERE rut = ?", (rut,))
        except sqlite3.IntegrityError as error:
            # Atrapamos el error por si choca con la llave foránea (cuando ya tiene registros de tiempo)
            if str(error) == "FOREIGN KEY constraint failed":
                raise EmpleadoConRegistrosError(
                    "No se puede borrar un empleado con registros de tiempo."
                ) from error
            raise
        return True
