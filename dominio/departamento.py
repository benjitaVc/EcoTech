class Departamento:
    """Representa un área de trabajo dentro de EcoTech."""

    def __init__(self, nombre: str):
        self.nombre = nombre
        self.empleados = []

    def agregar_empleado(self, empleado):
        """Agrega un empleado y lo vincula con el departamento."""
        if empleado not in self.empleados:
            self.empleados.append(empleado)
            empleado.departamento = self

    def __str__(self) -> str:
        return f"Departamento: {self.nombre} ({len(self.empleados)} empleados)"