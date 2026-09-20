import tkinter as tk
from tkinter import ttk, messagebox

class MainView(tk.Frame):
    def __init__(self, master, servicio, usuario_actual, on_logout):
        super().__init__(master)
        self.master = master
        self.servicio = servicio
        self.usuario_actual = usuario_actual
        self.on_logout = on_logout

        self.master.title("Restaurante App - Menú Principal")
        self.master.geometry("720x580")

        self.crear_widgets()

    def crear_widgets(self):
        lbl_bienvenida = tk.Label(
            self, 
            text=f"Panel Principal - Usuario: {self.usuario_actual.nombre} ({self.usuario_actual.rol})", 
            font=("Arial", 11, "bold")
        )
        lbl_bienvenida.pack(pady=10)

        frame_botones = tk.Frame(self)
        frame_botones.pack(pady=5)

        btn_prod = tk.Button(frame_botones, text="Productos", width=12, command=self.mostrar_productos)
        btn_prod.grid(row=0, column=0, padx=5)

        btn_usrs = tk.Button(frame_botones, text="Usuarios", width=12, command=self.mostrar_usuarios)
        btn_usrs.grid(row=0, column=1, padx=5)

        btn_ventas = tk.Button(frame_botones, text="Ventas", width=12, command=self.mostrar_ventas_pendiente)
        btn_ventas.grid(row=0, column=2, padx=5)

        btn_salir = tk.Button(frame_botones, text="Cerrar Sesión", width=12, bg="#dc3545", fg="white", command=self.cerrar_sesion)
        btn_salir.grid(row=0, column=3, padx=5)

        self.frame_contenido = tk.Frame(self)
        self.frame_contenido.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        self.pack(fill=tk.BOTH, expand=True)
        self.mostrar_productos()

    def limpiar_contenido(self):
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()

    def mostrar_productos(self):
        self.limpiar_contenido()
        frame_form = ttk.LabelFrame(self.frame_contenido, text=" Formulario de Productos ", padding=10)
        frame_form.pack(fill="x", pady=5)

        ttk.Label(frame_form, text="ID / Código:").grid(row=0, column=0, sticky="w", padx=5, pady=3)
        self.ent_id = ttk.Entry(frame_form, width=12)
        self.ent_id.grid(row=0, column=1, sticky="w", padx=5, pady=3)

        ttk.Label(frame_form, text="Nombre:").grid(row=0, column=2, sticky="w", padx=5, pady=3)
        self.ent_nombre = ttk.Entry(frame_form, width=25)
        self.ent_nombre.grid(row=0, column=3, sticky="w", padx=5, pady=3)

        ttk.Label(frame_form, text="Precio ($):").grid(row=1, column=0, sticky="w", padx=5, pady=3)
        self.ent_precio = ttk.Entry(frame_form, width=12)
        self.ent_precio.grid(row=1, column=1, sticky="w", padx=5, pady=3)

        ttk.Label(frame_form, text="Categoría:").grid(row=1, column=2, sticky="w", padx=5, pady=3)
        self.ent_categoria = ttk.Entry(frame_form, width=25)
        self.ent_categoria.grid(row=1, column=3, sticky="w", padx=5, pady=3)

        ttk.Label(frame_form, text="Stock:").grid(row=2, column=0, sticky="w", padx=5, pady=3)
        self.ent_stock = ttk.Entry(frame_form, width=12)
        self.ent_stock.grid(row=2, column=1, sticky="w", padx=5, pady=3)

        frame_acciones = ttk.LabelFrame(self.frame_contenido, text=" Acciones ", padding=10)
        frame_acciones.pack(fill="x", pady=5)

        tk.Button(frame_acciones, text="Registrar", width=10, bg="#28a745", fg="white", command=self.ejecutar_registro).pack(side="left", padx=4)
        tk.Button(frame_acciones, text="Cargar/Buscar ID", width=14, command=self.ejecutar_busqueda).pack(side="left", padx=4)
        tk.Button(frame_acciones, text="Actualizar", width=10, command=self.ejecutar_actualizacion).pack(side="left", padx=4)
        tk.Button(frame_acciones, text="Eliminar", width=10, bg="#ffc107", command=self.ejecutar_eliminacion).pack(side="left", padx=4)
        tk.Button(frame_acciones, text="Limpiar Campos", width=12, command=self.limpiar_formulario).pack(side="right", padx=4)

        frame_tabla = ttk.LabelFrame(self.frame_contenido, text=" Productos Registrados ", padding=10)
        frame_tabla.pack(fill=tk.BOTH, expand=True, pady=5)

        columnas = ("id", "nombre", "precio", "categoria", "stock")
        self.tabla_prod = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=6)

        self.tabla_prod.heading("id", text="ID")
        self.tabla_prod.heading("nombre", text="Nombre")
        self.tabla_prod.heading("precio", text="Precio ($)")
        self.tabla_prod.heading("categoria", text="Categoría")
        self.tabla_prod.heading("stock", text="Stock")

        self.tabla_prod.column("id", width=50, anchor="center")
        self.tabla_prod.column("nombre", width=180)
        self.tabla_prod.column("precio", width=80, anchor="e")
        self.tabla_prod.column("categoria", width=120)
        self.tabla_prod.column("stock", width=60, anchor="center")

        self.tabla_prod.pack(fill=tk.BOTH, expand=True)
        self.actualizar_tabla_productos()

    def actualizar_tabla_productos(self):
        for item in self.tabla_prod.get_children():
            self.tabla_prod.delete(item)

        productos = self.servicio.obtener_productos()
        for p in productos:
            self.tabla_prod.insert("", tk.END, values=(
                p.id_producto, p.nombre, f"{p.precio:.2f}", p.categoria, p.stock
            ))

    def limpiar_formulario(self):
        self.ent_id.delete(0, tk.END)
        self.ent_nombre.delete(0, tk.END)
        self.ent_precio.delete(0, tk.END)
        self.ent_categoria.delete(0, tk.END)
        self.ent_stock.delete(0, tk.END)

    def ejecutar_registro(self):
        exito, msg = self.servicio.agregar_producto(
            self.ent_id.get().strip(),
            self.ent_nombre.get().strip(),
            self.ent_precio.get().strip(),
            self.ent_categoria.get().strip(),
            self.ent_stock.get().strip()
        )
        if exito:
            messagebox.showinfo("Éxito", msg)
            self.actualizar_tabla_productos()
            self.limpiar_formulario()
        else:
            messagebox.showwarning("Atención", msg)

    def ejecutar_busqueda(self):
        id_search = self.ent_id.get().strip()
        if not id_search:
            messagebox.showwarning("Atención", "Ingrese el ID del producto que desea consultar.")
            return

        prod = self.servicio.obtener_producto_por_id(id_search)
        if prod:
            self.limpiar_formulario()
            self.ent_id.insert(0, prod.id_producto)
            self.ent_nombre.insert(0, prod.nombre)
            self.ent_precio.insert(0, str(prod.precio))
            self.ent_categoria.insert(0, prod.categoria)
            self.ent_stock.insert(0, str(prod.stock))
            messagebox.showinfo("Cargado", f"Producto '{prod.nombre}' cargado en el formulario.")
        else:
            messagebox.showerror("No encontrado", f"No existe un producto registrado con el ID '{id_search}'.")

    def ejecutar_actualizacion(self):
        exito, msg = self.servicio.actualizar_producto(
            self.ent_id.get().strip(),
            self.ent_nombre.get().strip(),
            self.ent_precio.get().strip(),
            self.ent_categoria.get().strip(),
            self.ent_stock.get().strip()
        )
        if exito:
            messagebox.showinfo("Éxito", msg)
            self.actualizar_tabla_productos()
            self.limpiar_formulario()
        else:
            messagebox.showwarning("Atención", msg)

    def ejecutar_eliminacion(self):
        id_prod = self.ent_id.get().strip()
        if not id_prod:
            messagebox.showwarning("Atención", "Escriba o busque el ID del producto a eliminar.")
            return

        confirmar = messagebox.askyesno("Confirmación", f"¿Está seguro de eliminar el producto con ID '{id_prod}'?")
        if confirmar:
            exito, msg = self.servicio.eliminar_producto(id_prod)
            if exito:
                messagebox.showinfo("Éxito", msg)
                self.actualizar_tabla_productos()
                self.limpiar_formulario()
            else:
                messagebox.showwarning("Atención", msg)

    def mostrar_usuarios(self):
        self.limpiar_contenido()

        lbl = tk.Label(self.frame_contenido, text="Usuarios del Sistema", font=("Arial", 12, "bold"))
        lbl.pack(pady=5)

        columnas = ("username", "rol")
        tabla = ttk.Treeview(self.frame_contenido, columns=columnas, show="headings", height=8)

        tabla.heading("username", text="Usuario")
        tabla.heading("rol", text="Rol")

        tabla.column("username", width=150)
        tabla.column("rol", width=150)

        usuarios = self.servicio.obtener_usuarios()
        for u in usuarios:
            tabla.insert("", tk.END, values=(u.username, u.rol))

        tabla.pack(fill=tk.BOTH, expand=True)

    def mostrar_ventas_pendiente(self):
        messagebox.showinfo("Módulo en Desarrollo", "El módulo de Ventas se incorporará en las próximas semanas.")

    def cerrar_sesion(self):
        self.destroy()
        self.on_logout()