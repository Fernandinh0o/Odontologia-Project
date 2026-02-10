import os
from datetime import datetime
from sqlite3 import Error

from database.conexion import crear_conexion
from modelos.venta import Venta

IMPUESTO_PORCENTAJE = 0.13
CARPETA_FACTURAS = "facturas"


def obtener_productos_disponibles():
    """Obtiene productos con stock mayor a cero para realizar ventas."""
    conn = crear_conexion()
    if conn is None:
        raise Error("No se pudo establecer conexión con la base de datos.")

    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id_producto, nombre, cantidad, precio_unitario
            FROM Productos
            WHERE cantidad > 0
            ORDER BY nombre ASC
            """
        )
        return cursor.fetchall()
    except Error as exc:
        raise Error(f"Error al obtener productos disponibles: {exc}") from exc
    finally:
        conn.close()


def _validar_lineas(lineas):
    if not lineas:
        raise ValueError("Debe agregar al menos un producto a la venta.")

    for linea in lineas:
        if linea["cantidad"] <= 0:
            raise ValueError("La cantidad por producto debe ser mayor que cero.")


def _construir_venta(cliente, usuario, lineas):
    _validar_lineas(lineas)
    subtotal = sum(linea["subtotal"] for linea in lineas)
    impuesto = round(subtotal * IMPUESTO_PORCENTAJE, 2)
    total = round(subtotal + impuesto, 2)
    return Venta(cliente=cliente, usuario=usuario, detalles=lineas, subtotal=subtotal, impuesto=impuesto, total=total)


def registrar_venta(cliente, usuario, lineas):
    """Registra una venta, descuenta inventario y genera el documento de factura."""
    venta = _construir_venta(cliente, usuario, lineas)
    conn = crear_conexion()
    if conn is None:
        raise Error("No se pudo establecer conexión con la base de datos.")

    try:
        cursor = conn.cursor()
        for linea in venta.detalles:
            cursor.execute(
                "SELECT nombre, cantidad, precio_unitario FROM Productos WHERE id_producto = ?",
                (linea["id_producto"],),
            )
            producto = cursor.fetchone()
            if not producto:
                raise ValueError(f"No existe el producto con ID {linea['id_producto']}.")

            _, stock_actual, precio_actual = producto
            if linea["cantidad"] > stock_actual:
                raise ValueError(
                    f"Stock insuficiente para el producto {linea['id_producto']}. Disponible: {stock_actual}."
                )

            if abs(float(precio_actual) - float(linea["precio_unitario"])) > 0.001:
                linea["precio_unitario"] = float(precio_actual)
                linea["subtotal"] = round(float(precio_actual) * linea["cantidad"], 2)

        venta = _construir_venta(cliente, usuario, venta.detalles)

        cursor.execute(
            """
            INSERT INTO Ventas (fecha_venta, cliente, usuario, subtotal, impuesto, total)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                venta.cliente,
                venta.usuario,
                venta.subtotal,
                venta.impuesto,
                venta.total,
            ),
        )
        id_venta = cursor.lastrowid

        for linea in venta.detalles:
            cursor.execute(
                """
                INSERT INTO DetalleVentas (id_venta, id_producto, cantidad, precio_unitario, subtotal)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    id_venta,
                    linea["id_producto"],
                    linea["cantidad"],
                    linea["precio_unitario"],
                    linea["subtotal"],
                ),
            )
            cursor.execute(
                """
                UPDATE Productos
                SET cantidad = cantidad - ?
                WHERE id_producto = ?
                """,
                (linea["cantidad"], linea["id_producto"]),
            )

        ruta_factura = generar_factura_txt(id_venta, venta)
        cursor.execute(
            "UPDATE Ventas SET ruta_factura = ? WHERE id_venta = ?",
            (ruta_factura, id_venta),
        )

        conn.commit()
        return id_venta, ruta_factura
    except (Error, ValueError) as exc:
        conn.rollback()
        raise Error(f"Error al registrar la venta: {exc}") from exc
    finally:
        conn.close()


def generar_factura_txt(id_venta, venta):
    """Genera una factura en texto plano para la venta registrada."""
    os.makedirs(CARPETA_FACTURAS, exist_ok=True)
    ruta = os.path.join(CARPETA_FACTURAS, f"factura_{id_venta}.txt")

    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write("CLÍNICA DENTAL - FACTURA\n")
        archivo.write(f"Número de factura: {id_venta}\n")
        archivo.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        archivo.write(f"Cliente: {venta.cliente}\n")
        archivo.write(f"Atendido por: {venta.usuario}\n")
        archivo.write("=" * 50 + "\n")
        archivo.write("DETALLE\n")
        archivo.write("ID | Producto | Cantidad | P. Unitario | Subtotal\n")
        archivo.write("-" * 50 + "\n")

        for linea in venta.detalles:
            archivo.write(
                f"{linea['id_producto']} | {linea['nombre']} | {linea['cantidad']} | "
                f"₡{linea['precio_unitario']:.2f} | ₡{linea['subtotal']:.2f}\n"
            )

        archivo.write("-" * 50 + "\n")
        archivo.write(f"Subtotal: ₡{venta.subtotal:.2f}\n")
        archivo.write(f"Impuesto (13%): ₡{venta.impuesto:.2f}\n")
        archivo.write(f"TOTAL: ₡{venta.total:.2f}\n")

    return ruta


def obtener_ventas():
    """Lista las ventas registradas junto con su factura generada."""
    conn = crear_conexion()
    if conn is None:
        raise Error("No se pudo establecer conexión con la base de datos.")

    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id_venta, fecha_venta, cliente, usuario, subtotal, impuesto, total, ruta_factura
            FROM Ventas
            ORDER BY id_venta DESC
            """
        )
        return cursor.fetchall()
    except Error as exc:
        raise Error(f"Error al obtener las ventas: {exc}") from exc
    finally:
        conn.close()
