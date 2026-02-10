class Venta:
    """Representa una venta con su detalle para generar factura."""

    def __init__(self, cliente, usuario, detalles, subtotal, impuesto, total):
        self.cliente = cliente
        self.usuario = usuario
        self.detalles = detalles
        self.subtotal = subtotal
        self.impuesto = impuesto
        self.total = total
