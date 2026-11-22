# Sistema Integral de Gestión - Software FJ

Proyecto académico en Python para gestionar clientes, servicios y reservas mediante programación orientada a objetos, sin utilizar bases de datos.

## Requisitos
- Python 3.9 o superior.
- No requiere instalar librerías externas.

## Ejecución
Desde la carpeta principal:
```bash
python main.py
```
Al ejecutarlo se muestran las operaciones de prueba y se crea `software_fj.log` con el registro de eventos y errores.

## Estructura
```text
software_fj/
├── __init__.py
├── entities.py
├── exceptions.py
├── reservation.py
├── services.py
└── system.py
main.py
README.md
```

## Funcionalidades
- Registro y validación de clientes.
- Servicios de reserva de salas, alquiler de equipos y asesorías especializadas.
- Creación, confirmación, cancelación y finalización de reservas.
- Cálculo de costos con descuentos, impuestos, cantidades y modalidades.
- Validaciones y excepciones personalizadas.
- Registro de eventos y errores mediante `logging`.
- Datos administrados en memoria; no se utiliza base de datos.

## Conceptos de programación orientada a objetos
- **Abstracción:** clases abstractas `Entidad` y `Servicio`.
- **Herencia:** `Cliente` y servicios especializados heredan de sus clases base.
- **Encapsulación:** atributos protegidos y propiedades con validación.
- **Polimorfismo:** cada servicio implementa su cálculo de costo y descripción.

## Pruebas incluidas
`main.py` ejecuta más de diez operaciones: registros válidos e inválidos, creación de servicios, reservas exitosas y fallidas, confirmación, cancelación y validaciones de disponibilidad.

## Persistencia
Clientes, servicios y reservas se conservan en memoria durante la ejecución. Al cerrar el programa, esos datos se reinician. El archivo de logs permanece en el directorio de ejecución.
