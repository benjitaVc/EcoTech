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


class InformeNomina(Informe):
    """Informe concreto para ver cuánto hay que pagarle a un empleado."""

    def __init__(self, titulo: str, empleado):
        super().__init__(titulo)
        self.empleado = empleado

    def exportar(self) -> str:
        pago = self.empleado.get_sueldo_base()
        return f"[NÓMINA] {self.titulo} -> Empleado: {self.empleado.nombre}, Pago: ${pago:,.0f}"


class InformeProyecto(Informe):
    """Informe concreto para ver las horas trabajadas en un proyecto."""

    def __init__(self, titulo: str, proyecto: str, horas: float):
        super().__init__(titulo)
        self.proyecto = proyecto
        self.horas = horas

    def exportar(self) -> str:
        return f"[PROYECTO] {self.titulo} -> Proyecto: {self.proyecto}, Horas acumuladas: {self.horas} hrs"