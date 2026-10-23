from dominio.registro_tiempo import RegistroTiempo
from infraestructura.conexion import transaccion


class RegistroTiempoRepositorio:
    """CRUD de la segunda entidad, con un único mapper."""

    @staticmethod
    def _fila_a_registro(fila):
        return RegistroTiempo(fila[2], fila[3], empleado_rut=fila[1], id=fila[0])

    def guardar(self, registro):
        if registro.id is not None:
            raise ValueError("Un registro nuevo no debe tener id.")
        if not isinstance(registro.empleado_rut, str) or not registro.empleado_rut.strip():
            raise ValueError("El registro debe indicar el RUT del empleado.")
        with transaccion() as conn:
            cur = conn.execute(
                "INSERT INTO registro_tiempo (empleado_rut, fecha, horas) VALUES (?, ?, ?)",
                (registro.empleado_rut, registro.fecha.isoformat(), registro.horas),
            )
            nuevo_id = cur.lastrowid
        registro.id = nuevo_id
        return registro

    def obtener(self, id):
        with transaccion() as conn:
            fila = conn.execute(
                "SELECT id, empleado_rut, fecha, horas FROM registro_tiempo WHERE id = ?",
                (id,),
            ).fetchone()
        return self._fila_a_registro(fila) if fila else None

    def listar(self, empleado_rut=None):
        sql = "SELECT id, empleado_rut, fecha, horas FROM registro_tiempo"
        params = []
        if empleado_rut is not None:
            sql = """SELECT id, empleado_rut, fecha, horas FROM registro_tiempo
                     WHERE empleado_rut = ?"""
            params.append(empleado_rut)
        with transaccion() as conn:
            filas = conn.execute(sql, params).fetchall()
        return [self._fila_a_registro(f) for f in filas]

    def actualizar(self, registro):
        """Modifica fecha y horas sin trasladar el historial a otro empleado."""
        with transaccion() as conn:
            cur = conn.execute(
                "UPDATE registro_tiempo SET fecha = ?, horas = ? WHERE id = ?",
                (registro.fecha.isoformat(), registro.horas, registro.id),
            )
            return cur.rowcount

    def eliminar(self, id):
        with transaccion() as conn:
            cur = conn.execute("DELETE FROM registro_tiempo WHERE id = ?", (id,))
            return cur.rowcount > 0
