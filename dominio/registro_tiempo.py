class RegistroTiempo:
    """Representa las horas trabajadas en un día."""

    def __init__(self, fecha: str, horas: float):
        self.fecha = fecha
        self._horas = None
        self.set_horas(horas)  # Filtro de seguridad

    def set_horas(self, horas: float):
        """Filtro de seguridad: No se pueden registrar 0 o menos horas."""
        if horas <= 0:
            raise ValueError("¡Error! Las horas registradas deben ser mayores a cero.")
        self._horas = horas

    @property
    def horas(self) -> float:
        """Permite leer self.horas fácilmente."""
        return self._horas

    def __str__(self) -> str:
        return f"Registro ({self.fecha}): {self._horas} hrs"