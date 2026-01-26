from sqlite3 import Error

from database.conexion import crear_conexion


def registrar_producto(producto):
    """Registra un producto en la base de datos.

    Recibe un Producto con nombre, cantidad y precio, e inserta esos datos en la tabla.
    """
    # Crear la conexión a la base de datos.
    conn = crear_conexion()
    # Validar que la conexión sea válida antes de continuar.
    if conn is None:
        raise Error("No se pudo establecer conexión con la base de datos.")

    try:
        # Crear el cursor para ejecutar consultas SQL.
        cursor = conn.cursor()
        # Insertar los datos del producto en la tabla Productos.
        cursor.execute(
            """
            INSERT INTO Productos (nombre, cantidad, precio, descripcion)
            VALUES (?, ?, ?, ?)
            """,
            (producto.nombre, producto.cantidad, producto.precio, producto.descripcion),
        )
        # Confirmar la transacción para guardar los cambios.
        conn.commit()
    except Error as exc:
        # Reportar el error de registro si la operación falla.
        raise Error(f"Error al registrar el producto: {exc}") from exc
    finally:
        # Cerrar la conexión para liberar recursos.
        conn.close()
