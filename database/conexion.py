import sqlite3
from sqlite3 import Error

from utilidades.constantes import DATABASE_NAME


def crear_conexion():
    """
    Crea una conexión a la base de datos SQLite.
    El archivo .db se creará en la raíz del proyecto.
    """
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        conn.execute("PRAGMA foreign_keys = ON")
    except Error as exc:
        print(f"Error al conectar con la base de datos '{DATABASE_NAME}': {exc}")
        return None
    return conn


def conectar():
    return crear_conexion()
