class ErrorSistema(Exception):
    """Error base del sistema."""


class ValidacionError(ErrorSistema):
    """Datos de entrada inválidos."""


class ServicioNoDisponibleError(ErrorSistema):
    """El servicio no está disponible."""


class ReservaError(ErrorSistema):
    """Operación de reserva no permitida."""


class EntidadDuplicadaError(ErrorSistema):
    """La entidad ya está registrada."""
