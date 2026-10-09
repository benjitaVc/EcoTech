from datetime import date
from dominio.empleado import Empleado
from infraestructura.conexion import obtener_conexion

class EmpleadoRepositorio:
    """Repositorio parametrizado para la entidad Empleado."""

    @staticmethod
    def _fila_a_empleado(fila):
        """Mapea una fila cruda devuelta por la BD a un objeto Empleado."""
        fecha_ing = date.fromisoformat(fila[2]) if isinstance(fila[2], str) else fila[2]
        return Empleado(
            rut=fila[0],
            nombre=fila[1],
            fecha_ingreso=fecha_ing,
            sueldo_base=fila[3],
        )

    def guardar(self, empleado: Empleado) -> Empleado:
        """Inserta persona y empleado usando marcadores ?."""
        with obtener_conexion() as conn:
            conn.execute(
                "INSERT INTO persona (rut, nombre) VALUES (?, ?)",
                (empleado.rut, empleado.nombre),
            )
            conn.execute(
                """INSERT INTO empleado (rut, fecha_ingreso, sueldo_base)
                   VALUES (?, ?, ?)""",
                (
                    empleado.rut,
                    empleado.fecha_ingreso.isoformat() if isinstance(empleado.fecha_ingreso, date) else str(empleado.fecha_ingreso),
                    empleado.get_sueldo_base(),
                ),
            )
        return empleado

    def obtener(self, rut: str):
        """Consulta un empleado por RUT. Devuelve Empleado o None si no existe."""
        with obtener_conexion() as conn:
            fila = conn.execute(
                """SELECT p.rut, p.nombre, e.fecha_ingreso, e.sueldo_base
                   FROM empleado e JOIN persona p ON p.rut = e.rut
                   WHERE e.rut = ?""",
                (rut,),
            ).fetchone()
        return self._fila_a_empleado(fila) if fila else None

    def listar(self, nombre_contiene: str = None):
        """Lista empleados con o sin filtro de nombre parametrizado."""
        sql = """SELECT p.rut, p.nombre, e.fecha_ingreso, e.sueldo_base
                 FROM empleado e JOIN persona p ON p.rut = e.rut"""
        params = []
        if nombre_contiene:
            sql += " WHERE p.nombre LIKE ?"
            params.append(f"%{nombre_contiene}%")
        with obtener_conexion() as conn:
            filas = conn.execute(sql, params).fetchall()
        return [self._fila_a_empleado(f) for f in filas]

    def actualizar(self, empleado: Empleado) -> int:
        """Actualiza el sueldo base y devuelve la cantidad de filas modificadas."""
        with obtener_conexion() as conn:
            cur = conn.execute(
                "UPDATE empleado SET sueldo_base = ? WHERE rut = ?",
                (empleado.get_sueldo_base(), empleado.rut),
            )
        return cur.rowcount

    def eliminar(self, rut: str) -> bool:
        """Aplica DELETE real del registro según nuestra decisión de diseño."""
        with obtener_conexion() as conn:
            cur = conn.execute("DELETE FROM empleado WHERE rut = ?", (rut,))
        return cur.rowcount > 0