from datetime import datetime

class Venta:
    def __init__(self, id_venta: int, id_producto: int, nombre_producto: str, cantidad: int, precio_unitario: float, total: float, fecha: str = None):
        self.id_venta = id_venta
        self.id_producto = id_producto
        self.nombre_producto = nombre_producto
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        self.total = total
        self.fecha = fecha if fecha else datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id_venta=data.get("id_venta"),
            id_producto=data.get("id_producto"),
            nombre_producto=data.get("nombre_producto", ""),
            cantidad=int(data.get("cantidad", 0)),
            precio_unitario=float(data.get("precio_unitario", 0.0)),
            total=float(data.get("total", 0.0)),
            fecha=data.get("fecha")
        )

    def to_dict(self):
        return {
            "id_venta": self.id_venta,
            "id_producto": self.id_producto,
            "nombre_producto": self.nombre_producto,
            "cantidad": self.cantidad,
            "precio_unitario": self.precio_unitario,
            "total": self.total,
            "fecha": self.fecha
        }