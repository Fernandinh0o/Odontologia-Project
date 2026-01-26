from sqlite3 import Error

from database.conexion import crear_conexion


def registrar_producto(producto):
    conn = crear_conexion()
    if conn is None:
        raise Error("No se pudo establecer conexión con la base de datos.")

    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO Productos (nombre, cantidad, precio, descripcion)
            VALUES (?, ?, ?, ?)
            """,
            (producto.nombre, producto.cantidad, producto.precio, producto.descripcion),
        )
        conn.commit()
    except Error as exc:
        raise Error(f"Error al registrar el producto: {exc}") from exc
    finally:
        conn.close()
