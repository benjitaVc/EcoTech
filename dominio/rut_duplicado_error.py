from dominio.ecotech_error import EcoTechError


class RutDuplicadoError(EcoTechError):
    """Se lanza cuando se intenta registrar un empleado con un RUT que ya existe en la BD."""
    pass
