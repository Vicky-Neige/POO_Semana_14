from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta
from servicios.archivo_servicio import ArchivoServicio

class RestauranteServicio:
    def __init__(self, ruta_productos: str, ruta_usuarios: str, ruta_ventas: str = None):
        self.ruta_productos = ruta_productos
        self.ruta_usuarios = ruta_usuarios
        self.ruta_ventas = ruta_ventas
        self.productos = []
        self.usuarios = []
        self.ventas = []
        self.cargar_datos()

    def cargar_datos(self):
        raw_productos = ArchivoServicio.cargar_json(self.ruta_productos)
        self.productos = [Producto.from_dict(p) for p in raw_productos]

        raw_usuarios = ArchivoServicio.cargar_json(self.ruta_usuarios)
        self.usuarios = [Usuario.from_dict(u) for u in raw_usuarios]

        if self.ruta_ventas:
            raw_ventas = ArchivoServicio.cargar_json(self.ruta_ventas)
            self.ventas = [Venta.from_dict(v) for v in raw_ventas]

    def guardar_productos(self):
        datos = [p.to_dict() for p in self.productos]
        ArchivoServicio.guardar_json(self.ruta_productos, datos)

    def guardar_ventas(self):
        if self.ruta_ventas:
            datos = [
                v.to_dict() if hasattr(v, 'to_dict') else v 
                for v in self.ventas
            ]
            ArchivoServicio.guardar_json(self.ruta_ventas, datos)

    def validar_acceso(self, username: str, password: str) -> Usuario:
        for usuario in self.usuarios:
            if usuario.username == username and usuario.password == password:
                return usuario
        return None

    def obtener_usuarios(self) -> list:
        return self.usuarios

    def obtener_productos(self) -> list:
        return self.productos

    def obtener_producto_por_id(self, id_prod):
        for p in self.productos:
            if str(p.id_producto) == str(id_prod):
                return p
        return None

    def agregar_producto(self, id_prod, nombre, precio, categoria, stock):
        if not id_prod or not nombre:
            return False, "El ID y el Nombre son obligatorios."

        if self.obtener_producto_por_id(id_prod):
            return False, f"El producto con ID '{id_prod}' ya existe."

        try:
            precio_val = float(precio)
            stock_val = int(stock)
        except ValueError:
            return False, "El precio debe ser un número y el stock un número entero."

        nuevo_prod = Producto(id_prod, nombre, precio_val, categoria, stock_val)
        self.productos.append(nuevo_prod)
        self.guardar_productos()
        return True, "Producto registrado correctamente."

    def actualizar_producto(self, id_prod, nombre, precio, categoria, stock):
        if not id_prod:
            return False, "Debe especificar un ID para actualizar."

        prod = self.obtener_producto_por_id(id_prod)
        if not prod:
            return False, f"No se encontró ningún producto con ID '{id_prod}'."

        try:
            precio_val = float(precio)
            stock_val = int(stock)
        except ValueError:
            return False, "El precio debe ser un número y el stock un número entero."

        prod.nombre = nombre
        prod.precio = precio_val
        prod.categoria = categoria
        prod.stock = stock_val

        self.guardar_productos()
        return True, "Producto actualizado correctamente."

    def eliminar_producto(self, id_prod):
        if not id_prod:
            return False, "Debe especificar un ID para eliminar."

        prod = self.obtener_producto_por_id(id_prod)
        if not prod:
            return False, f"No se encontró el producto con ID '{id_prod}'."

        self.productos.remove(prod)
        self.guardar_productos()
        return True, "Producto eliminado correctamente."

    def registrar_venta(self, id_producto, cantidad):
        producto = self.obtener_producto_por_id(id_producto)
        if not producto:
            return False, "El producto seleccionado no existe."

        cantidad = int(cantidad)

        if producto.stock < cantidad:
            return False, f"Stock insuficiente. Disponible: {producto.stock}"

        producto.stock -= cantidad
        self.guardar_productos()

        from datetime import datetime
        id_venta = str(len(self.ventas) + 1)
        total = producto.precio * cantidad
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        nueva_venta = {
            "id_venta": id_venta,
            "id_producto": id_producto,
            "nombre_producto": producto.nombre,
            "cantidad": cantidad,
            "precio_unitario": producto.precio,
            "total": total,
            "fecha": fecha
        }

        self.ventas.append(nueva_venta)
        self.guardar_ventas()

        return True, "Venta registrada con éxito."

    def obtener_ventas(self) -> list:
        return self.ventas