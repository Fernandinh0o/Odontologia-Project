class Producto:
    """Define la estructura del producto para el inventario."""

    def __init__(
        self,
        id_producto,
        nombre,
        categoria,
        cantidad,
        precio_unitario,
        stock_minimo,
        proveedor,
        descripcion="",
        estado="",
        valor_total=0.0,
    ):
        self.id_producto = id_producto
        self.nombre = nombre
        self.categoria = categoria
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        self.stock_minimo = stock_minimo
        self.proveedor = proveedor
        self.descripcion = descripcion
        self.estado = estado
        self.valor_total = valor_total
