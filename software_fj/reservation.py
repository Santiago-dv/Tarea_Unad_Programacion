from datetime import datetime
from .entities import Entidad
from .exceptions import ReservaError, ValidacionError


class Reserva(Entidad):
    ESTADOS = ("pendiente", "confirmada", "cancelada", "completada")

    def __init__(self, identificador, cliente, servicio, duracion, costo):
        super().__init__(identificador)
        if cliente is None or servicio is None:
            raise ValidacionError("La reserva requiere cliente y servicio.")
        if duracion <= 0 or costo < 0:
            raise ValidacionError("La duración y el costo no son válidos.")
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.costo = costo
        self.estado = "pendiente"
        self.fecha = datetime.now()

    def confirmar(self):
        if self.estado != "pendiente":
            raise ReservaError("Solo se pueden confirmar reservas pendientes.")
        self.servicio.validar_disponibilidad()
        self.estado = "confirmada"
        return self.estado

    def cancelar(self):
        if self.estado not in ("pendiente", "confirmada"):
            raise ReservaError("La reserva no se puede cancelar en su estado actual.")
        self.estado = "cancelada"
        return self.estado

    def completar(self):
        if self.estado != "confirmada":
            raise ReservaError("Solo se pueden completar reservas confirmadas.")
        self.estado = "completada"
        return self.estado

    def resumen(self):
        return (f"Reserva {self.identificador}: {self.cliente.nombre} | "
                f"{self.servicio.nombre} | {self.estado} | ${self.costo:.2f}")
