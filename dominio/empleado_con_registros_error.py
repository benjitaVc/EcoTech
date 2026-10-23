from dominio.ecotech_error import EcoTechError


class EmpleadoConRegistrosError(EcoTechError):
    """No se puede borrar un empleado mientras tenga registros de tiempo."""
    pass
