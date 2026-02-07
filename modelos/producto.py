class Producto:
    """ Aqui se define lo que vendria siendo el producto, de momento como no se conocen todos los 
    parametros solo es un borrador por decir asi."""
    
    def __init__(self, nombre, cantidad, precio, descripcion="", id_producto=None):
        self.id = id_producto
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio
        self.descripcion = descripcion
