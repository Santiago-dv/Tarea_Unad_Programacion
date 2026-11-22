from software_fj import SistemaFJ
from software_fj.entities import Cliente
from software_fj.services import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from software_fj.exceptions import ErrorSistema


def ejecutar_pruebas():
    sistema = SistemaFJ()
    print("\n=== SOFTWARE FJ | DEMOSTRACIÓN ===")
    sistema.registrar_cliente(Cliente("C001", "Laura Pérez", "laura@email.com", "3001234567"))
    sistema.registrar_cliente(Cliente("C002", "Carlos Díaz", "carlos@email.com", "3017654321"))
    print("1-2. Clientes registrados.")
    try:
        Cliente("C003", "Ana Ruiz", "correo_invalido", "3021234567")
    except ErrorSistema as error:
        print(f"3. Cliente inválido controlado: {error}")

    sala = sistema.registrar_servicio(ReservaSala("S001", "Sala Ejecutiva", 50000, 12))
    sistema.registrar_servicio(AlquilerEquipo("S002", "Proyector", 30000, 5))
    asesoria = sistema.registrar_servicio(AsesoriaEspecializada("S003", "Consultoría TI", 80000, "Sistemas"))
    print("4. Tres servicios registrados.")
    try:
        ReservaSala("S004", "Sala inválida", -1000, 10)
    except ErrorSistema as error:
        print(f"5. Servicio inválido controlado: {error}")

    r1 = sistema.crear_reserva("R001", "C001", "S001", 2, descuento=0.10, impuesto=0.19)
    r2 = sistema.crear_reserva("R002", "C002", "S002", 1, cantidad=2)
    r3 = sistema.crear_reserva("R003", "C001", "S003", 2, modalidad="presencial")
    print("6-8. Reservas creadas:", r1.resumen(), r2.resumen(), r3.resumen(), sep="\n")
    for numero, cliente, servicio, duracion in [
        (9, "C999", "S001", 1), (10, "C001", "S001", 0)
    ]:
        try:
            sistema.crear_reserva(f"R{numero:03}", cliente, servicio, duracion)
        except ErrorSistema as error:
            print(f"{numero}. Error controlado: {error}")

    sistema.procesar_reserva("R001", "confirmar")
    sistema.procesar_reserva("R001", "completar")
    sistema.procesar_reserva("R002", "cancelar")
    print("11-12. Reserva completada y reserva cancelada.")
    sistema.registrar_servicio(ReservaSala("S005", "Sala en mantenimiento", 40000, 8, disponible=False))
    try:
        sistema.crear_reserva("R006", "C001", "S005", 1)
    except ErrorSistema as error:
        print(f"13. Servicio no disponible: {error}")
    try:
        asesoria.calcular_costo(1, modalidad="mixta")
    except ErrorSistema as error:
        print(f"14. Parámetro inválido: {error}")

    print("15. Consulta con try/except/else/finally.")
    try:
        cliente = sistema.buscar_cliente("C001")
    except ErrorSistema as error:
        sistema.logger.exception("Falló la consulta")
        print(error)
    else:
        print(cliente.resumen())
    finally:
        sistema.logger.info("Finalizó la consulta")
    print("\n--- RESUMEN ---")
    for reserva in sistema.listar_reservas():
        print(reserva)


if __name__ == "__main__":
    try:
        ejecutar_pruebas()
    except Exception as error:
        print(f"Error inesperado: {error}")
