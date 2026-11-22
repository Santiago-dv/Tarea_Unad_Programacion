from abc import ABC, abstractmethod
from datetime import datetime
from .exceptions import ValidacionError


class Entidad(ABC):
    def __init__(self, identificador):
        identificador = str(identificador).strip()
        if not identificador:
            raise ValidacionError("El identificador no puede estar vacío.")
        self._identificador = identificador
        self._creado_en = datetime.now()

    @property
    def identificador(self):
        return self._identificador

    @property
    def creado_en(self):
        return self._creado_en

    @abstractmethod
    def resumen(self):
        pass


class Cliente(Entidad):
    def __init__(self, identificador, nombre, correo, telefono):
        super().__init__(identificador)
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        valor = str(valor).strip()
        if len(valor) < 2:
            raise ValidacionError("El nombre debe tener al menos 2 caracteres.")
        self._nombre = valor

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor):
        valor = str(valor).strip().lower()
        if "@" not in valor or "." not in valor.split("@")[-1]:
            raise ValidacionError("El correo electrónico no es válido.")
        self._correo = valor

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        valor = str(valor).strip()
        if len(valor) < 7 or not valor.replace("+", "").replace("-", "").replace(" ", "").isdigit():
            raise ValidacionError("El teléfono debe contener al menos 7 dígitos.")
        self._telefono = valor

    def resumen(self):
        return f"{self.identificador} - {self.nombre} ({self.correo})"
