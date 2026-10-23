from dominio.ecotech_error import EcoTechError


class EmpleadoNoEncontradoError(EcoTechError):
    """Disponible para operaciones que requieran un empleado existente; obtener devuelve None."""
    pass
