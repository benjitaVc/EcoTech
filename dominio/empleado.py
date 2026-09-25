from dominio.persona import Persona

class Empleado(Persona):
    """Un Empleado ES UNA Persona (aplica herencia)."""

    def __init__(self, rut: str, nombre: str, fecha_ingreso: str, sueldo_base: float):
        # 1. Llamamos a la clase base (Persona) para que guarde el RUT y nombre con seguridad
        super().__init__(rut, nombre)
        
        self.fecha_ingreso = fecha_ingreso
        self._sueldo_base = None
        
        # 2. Usamos nuestro filtro de seguridad para el sueldo
        self.set_sueldo_base(sueldo_base)
        
        self.registros = []
        self.departamento = None

    def set_sueldo_base(self, sueldo_base: float):
        """Filtro de seguridad: El sueldo no puede ser negativo."""
        if sueldo_base < 0:
            raise ValueError("¡Error! El sueldo base no puede ser negativo.")
        self._sueldo_base = sueldo_base

    def get_sueldo_base(self) -> float:
        """Devuelve el sueldo base guardado."""
        return self._sueldo_base

    def registrar_hora(self, registro):
        """Agrega un registro de tiempo a la lista."""
        self.registros.append(registro)

    def total_horas(self) -> float:
        """Suma las horas de todos los registros del empleado."""
        return sum(r.horas for r in self.registros)

    def __str__(self) -> str:
        """Texto bonito que describe al empleado al usar print()."""
        return f"Empleado: {self.nombre} | Sueldo: ${self._sueldo_base:,.0f} | Horas Totales: {self.total_horas()}h"