class Persona:
    """Representa a una persona en el sistema."""

    def __init__(self, rut: str, nombre: str):
        self._rut = None   # Guardaremos el RUT aquí de forma protegida
        self.set_rut(rut)  # Usamos nuestro "filtro de seguridad" desde el inicio
        self.nombre = nombre

    def set_rut(self, rut: str):
        """Filtro de seguridad: Verifica que el RUT sea un texto válido con guion."""
        if not isinstance(rut, str) or not rut.strip() or "-" not in rut:
            raise ValueError("¡Error! El RUT debe ser un texto válido y llevar guion (Ejemplo: 12345678-9).")
        self._rut = rut

    def get_rut(self) -> str:
        """Entrega el RUT guardado."""
        return self._rut

    def __str__(self) -> str:
        """Define cómo se imprime una Persona cuando hacemos print()."""
        return f"Persona: {self.nombre} | RUT: {self._rut}"