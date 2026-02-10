import sqlite3
from sqlite3 import Error

from .conexion import crear_conexion
""" Va para empezar aqui se utiliza SQL y genera un init.py de manera OBLIGATORIA asi que no deberia ocurrir algun 
error pero sepa"""

def crear_tablas_iniciales():
    """
    Crea todas las tablas necesarias para el sistema si no existen.
    """
    # Definición de Tablas SQL

    # 1. Tabla de Usuarios
    sql_tabla_usuarios = """
    CREATE TABLE IF NOT EXISTS Usuarios (
        id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_usuario TEXT NOT NULL UNIQUE,
        telefono TEXT,
        password_hash TEXT NOT NULL,
        rol TEXT NOT NULL CHECK(rol IN ('Admin', 'Empleado','Secretaria','Odontologo','Usuario'))
    );
    """

    # 2. Tabla de Productos
    sql_tabla_productos = """
    CREATE TABLE IF NOT EXISTS Productos (
        id_producto INTEGER PRIMARY KEY,
        nombre TEXT NOT NULL,
        categoria TEXT NOT NULL,
        cantidad INTEGER NOT NULL,
        precio_unitario REAL NOT NULL,
        stock_minimo INTEGER NOT NULL,
        proveedor TEXT NOT NULL,
        descripcion TEXT
    );
    """

    # 3. Tabla de Ventas
    sql_tabla_ventas = """
    CREATE TABLE IF NOT EXISTS Ventas (
        id_venta INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha_venta TEXT NOT NULL,
        cliente TEXT NOT NULL,
        usuario TEXT NOT NULL,
        subtotal REAL NOT NULL,
        impuesto REAL NOT NULL,
        total REAL NOT NULL,
        ruta_factura TEXT
    );
    """

    # 4. Tabla de Detalle de Ventas
    sql_tabla_detalle_ventas = """
    CREATE TABLE IF NOT EXISTS DetalleVentas (
        id_detalle INTEGER PRIMARY KEY AUTOINCREMENT,
        id_venta INTEGER NOT NULL,
        id_producto INTEGER NOT NULL,
        cantidad INTEGER NOT NULL,
        precio_unitario REAL NOT NULL,
        subtotal REAL NOT NULL,
        FOREIGN KEY (id_venta) REFERENCES Ventas(id_venta),
        FOREIGN KEY (id_producto) REFERENCES Productos(id_producto)
    );
    """

    # Ejecución de Comandos
    conn = crear_conexion()

    if conn is not None:
        try:
            cursor = conn.cursor()

            # Ejecutamos la creación de cada tabla
            print("Creando/Verificando tablas...")
            cursor.execute(sql_tabla_usuarios)
            cursor.execute(sql_tabla_productos)
            cursor.execute(sql_tabla_ventas)
            cursor.execute(sql_tabla_detalle_ventas)

            conn.commit()
            print("Tablas listas.")

        except Error as exc:
            print(f"Error al crear las tablas: {exc}")
        finally:
            if conn:
                conn.close()
    else:
        print("Error: No se pudo crear la conexión a la base de datos.")

""" Este modulo no inserta o crea de una vez los usuarios solo hace las tablas si no existen,
si ya existen no pasa nada. Mas que todo se uso para crear las tablas y ya"""
