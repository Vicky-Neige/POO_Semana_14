import os 
import tkinter as tk
from tkinter import ttk, messagebox

class MainView(tk.Frame):
    def __init__(self, master, servicio, usuario_actual, on_logout):
        super().__init__(master)
        self.master = master
        self.servicio = servicio
        self.restaurante_servicio = servicio
        self.usuario_actual = usuario_actual
        self.on_logout = on_logout

        self.master.title("Restaurante App - Menú Principal")
        self.master.geometry("720x750")


        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ruta_logo = os.path.join(base_dir, "assets", "logo.png")

        if os.path.exists(ruta_logo):
            try:
                self.img_logo = tk.PhotoImage(file=ruta_logo)
                self.img_logo = self.img_logo.subsample(3, 3)
                lbl_logo = tk.Label(self.master, image=self.img_logo)
                lbl_logo.pack(pady=5)
            except Exception as e:
                print(f"No se pudo cargar el logo: {e}")
            else:
                print(f"Ruta no encontrada: {ruta_logo}")

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

        btn_ventas = tk.Button(frame_botones, text="Ventas", width=12, command=self.mostrar_ventas)
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

        productos = self.restaurante_servicio.obtener_productos()
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

    def mostrar_ventas(self):
        self.limpiar_contenido()

        frame_form = ttk.LabelFrame(self.frame_contenido, text=" Registrar Venta ", padding=10)
        frame_form.pack(fill="x", pady=5)

        ttk.Label(frame_form, text="Usuario:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.cb_usuarios = ttk.Combobox(frame_form, state="readonly", width=15)
        self.cb_usuarios.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_form, text="Producto:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.cb_productos = ttk.Combobox(frame_form, state="readonly", width=20)
        self.cb_productos.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(frame_form, text="Cantidad:").grid(row=0, column=4, padx=5, pady=5, sticky="w")
        self.ent_cantidad_venta = ttk.Entry(frame_form, width=8)
        self.ent_cantidad_venta.grid(row=0, column=5, padx=5, pady=5)
        self.ent_cantidad_venta.insert(0, "1")

        btn_registrar = tk.Button(frame_form, text="Registrar Venta", bg="#28a745", fg="white", command=self.callback_registrar_venta)
        btn_registrar.grid(row=0, column=6, padx=10, pady=5)

        frame_tabla = ttk.LabelFrame(self.frame_contenido, text=" Ventas Registradas ", padding=10)
        frame_tabla.pack(fill="both", expand=True, pady=5)

        columnas = ("id_venta", "producto", "cantidad", "precio", "total", "fecha")
        self.tabla_ventas = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=8)

        self.tabla_ventas.heading("id_venta", text="ID")
        self.tabla_ventas.heading("producto", text="Producto")
        self.tabla_ventas.heading("cantidad", text="Cantidad")
        self.tabla_ventas.heading("precio", text="P. Unitario ($)")
        self.tabla_ventas.heading("total", text="Total ($)")
        self.tabla_ventas.heading("fecha", text="Fecha")

        self.tabla_ventas.column("id_venta", width=50, anchor="center")
        self.tabla_ventas.column("producto", width=150)
        self.tabla_ventas.column("cantidad", width=70, anchor="center")
        self.tabla_ventas.column("precio", width=90, anchor="e")
        self.tabla_ventas.column("total", width=90, anchor="e")
        self.tabla_ventas.column("fecha", width=130, anchor="center")

        self.tabla_ventas.pack(fill="both", expand=True)

        self.actualizar_comboboxes_ventas()
        self.cargar_tabla_ventas()

    def actualizar_comboboxes_ventas(self):
        usuarios = self.servicio.obtener_usuarios()
        self.cb_usuarios['values'] = [u.username for u in usuarios]
        if usuarios:
            self.cb_usuarios.current(0)

        productos = self.servicio.obtener_productos()
        self.cb_productos['values'] = [f"{p.id_producto} - {p.nombre}" for p in productos]
        if productos:
            self.cb_productos.current(0)

    def cargar_tabla_ventas(self):
        for item in self.tabla_ventas.get_children():
            self.tabla_ventas.delete(item)

        for v in self.servicio.obtener_ventas():
            v_id = v.get("id_venta") if isinstance(v, dict) else getattr(v, "id_venta", "")
            v_prod = v.get("nombre_producto") if isinstance(v, dict) else getattr(v, "nombre_producto", "")
            v_cant = v.get("cantidad") if isinstance(v, dict) else getattr(v, "cantidad", 0)
            v_prec = v.get("precio_unitario") if isinstance(v, dict) else getattr(v, "precio_unitario", 0.0)
            v_tot = v.get("total") if isinstance(v, dict) else getattr(v, "total", 0.0)
            v_fec = v.get("fecha") if isinstance(v, dict) else getattr(v, "fecha", "")

            self.tabla_ventas.insert("", tk.END, values=(
                v_id, v_prod, v_cant, f"${float(v_prec):.2f}", f"${float(v_tot):.2f}", v_fec
            ))

    def callback_registrar_venta(self):
        prod_sel = self.cb_productos.get()
        cant_str = self.ent_cantidad_venta.get().strip()
        usuario = self.usuario_actual.nombre if hasattr(self.usuario_actual, 'nombre') else str(self.usuario_actual)

        if not prod_sel or not cant_str:
            messagebox.showerror("Error", "Debe seleccionar un producto e ingresar la cantidad.")
            return

        try:
            cant = int(cant_str) 
            if cant <= 0:
                messagebox.showerror("Error", "La cantidad debe ser mayor a 0.")
                return

            id_producto = prod_sel.split(" - ")[0]
            exito, msj = self.servicio.registrar_venta(id_producto, cant)

            if exito:
                messagebox.showinfo("Éxito", msj)
                self.ent_cantidad_venta.delete(0, tk.END)
                self.cargar_tabla_ventas()
                if hasattr(self, 'actualizar_comboboxes_ventas'):
                    self.actualizar_comboboxes_ventas()
            else:
                messagebox.showerror("Error", msj)

        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número entero válido.")

    def cerrar_sesion(self):
        self.destroy()
        self.on_logout()