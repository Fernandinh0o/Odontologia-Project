class Producto:
    def __init__(self, nombre, cantidad, precio, descripcion="", id_producto=None):
        self.id = id_producto
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio
        self.descripcion = descripcion
