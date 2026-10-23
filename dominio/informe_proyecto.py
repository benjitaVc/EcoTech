from dominio.informe import Informe


class InformeProyecto(Informe):
    """Informe concreto para ver las horas trabajadas en un proyecto."""

    def __init__(self, titulo: str, proyecto: str, horas: float):
        super().__init__(titulo)
        self.proyecto = proyecto
        self.horas = horas

    def exportar(self) -> str:
        return f"[PROYECTO] {self.titulo} -> Proyecto: {self.proyecto}, Horas acumuladas: {self.horas} hrs"
