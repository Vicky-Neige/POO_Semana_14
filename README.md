# Restaurante App - Semana 14 (Componentes y Contenedores).

Este repositorio contiene la evolución del proyecto **`restaurante_app`** correspondiente a la **Semana 14** de la asignatura **Programación Orientada a Objetos**. En esta entrega se implementa una interfaz gráfica mejorada mediante el uso de componentes y contenedores de Tkinter (`ttk.LabelFrame`, `ttk.Entry`, `ttk.Treeview`, `ttk.Button`), permitiendo una gestión completa (CRUD) de productos y manteniendo una clara separación de responsabilidades.

## Información Académica
- **Estudiante:** Mayerli Melania Granda Quispe
- **Asignatura:** Programación Orientada a Objetos
- **Semestre:** Segundo Semestre
- **Paralelo:** "F"
- **MSC:** Kevin Bolívar Lascano Sánchez
- **Semana:** Semana 14
## Estructura del Proyecto

```text
restaurante_app/
├── datos/
│   ├── productos.json
│   └── usuarios.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   └── usuario.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py
├── ui/
│   ├── __init__.py
│   ├── login_view.py
│   └── main_view.py
├── main.py
└── README.md
```
## Novedades y Mejoras de Implementadas

1. Uso de Contenedores (ttk.LabelFrame):

- **Formulario de Productos**: Agrupa visualmente las entradas de texto para ID, Nombre, Precio, Categoría y Stock.
- **Panel de accciones**: Agrupa los botones de comandos para interactuar con la lógica del negocio.
- **Área de Visualización**: Enmarca la tabla (Treeview) para mostrar la lista actualizada de registros.

2. Operaciones sobre Productos (CRUD) mediante command=:
- **Registrar**: Agrupa
- **Cargar / Buscar ID**: Busca un producto por su identificador y carga sus datos en los campos del formulario.
- **Actualizar**: Modifica la información de un producto existente.
- **Eliminar**: Remueve un producto del sistema previa confirmación.
- **Limpiar Formulario**: Vacia las entradas de texto para permitir un nuevo registro.

3. Separación de Responsabilidades y Persistencia:
- Toda la validación lógica y actualización de memoria se delega a RestauranteServicio.
- La persistencia se realiza llamando a ArchivoServicio para actualizar productos.json.
- La vista (MainView) se limita a capturar los eventos del usuario y refrescar los elementos visuales.