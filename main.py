from datetime import date
from dominio.empleado import Empleado
from infraestructura.empleado_repositorio import EmpleadoRepositorio

def probar_crud_y_seguridad():
    repo = EmpleadoRepositorio()

    print("=== 1. PRUEBA DE INSERT (Guardar) ===")
    ana = Empleado("12345678-9", "Ana Rojas", date(2024, 3, 1), 950_000)
    repo.guardar(ana)
    print("Empleado guardado exitosamente.")

    print("\n=== 2. PRUEBA DE SELECT (Obtener uno y Listar) ===")
    empleado_obtenido = repo.obtener("12345678-9")
    print(f"Obtenido: {empleado_obtenido}")
    print(f"Total empleados en BD: {len(repo.listar())}")

    print("\n=== 3. PRUEBA DE UPDATE (Actualizar) ===")
    ana.set_sueldo_base(1_050_000)
    filas_modificadas = repo.actualizar(ana)
    print(f"Filas actualizadas: {filas_modificadas}")
    print(f"Nuevo sueldo en BD: {repo.obtener('12345678-9').get_sueldo_base()}")

    print("\n=== 4. PRUEBA DE SEGURIDAD (Inyección SQL) ===")
    payload_ataque = "' OR '1'='1"
    resultado_ataque = repo.listar(nombre_contiene=payload_ataque)
    print(f"Resultado de búsqueda con payload '{payload_ataque}': {resultado_ataque}")
    
    if len(resultado_ataque) == 0:
        print("✔ PRUEBA SUPERADA: La consulta está correctamente parametrizada y es segura.")
    else:
        print("✘ ALERTA DE SEGURIDAD: La consulta no está totalmente parametrizada.")

    print("\n=== 5. PRUEBA DE DELETE (Eliminar) ===")
    eliminado = repo.eliminar("12345678-9")
    print(f"Empleado eliminado: {eliminado}")
    print(f"Total empleados tras eliminar: {len(repo.listar())}")

if __name__ == "__main__":
    probar_crud_y_seguridad()