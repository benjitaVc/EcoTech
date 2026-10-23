from dominio.informe import Informe


class InformeNomina(Informe):
    """Informe concreto para ver cuánto hay que pagarle a un empleado."""

    def __init__(self, titulo: str, empleado):
        super().__init__(titulo)
        self.empleado = empleado

    def exportar(self) -> str:
        pago = self.empleado.get_sueldo_base()
        return f"[NÓMINA] {self.titulo} -> Empleado: {self.empleado.nombre}, Pago: ${pago:,.0f}"
