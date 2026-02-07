import sqlite3
from sqlite3 import Error

from utilidades.constantes import DATABASE_NAME

"""" Practicamente es el enlace al sistema, sin esto nada funciona. Esta automatizado de manera que no hay
que colocar db en cada archivo, es automatico."""


def crear_conexion():
    """
    Crea una conexión a la base de datos SQLite.
    El archivo .db se creará en la raíz del proyecto.
    """
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_NAME) #Esto crea la base de datos.
        conn.execute("PRAGMA foreign_keys = ON")
    except Error as exc:
        print(f"Error al conectar con la base de datos '{DATABASE_NAME}': {exc}")
        return None
    return conn


def conectar():
    return crear_conexion()

""" Cabe aclarar que este archivo/modulo no crea tablas solo es la conexion principal."""