"""Prueba manual de commit y rollback en una base temporal, sin tocar datos reales."""
import sqlite3
from pathlib import Path
from tempfile import TemporaryDirectory
from dominio.empleado import Empleado
from infraestructura import conexion
from infraestructura.empleado_repositorio import EmpleadoRepositorio
from inicializar_bd import inicializar_bd


def mostrar_evidencia():
    anterior = conexion.DB_PATH
    try:
        with TemporaryDirectory(prefix="ecotech_evidencia_") as carpeta:
            conexion.DB_PATH = str(Path(carpeta) / "evidencia.db")
            inicializar_bd()
            repo = EmpleadoRepositorio()
            repo.guardar(Empleado("correcto", "Caso correcto", "2026-10-22", 100))
            with conexion.transaccion() as conn:
                print("COMMIT: persona =", conn.execute(
                    "SELECT count(*) FROM persona WHERE rut = ?", ("correcto",)
                ).fetchone()[0])
                print("COMMIT: empleado =", conn.execute(
                    "SELECT count(*) FROM empleado WHERE rut = ?", ("correcto",)
                ).fetchone()[0])

            empleado = Empleado("fallo", "Fallo controlado", "2026-10-22", 100)
            # Solo en esta prueba: evita el setter para provocar el CHECK del segundo INSERT.
            empleado._sueldo_base = -1
            try:
                repo.guardar(empleado)
            except sqlite3.IntegrityError as error:
                print("SEGUNDO INSERT rechazado:", error)
            else:
                raise AssertionError("La base aceptó el sueldo inválido.")
            with conexion.transaccion() as conn:
                personas = conn.execute(
                    "SELECT count(*) FROM persona WHERE rut = ?", ("fallo",)
                ).fetchone()[0]
                empleados = conn.execute(
                    "SELECT count(*) FROM empleado WHERE rut = ?", ("fallo",)
                ).fetchone()[0]
                print("ROLLBACK: persona =", personas)
                print("ROLLBACK: empleado =", empleados)
                print("Integridad referencial:", conn.execute("PRAGMA foreign_key_check").fetchall())
            if personas != 0 or empleados != 0:
                raise AssertionError("Quedaron datos parciales.")
            print("RESULTADO: no quedan datos parciales; el registro correcto se conserva:",
                  repo.obtener("correcto") is not None)
    finally:
        conexion.DB_PATH = anterior


if __name__ == "__main__":
    mostrar_evidencia()
