from dominio.empleado import Empleado
from dominio.informe import InformeNomina, InformeProyecto

def main():
    # 1. Crear dos empleados de prueba
    emp1 = Empleado("12345678-9", "Benjamin", "2024-01-15", 850000.0)
    emp2 = Empleado("98765432-1", "Constanza", "2024-02-01", 920000.0)

    # 2. Crear los 3 informes que pide la pauta (2 de Nómina y 1 de Proyecto)
    inf1 = InformeNomina("Nómina de Marzo", emp1)
    inf2 = InformeNomina("Nómina de Marzo", emp2)
    inf3 = InformeProyecto("Monitoreo EcoTech", "Sistema de Control", 45.5)

    # 3. Guardarlos en una lista mixta
    informes = [inf1, inf2, inf3]

    # 4. Recorrer la lista invocando exportar()
    print("=== EXPORTACIÓN DE INFORMES (POLIMORFISMO) ===")
    for informe in informes:
        print(informe.exportar())

if __name__ == "__main__":
    main()