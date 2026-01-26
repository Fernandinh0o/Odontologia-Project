from sqlite3 import Error

from database.conexion import crear_conexion
#Crear conexion abre la conexion con la base de datos y reusa el modulo de la conexion.

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


def obtener_productos():
    """Obtiene todos los productos registrados en la base de datos."""
    # Extrae los datos para mostrarlos en la interfaz.
    conn = crear_conexion()
    # Extrae los datos para la interfaz de inventario.
    if conn is None:
        raise Error("No se pudo establecer conexión con la base de datos.")

    try:
        # Ejecuta la consulta para recuperar los productos.
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Productos")
        return cursor.fetchall()
    except Error as exc:
        # Reporta el error de consulta si la operación falla.
        raise Error(f"Error al obtener los productos: {exc}") from exc
    finally:
        # Cierra la conexión para liberar recursos.
        conn.close()
