class Persona:
    """Clase base para representar a una persona."""

    def __init__(self, rut: str, nombre: str):
        self.rut = rut
        self.nombre = nombre

    @property
    def rut(self):
        return self._rut

    @rut.setter
    def rut(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El RUT debe ser un texto no vacío.")
        self._rut = valor

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El nombre debe ser un texto no vacío.")
        self._nombre = valor
