import sqlite3
from sqlite3 import Error

from .conexion import crear_conexion


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
        password_hash TEXT NOT NULL,
        rol TEXT NOT NULL CHECK(rol IN ('Admin', 'Empleado'))
    );
    """

    # 2. Tabla de Productos
    sql_tabla_productos = """
    CREATE TABLE IF NOT EXISTS Productos (
        id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        cantidad INTEGER NOT NULL,
        precio REAL NOT NULL,
        descripcion TEXT
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

            conn.commit()
            print("Tablas listas.")

        except Error as exc:
            print(f"Error al crear las tablas: {exc}")
        finally:
            if conn:
                conn.close()
    else:
        print("Error: No se pudo crear la conexión a la base de datos.")
