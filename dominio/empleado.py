from datetime import date
from dominio.persona import Persona

class Empleado(Persona):
    """Un Empleado ES UNA Persona (aplica herencia)."""

    def __init__(self, rut: str, nombre: str, fecha_ingreso, sueldo_base: float):
        # 1. Llamamos a la clase base Persona para registrar rut y nombre
        super().__init__(rut, nombre)

        # 2. Asignamos la fecha de ingreso
        if isinstance(fecha_ingreso, str):
            self.fecha_ingreso = date.fromisoformat(fecha_ingreso)
        else:
            self.fecha_ingreso = fecha_ingreso

        # 3. Asignamos el sueldo base con el setter
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

    def __repr__(self):
        return f"Empleado(rut='{self.rut}', nombre='{self.nombre}', fecha_ingreso={self.fecha_ingreso}, sueldo_base={self._sueldo_base})"