from abc import ABC, abstractmethod


class Informe(ABC):
    """Clase abstracta que define la estructura básica de un informe."""

    def __init__(self, titulo: str):
        self.titulo = titulo

    @abstractmethod
    def exportar(self) -> str:
        """Método abstracto: obliga a las subclases a implementar su propia versión."""
        pass

    def __str__(self) -> str:
        return f"Informe: {self.titulo}"
