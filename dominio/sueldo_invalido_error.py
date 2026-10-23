from dominio.ecotech_error import EcoTechError


class SueldoInvalidoError(EcoTechError, ValueError):
    """Se lanza cuando el sueldo base no cumple las reglas de negocio (ej. es menor a 0)."""
    pass
