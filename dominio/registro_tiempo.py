from datetime import date
from math import isfinite


class RegistroTiempo:
    """Representa las horas trabajadas por un empleado en un día."""

    def __init__(self, fecha, horas: float, empleado_rut=None, id=None):
        self.fecha = fecha
        self.set_horas(horas)
        self.empleado_rut = empleado_rut
        self.id = id

    @property
    def fecha(self):
        return self._fecha

    @fecha.setter
    def fecha(self, valor):
        if isinstance(valor, str):
            valor = date.fromisoformat(valor)
        if type(valor) is not date:
            raise ValueError("El registro debe tener una fecha válida.")
        self._fecha = valor

    def set_horas(self, horas: float):
        if (type(horas) not in (int, float) or not isfinite(horas)
                or horas <= 0 or horas > 24):
            raise ValueError("Las horas deben ser un número finito mayor que 0 y hasta 24.")
        self._horas = horas

    @property
    def horas(self) -> float:
        return self._horas

    def __str__(self) -> str:
        return f"Registro ({self.fecha}): {self._horas} hrs"
