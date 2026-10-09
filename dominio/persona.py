class Persona:
    """Clase base para representar a una persona."""
    def __init__(self, rut: str, nombre: str):
        self.rut = rut
        self.nombre = nombre