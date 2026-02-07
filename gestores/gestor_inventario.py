from sqlite3 import Error

from database.conexion import crear_conexion


def validar_campos_numericos(cantidad, precio_unitario, stock_minimo):
    """Valida que los campos numéricos no estén vacíos y sean positivos."""
    if cantidad is None or precio_unitario is None or stock_minimo is None:
        raise ValueError("Los campos numéricos son obligatorios.")

    if cantidad < 0 or stock_minimo < 0:
        raise ValueError("Cantidad y stock mínimo deben ser cero o positivos.")

    if precio_unitario <= 0:
        raise ValueError("El precio unitario debe ser mayor que cero.")


def calcular_estado(cantidad, stock_minimo):
    """Calcula el estado del producto en base a la cantidad y stock mínimo."""
    if cantidad == 0:
        return "Agotado"
    if cantidad <= stock_minimo:
        return "Bajo stock"
    return "Disponible"


def calcular_valor_total(cantidad, precio_unitario):
    """Calcula el valor total del inventario para el producto."""
    return cantidad * precio_unitario


def _validar_id_unico(cursor, id_producto):
    cursor.execute("SELECT 1 FROM Productos WHERE id_producto = ?", (id_producto,))
    if cursor.fetchone():
        raise ValueError("El id_producto ya existe. Debe ser único.")


def registrar_producto(producto):
    """Registra un producto en la base de datos."""
    conn = crear_conexion()
    if conn is None:
        raise Error("No se pudo establecer conexión con la base de datos.")

    try:
        cursor = conn.cursor()
        _validar_id_unico(cursor, producto.id_producto)
        validar_campos_numericos(
            producto.cantidad,
            producto.precio_unitario,
            producto.stock_minimo,
        )
        producto.estado = calcular_estado(
            producto.cantidad,
            producto.stock_minimo,
        )
        producto.valor_total = calcular_valor_total(
            producto.cantidad,
            producto.precio_unitario,
        )
        cursor.execute(
            """
            INSERT INTO Productos (
                id_producto,
                nombre,
                categoria,
                cantidad,
                precio_unitario,
                stock_minimo,
                proveedor,
                descripcion
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                producto.id_producto,
                producto.nombre,
                producto.categoria,
                producto.cantidad,
                producto.precio_unitario,
                producto.stock_minimo,
                producto.proveedor,
                producto.descripcion,
            ),
        )
        conn.commit()
    except (Error, ValueError) as exc:
        raise Error(f"Error al registrar el producto: {exc}") from exc
    finally:
        conn.close()


def actualizar_producto(producto):
    """Actualiza un producto existente en la base de datos."""
    conn = crear_conexion()
    if conn is None:
        raise Error("No se pudo establecer conexión con la base de datos.")

    try:
        cursor = conn.cursor()
        validar_campos_numericos(
            producto.cantidad,
            producto.precio_unitario,
            producto.stock_minimo,
        )
        producto.estado = calcular_estado(
            producto.cantidad,
            producto.stock_minimo,
        )
        producto.valor_total = calcular_valor_total(
            producto.cantidad,
            producto.precio_unitario,
        )
        cursor.execute(
            """
            UPDATE Productos
            SET nombre = ?,
                categoria = ?,
                cantidad = ?,
                precio_unitario = ?,
                stock_minimo = ?,
                proveedor = ?,
                descripcion = ?
            WHERE id_producto = ?
            """,
            (
                producto.nombre,
                producto.categoria,
                producto.cantidad,
                producto.precio_unitario,
                producto.stock_minimo,
                producto.proveedor,
                producto.descripcion,
                producto.id_producto,
            ),
        )
        if cursor.rowcount == 0:
            raise ValueError("No existe un producto con ese id_producto.")
        conn.commit()
    except (Error, ValueError) as exc:
        raise Error(f"Error al actualizar el producto: {exc}") from exc
    finally:
        conn.close()


def obtener_productos():
    """Obtiene todos los productos registrados en la base de datos."""
    conn = crear_conexion()
    if conn is None:
        raise Error("No se pudo establecer conexión con la base de datos.")

    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id_producto, nombre, categoria, cantidad, precio_unitario,
                   stock_minimo, proveedor, descripcion
            FROM Productos
            """
        )
        return cursor.fetchall()
    except Error as exc:
        raise Error(f"Error al obtener los productos: {exc}") from exc
    finally:
        conn.close()
