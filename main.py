import sqlite3
import sys
from datetime import date
from pathlib import Path
from tempfile import TemporaryDirectory
from dominio.empleado import Empleado
from dominio.registro_tiempo import RegistroTiempo
from dominio.excepciones import EmpleadoConRegistrosError, EcoTechError, RutDuplicadoError
from dominio.departamento import Departamento
from dominio.informe_nomina import InformeNomina
from dominio.informe_proyecto import InformeProyecto
from infraestructura import conexion
from infraestructura.empleado_repositorio import EmpleadoRepositorio
from infraestructura.registro_tiempo_repositorio import RegistroTiempoRepositorio
from inicializar_bd import inicializar_bd


def comprobar(condicion):
    if not condicion:
        raise AssertionError("Falló una comprobación de la demostración.")


def probar_crud_y_seguridad():
    repo = EmpleadoRepositorio()
    tiempos = RegistroTiempoRepositorio()
    ana = Empleado("12345678-9", "Ana Rojas", date(2024, 3, 1), 950_000)
    repo.guardar(ana)
    print("CREAR:", repo.obtener(ana.rut))
    print("LISTAR:", len(repo.listar()), "empleado(s)")
    ana.set_sueldo_base(1_050_000)
    comprobar(repo.actualizar(ana) == 1)
    comprobar(repo.obtener(ana.rut).get_sueldo_base() == 1_050_000)
    print("ACTUALIZAR: sueldo comprobado")

    registro = RegistroTiempo(date(2024, 3, 2), 8, ana.rut)
    tiempos.guardar(registro)
    comprobar(tiempos.obtener(registro.id).horas == 8)
    comprobar(len(tiempos.listar(ana.rut)) == 1)
    registro.set_horas(7)
    comprobar(tiempos.actualizar(registro) == 1)
    comprobar(tiempos.obtener(registro.id).horas == 7)
    print("REGISTROS: creación, lectura y actualización comprobadas")
    departamento = Departamento("Informática")
    departamento.agregar_empleado(ana)
    ana.registros = tiempos.listar(ana.rut)
    informes = [InformeNomina("Sueldo base", ana),
                InformeProyecto("Horas registradas", "EcoTech", ana.calcular_total_horas())]
    print("POLIMORFISMO:", departamento)
    for informe in informes:
        print(informe.exportar())
    try:
        ana.set_sueldo_base(-100)
    except ValueError:
        print("VALIDACIÓN: sueldo negativo rechazado; la demo continúa")
    try:
        repo.guardar(ana)
    except RutDuplicadoError:
        print("VALIDACIÓN: RUT duplicado rechazado; la demo continúa")

    payload = "' OR '1'='1"
    print("Payload probado:", repr(payload))
    print("Búsqueda por nombre antes de guardarlo:", repo.listar(payload))
    comprobar(repo.listar(payload) == [])
    comprobar(repo.obtener(payload) is None)
    comprobar(repo.eliminar(payload) is False)
    comprobar(repo.actualizar(Empleado(payload, "Intento", date(2024, 3, 1), 1)) == 0)
    comprobar(tiempos.obtener(payload) is None)
    comprobar(tiempos.listar(payload) == [])
    comprobar(tiempos.eliminar(payload) is False)
    intento = RegistroTiempo(date(2024, 3, 2), 1, ana.rut, payload)
    comprobar(tiempos.actualizar(intento) == 0)
    # Guardar el texto literalmente comprueba también las escrituras.
    literal = Empleado(payload, payload, date(2024, 3, 1), 10)
    repo.guardar(literal)
    tiempos.guardar(RegistroTiempo(date(2024, 3, 2), 1, payload))
    comprobar(len(repo.listar(payload)) == 1)
    comprobar(repo.obtener(payload).nombre == payload)
    comprobar(repo.obtener(ana.rut).get_sueldo_base() == 1_050_000)
    print("INYECCIÓN: el texto se trata como dato; no afecta a Ana")

    try:
        repo.eliminar(ana.rut)
    except EmpleadoConRegistrosError:
        print("INTEGRIDAD: borrado con historial bloqueado")
    else:
        raise AssertionError("Se permitió borrar un empleado con historial")
    comprobar(tiempos.eliminar(registro.id))
    comprobar(tiempos.obtener(registro.id) is None)
    comprobar(repo.eliminar(ana.rut))
    comprobar(repo.obtener(ana.rut) is None)
    repo.guardar(ana)
    comprobar(repo.eliminar(ana.rut))
    print("ELIMINAR: ambas entidades y reutilización del RUT comprobadas")


def demostracion():
    ruta_anterior = conexion.DB_PATH
    try:
        with TemporaryDirectory(prefix="ecotech_demo_") as carpeta:
            conexion.DB_PATH = str(Path(carpeta) / "demo.db")
            inicializar_bd()
            probar_crud_y_seguridad()
    finally:
        conexion.DB_PATH = ruta_anterior


def ejecutar(argumentos=None):
    argumentos = sys.argv[1:] if argumentos is None else argumentos
    try:
        if argumentos == ["--menu"]:
            from consola import menu
            menu()
        elif not argumentos:
            demostracion()
        else:
            print("Uso: py main.py [--menu]")
            return 1
    except EcoTechError as error:
        print("No se pudo completar la operación:", error)
        return 1
    except ValueError:
        print("Dato inválido. Revise los valores y las fechas.")
        return 1
    except sqlite3.Error:
        print("Error al operar con SQLite. Revise la configuración y el esquema.")
        return 1
    except OSError:
        print("No se pudo acceder a un archivo. Revise la carpeta y sus permisos.")
        return 1
    except (KeyboardInterrupt, EOFError):
        print("\nSesión terminada.")
    return 0


if __name__ == "__main__":
    sys.exit(ejecutar())
