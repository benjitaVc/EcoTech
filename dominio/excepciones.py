class EcoTechError(Exception):
    """Excepción base para todos los errores del sistema EcoTech."""
    pass

class RutDuplicadoError(EcoTechError):
    """Se lanza cuando se intenta registrar un empleado con un RUT que ya existe en la BD."""
    pass

class SueldoInvalidoError(EcoTechError, ValueError):
    """Se lanza cuando el sueldo base no cumple las reglas de negocio (ej. es menor a 0)."""
    pass

class EmpleadoNoEncontradoError(EcoTechError):
    """Se lanza cuando se busca, actualiza o elimina un empleado que no existe."""
    pass