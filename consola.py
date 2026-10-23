import sqlite3
from dominio.empleado import Empleado
from dominio.registro_tiempo import RegistroTiempo
from dominio.excepciones import EcoTechError
from infraestructura.empleado_repositorio import EmpleadoRepositorio
from infraestructura.registro_tiempo_repositorio import RegistroTiempoRepositorio
from inicializar_bd import inicializar_bd


def menu():
    inicializar_bd()
    empleados = EmpleadoRepositorio()
    tiempos = RegistroTiempoRepositorio()
    while True:
        print("\nECOTECH")
        print("1 Guardar empleado | 2 Listar empleados | 3 Buscar empleado")
        print("4 Cambiar sueldo | 5 Eliminar empleado")
        print("6 Guardar horas | 7 Listar horas | 8 Buscar registro")
        print("9 Cambiar registro | 10 Eliminar registro | 0 Salir")
        try:
            opcion = input("Opción: ").strip()
            if opcion == "0":
                print("Hasta luego.")
                return
            elif opcion == "1":
                rut = input("RUT: ").strip()
                nombre = input("Nombre: ").strip()
                fecha = input("Ingreso (AAAA-MM-DD): ").strip()
                sueldo = float(input("Sueldo, sin separador de miles: "))
                empleados.guardar(Empleado(rut, nombre, fecha, sueldo))
                print("Empleado guardado.")
            elif opcion == "2":
                for empleado in empleados.listar(input("Nombre contiene (vacío = todos): ")):
                    print(empleado)
            elif opcion == "3":
                empleado = empleados.obtener(input("RUT: ").strip())
                print(empleado if empleado else "Empleado no encontrado.")
            elif opcion == "4":
                empleado = empleados.obtener(input("RUT: ").strip())
                if empleado is None:
                    print("Empleado no encontrado.")
                    continue
                empleado.set_sueldo_base(float(input("Nuevo sueldo: ")))
                print("Filas actualizadas:", empleados.actualizar(empleado))
            elif opcion == "5":
                eliminado = empleados.eliminar(input("RUT: ").strip())
                print("Empleado eliminado." if eliminado else "Empleado no encontrado.")
            elif opcion == "6":
                rut = input("RUT del empleado: ").strip()
                if empleados.obtener(rut) is None:
                    print("Empleado no encontrado.")
                    continue
                fecha = input("Fecha (AAAA-MM-DD): ").strip()
                horas = float(input("Horas: "))
                registro = tiempos.guardar(RegistroTiempo(fecha, horas, rut))
                print("Registro guardado con ID:", registro.id)
            elif opcion == "7":
                rut = input("RUT (vacío = todos): ").strip()
                for registro in tiempos.listar(rut or None):
                    print(registro.id, registro.empleado_rut, registro)
            elif opcion == "8":
                registro = tiempos.obtener(int(input("ID: ")))
                print(registro if registro else "Registro no encontrado.")
            elif opcion == "9":
                registro = tiempos.obtener(int(input("ID: ")))
                if registro is None:
                    print("Registro no encontrado.")
                    continue
                registro.fecha = input("Nueva fecha (AAAA-MM-DD): ").strip()
                registro.set_horas(float(input("Nuevas horas: ")))
                print("Filas actualizadas:", tiempos.actualizar(registro))
            elif opcion == "10":
                eliminado = tiempos.eliminar(int(input("ID: ")))
                print("Registro eliminado." if eliminado else "Registro no encontrado.")
            else:
                print("Elija una opción entre 0 y 10.")
        except EcoTechError as error:
            print("No se realizó la operación:", error)
        except ValueError:
            print("Dato inválido. Revise números y fechas (AAAA-MM-DD).")
        except sqlite3.IntegrityError:
            print("No se realizó la operación: revise duplicados y relaciones.")
        except sqlite3.Error:
            print("Error al operar con SQLite. Revise la base e intente nuevamente.")
        except (EOFError, KeyboardInterrupt):
            print("\nSesión terminada.")
            return
