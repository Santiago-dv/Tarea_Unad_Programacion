from abc import ABC, abstractmethod
from .entities import Entidad
from .exceptions import ValidacionError, ServicioNoDisponibleError


class Servicio(Entidad, ABC):
    def __init__(self, identificador, nombre, tarifa_base, disponible=True):
        super().__init__(identificador)
        nombre = str(nombre).strip()
        if not nombre:
            raise ValidacionError("El nombre del servicio es obligatorio.")
        if not isinstance(tarifa_base, (int, float)) or tarifa_base <= 0:
            raise ValidacionError("La tarifa base debe ser un número positivo.")
        self.nombre = nombre
        self.tarifa_base = float(tarifa_base)
        self.disponible = bool(disponible)

    def validar_disponibilidad(self):
        if not self.disponible:
            raise ServicioNoDisponibleError(f"El servicio '{self.nombre}' no está disponible.")

    @abstractmethod
    def calcular_costo(self, duracion, *args, **kwargs):
        pass

    @abstractmethod
    def describir(self):
        pass

    def validar_parametros(self, duracion):
        if not isinstance(duracion, (int, float)) or duracion <= 0:
            raise ValidacionError("La duración debe ser un número positivo.")

    def resumen(self):
        return self.describir()


class ReservaSala(Servicio):
    def __init__(self, identificador, nombre, tarifa_base, capacidad, disponible=True):
        super().__init__(identificador, nombre, tarifa_base, disponible)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise ValidacionError("La capacidad debe ser un entero positivo.")
        self.capacidad = capacidad

    def calcular_costo(self, duracion, *args, **kwargs):
        self.validar_parametros(duracion)
        descuento = kwargs.get("descuento", args[0] if args else 0)
        impuesto = kwargs.get("impuesto", 0.19)
        if not 0 <= descuento < 1 or not 0 <= impuesto <= 1:
            raise ValidacionError("Descuento e impuesto deben estar entre 0 y 1.")
        return round(self.tarifa_base * duracion * (1 - descuento) * (1 + impuesto), 2)

    def describir(self):
        return f"Sala: {self.nombre}; capacidad: {self.capacidad}; tarifa/hora: ${self.tarifa_base:.2f}"


class AlquilerEquipo(Servicio):
    def __init__(self, identificador, nombre, tarifa_base, unidades, disponible=True):
        super().__init__(identificador, nombre, tarifa_base, disponible)
        if not isinstance(unidades, int) or unidades <= 0:
            raise ValidacionError("Las unidades deben ser un entero positivo.")
        self.unidades = unidades

    def calcular_costo(self, duracion, *args, **kwargs):
        self.validar_parametros(duracion)
        cantidad = kwargs.get("cantidad", args[0] if args else 1)
        descuento = kwargs.get("descuento", 0)
        if not isinstance(cantidad, int) or cantidad < 1 or cantidad > self.unidades:
            raise ValidacionError("La cantidad supera las unidades disponibles.")
        if not 0 <= descuento < 1:
            raise ValidacionError("El descuento debe estar entre 0 y 1.")
        return round(self.tarifa_base * duracion * cantidad * (1 - descuento), 2)

    def describir(self):
        return f"Equipo: {self.nombre}; unidades: {self.unidades}; tarifa/día: ${self.tarifa_base:.2f}"


class AsesoriaEspecializada(Servicio):
    def __init__(self, identificador, nombre, tarifa_base, especialidad, disponible=True):
        super().__init__(identificador, nombre, tarifa_base, disponible)
        especialidad = str(especialidad).strip()
        if not especialidad:
            raise ValidacionError("La especialidad es obligatoria.")
        self.especialidad = especialidad

    def calcular_costo(self, duracion, *args, **kwargs):
        self.validar_parametros(duracion)
        modalidad = kwargs.get("modalidad", args[0] if args else "virtual")
        if modalidad not in ("virtual", "presencial"):
            raise ValidacionError("La modalidad debe ser virtual o presencial.")
        recargo = 0.15 if modalidad == "presencial" else 0
        return round(self.tarifa_base * duracion * (1 + recargo), 2)

    def describir(self):
        return f"Asesoría: {self.nombre}; especialidad: {self.especialidad}; tarifa/hora: ${self.tarifa_base:.2f}"
