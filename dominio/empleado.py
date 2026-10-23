from datetime import date
from math import isfinite
from dominio.persona import Persona
from dominio.excepciones import SueldoInvalidoError


class Empleado(Persona):
    """Un Empleado es una Persona (aplica herencia)."""

    def __init__(self, rut: str, nombre: str, fecha_ingreso, sueldo_base: float):
        super().__init__(rut, nombre)
        self.fecha_ingreso = fecha_ingreso
        self.set_sueldo_base(sueldo_base)
        self.registros = []
        self.departamento = None

    @property
    def fecha_ingreso(self):
        return self._fecha_ingreso

    @fecha_ingreso.setter
    def fecha_ingreso(self, valor):
        if isinstance(valor, str):
            valor = date.fromisoformat(valor)
        if type(valor) is not date:
            raise ValueError("La fecha de ingreso debe ser una fecha válida.")
        self._fecha_ingreso = valor

    def set_sueldo_base(self, sueldo_base: float):
        if (type(sueldo_base) not in (int, float)
                or not isfinite(sueldo_base) or sueldo_base < 0):
            raise SueldoInvalidoError("El sueldo debe ser un número finito no negativo.")
        self._sueldo_base = sueldo_base

    def get_sueldo_base(self) -> float:
        return self._sueldo_base

    def calcular_total_horas(self):
        """Suma las horas de los registros cargados en este empleado."""
        total = 0
        for registro in self.registros:
            total += registro.horas
        return total

    def __repr__(self):
        return (f"Empleado(rut='{self.rut}', nombre='{self.nombre}', "
                f"fecha_ingreso={self.fecha_ingreso}, sueldo_base={self._sueldo_base})")
