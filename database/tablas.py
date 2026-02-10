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

    sql_tabla_pacientes = """
        CREATE TABLE IF NOT EXISTS Pacientes (
            id_paciente INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            telefono TEXT,
            nit TEXT,
            tiene_seguro BOOLEAN DEFAULT 0,
            aseguradora TEXT
        );
        """

    sql_tabla_tratamientos = """
        CREATE TABLE IF NOT EXISTS Tratamientos (
            id_tratamiento INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            precio_base REAL NOT NULL
        );
        """

    sql_tabla_presupuestos = """
        CREATE TABLE IF NOT EXISTS Presupuestos (
            id_presupuesto INTEGER PRIMARY KEY,
            id_paciente INTEGER NOT NULL,
            fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
            total REAL DEFAULT 0,
            FOREIGN KEY(id_paciente) REFERENCES Pacientes(id_paciente)
        );
        """

    sql_tabla_detalle_presupuesto = """
        CREATE TABLE IF NOT EXISTS Detalle_Presupuesto (
            id_detalle INTEGER PRIMARY KEY,
            id_presupuesto INTEGER NOT NULL,
            id_tratamiento INTEGER NOT NULL,
            pieza_dental TEXT,
            precio_final REAL NOT NULL,
            notas TEXT,
            FOREIGN KEY(id_presupuesto) REFERENCES Presupuestos(id_presupuesto),
            FOREIGN KEY(id_tratamiento) REFERENCES Tratamientos(id_tratamiento)
        );
        """

    sql_tabla_pagos_gastos = """
        CREATE TABLE IF NOT EXISTS Pagos_Gastos (
            id_gasto INTEGER PRIMARY KEY,
            tipo TEXT NOT NULL,
            monto REAL NOT NULL,
            fecha DATE DEFAULT (DATE('now')),
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
            cursor.execute(sql_tabla_ventas)
            cursor.execute(sql_tabla_detalle_ventas)
            cursor.execute(sql_tabla_pacientes)
            cursor.execute(sql_tabla_tratamientos)
            cursor.execute(sql_tabla_presupuestos)
            cursor.execute(sql_tabla_detalle_presupuesto)
            cursor.execute(sql_tabla_pagos_gastos)

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
