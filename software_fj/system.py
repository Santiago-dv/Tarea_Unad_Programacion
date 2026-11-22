import logging
from .entities import Cliente
from .services import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from .reservation import Reserva
from .exceptions import (ValidacionError, EntidadDuplicadaError,
                         ServicioNoDisponibleError, ReservaError)


class SistemaFJ:
    def __init__(self, archivo_log="software_fj.log"):
        self.clientes = []
        self.servicios = []
        self.reservas = []
        self.logger = logging.getLogger("SoftwareFJ")
        self.logger.setLevel(logging.INFO)
        self.logger.propagate = False
        if not self.logger.handlers:
            handler = logging.FileHandler(archivo_log, encoding="utf-8")
            handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
            self.logger.addHandler(handler)

    def registrar_cliente(self, cliente):
        if not isinstance(cliente, Cliente):
            raise ValidacionError("El objeto suministrado no es un cliente.")
        if any(c.identificador == cliente.identificador for c in self.clientes):
            raise EntidadDuplicadaError("Ya existe un cliente con ese identificador.")
        self.clientes.append(cliente)
        self.logger.info("Cliente registrado: %s", cliente.identificador)
        return cliente

    def registrar_servicio(self, servicio):
        tipos = (ReservaSala, AlquilerEquipo, AsesoriaEspecializada)
        if not isinstance(servicio, tipos):
            raise ValidacionError("Tipo de servicio no reconocido.")
        if any(s.identificador == servicio.identificador for s in self.servicios):
            raise EntidadDuplicadaError("Ya existe un servicio con ese identificador.")
        self.servicios.append(servicio)
        self.logger.info("Servicio registrado: %s", servicio.identificador)
        return servicio

    def crear_reserva(self, identificador, id_cliente, id_servicio, duracion, *args, **kwargs):
        try:
            cliente = self.buscar_cliente(id_cliente)
            servicio = self.buscar_servicio(id_servicio)
            servicio.validar_disponibilidad()
            costo = servicio.calcular_costo(duracion, *args, **kwargs)
            reserva = Reserva(identificador, cliente, servicio, duracion, costo)
            self.reservas.append(reserva)
            self.logger.info("Reserva creada: %s", identificador)
            return reserva
        except (ValidacionError, ServicioNoDisponibleError) as exc:
            self.logger.exception("No fue posible crear la reserva %s", identificador)
            raise ReservaError(f"Error al crear la reserva: {exc}") from exc

    def buscar_cliente(self, identificador):
        for cliente in self.clientes:
            if cliente.identificador == str(identificador):
                return cliente
        raise ValidacionError(f"No existe el cliente {identificador}.")

    def buscar_servicio(self, identificador):
        for servicio in self.servicios:
            if servicio.identificador == str(identificador):
                return servicio
        raise ValidacionError(f"No existe el servicio {identificador}.")

    def procesar_reserva(self, identificador, accion):
        reserva = next((r for r in self.reservas if r.identificador == str(identificador)), None)
        if reserva is None:
            raise ReservaError(f"No existe la reserva {identificador}.")
        try:
            if accion == "confirmar":
                resultado = reserva.confirmar()
            elif accion == "cancelar":
                resultado = reserva.cancelar()
            elif accion == "completar":
                resultado = reserva.completar()
            else:
                raise ReservaError("Acción no reconocida.")
            self.logger.info("Reserva %s: %s", identificador, resultado)
            return resultado
        except Exception:
            self.logger.exception("Error al procesar la reserva %s", identificador)
            raise

    def listar_reservas(self):
        return [r.resumen() for r in self.reservas]
