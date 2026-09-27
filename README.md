# Restaurante App - Semana 15 (Manejo de Eventos y Recursos Visuales).

Este repositorio contiene la evolución del proyecto **`restaurante_app`** correspondiente a la **Semana 15** de la asignatura **Programación Orientada a Objetos**. En esta entrega se consolida la arquitectura POO agregando la gestión de recursos multimedia desde la carpeta `assets/`, la captura de eventos mediante callbacks en botones (`command=`) y la persistencia completa del módulo de ventas en archivos JSON.

## Información Académica
- **Estudiante:** Mayerli Melania Granda Quispe
- **Asignatura:** Programación Orientada a Objetos
- **Semestre:** Segundo Semestre
- **Paralelo:** "F"
- **MSC:** Kevin Bolívar Lascano Sánchez
- **Semana:** Semana 15
## Estructura del Proyecto

```text
restaurante_app/
│── assets/
│   └── logo.png
│── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
│── modelos/
│   ├── __init__.py
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
│── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py
│── ui/
│   ├── __init__.py
│   ├── login_view.py
│   └── main_view.py
│── main.py
└── README.md
```
## Novedades y Mejoras de Implementadas

1. Integración de Recursos Virtuales (assets/):
- Incorporación de Logotipo: Carga e integración dinámica de logo.png desde la carpeta assets/ descompuesta mediante os.path y mostrada en la interfaz principal con tkinter.PhotoImage.

2. Programación Orientada a Eventos (Callbacks):
- Enlace directo de la acción del usuario en la interfaz visual a través de botones configurados con el parámetro command=.
- Implementación de callbacks en el formulario de ventas (callback_registrar_venta) para validar campos, procesar la transacción y refrescar componentes visuales.

- **Formulario de Productos**: Agrupa visualmente las entradas de texto para ID, Nombre, Precio, Categoría y Stock.
- **Panel de accciones**: Agrupa los botones de comandos para interactuar con la lógica del negocio.
- **Área de Visualización**: Enmarca la tabla (Treeview) para mostrar la lista actualizada de registros.

3. Módulo Completo de Ventas y Persistencia:
- Modelo Venta (venta.py): Encapsulamiento de los atributos de la venta (ID, producto, cantidad, precios, fecha).
- Lógica Centralizada (restaurante_servicio.py): Control de stock, cálculo de montos y almacenamiento en ventas.json.
- Visualización Dinámica (main_view.py): Despliegue de registros en una tabla ttk.Treeview y selección mediante ttk.Combobox.