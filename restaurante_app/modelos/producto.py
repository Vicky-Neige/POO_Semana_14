class Producto:
    def __init__(self, id_producto: int, nombre: str, precio: float, categoria: str, stock: int):
        self.id_producto = id_producto
        self.nombre = nombre
        self.precio = precio
        self.categoria = categoria
        self.stock = stock

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id_producto=data.get("id"),
            nombre=data.get("nombre", ""),
            precio=float(data.get("precio", 0.0)),
            categoria=data.get("categoria", ""),
            stock=int(data.get("stock", 0))
        )
    def to_dict(self):
        return {
            "id": self.id_producto,
            "nombre": self.nombre,
            "precio": self.precio,
            "categoria": self.categoria,
            "stock": self.stock
        }