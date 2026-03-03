import sqlite3
from sqlite3 import Error
from .conexion import crear_conexion


def crear_tablas_iniciales():
    """
    Crea todas las tablas necesarias para el sistema si no existen.
    """

    sql_tabla_usuarios = """
    CREATE TABLE IF NOT EXISTS Usuarios (
        id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_usuario TEXT NOT NULL UNIQUE,
        telefono TEXT,
        password_hash TEXT NOT NULL,
        rol TEXT NOT NULL CHECK(rol IN ('Admin', 'Empleado','Secretaria','Odontologo','Usuario'))
    );
    """

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
        aseguradora TEXT,
        poliza TEXT
    );
    """

    sql_tabla_tratamientos = """
    CREATE TABLE IF NOT EXISTS Tratamientos (
        id_tratamiento INTEGER PRIMARY KEY,
        nombre TEXT NOT NULL,
        precio_base REAL NOT NULL,
        es_clinico BOOLEAN DEFAULT 1
    );
    """

    sql_tabla_presupuestos = """
    CREATE TABLE IF NOT EXISTS Presupuestos (
        id_presupuesto INTEGER PRIMARY KEY,
        id_paciente INTEGER NOT NULL,
        fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
        total REAL DEFAULT 0,
        estado TEXT DEFAULT 'Pendiente',
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
        descripcion TEXT,
        es_confidencial BOOLEAN DEFAULT 0
    );
    """

    sql_tabla_nomina = """
    CREATE TABLE IF NOT EXISTS Nominas (
        id_pago INTEGER PRIMARY KEY AUTOINCREMENT,
        id_usuario INTEGER NOT NULL,
        fecha DATE DEFAULT (DATE('now')),
        concepto TEXT NOT NULL,
        monto_base REAL NOT NULL,
        bonificaciones REAL DEFAULT 0,
        deducciones REAL DEFAULT 0,
        total_pagado REAL NOT NULL,
        FOREIGN KEY(id_usuario) REFERENCES Usuarios(id_usuario)
    );
    """

    def insertar_datos_prueba(cursor):
        cursor.execute("SELECT COUNT(*) FROM Tratamientos")
        if cursor.fetchone()[0] == 0:
            print("Insertando tratamientos base...")
            tratamientos_base = [
                (1, 'Consulta General', 150.00, 0),
                (2, 'Limpieza Dental', 250.00, 0),
                (3, 'Extracción Simple', 300.00, 1),
                (4, 'Extracción Cordal', 800.00, 1),
                (5, 'Blanqueamiento', 1500.00, 0)
            ]
            cursor.executemany("""
                INSERT INTO Tratamientos (id_tratamiento, nombre, precio_base, es_clinico) 
                VALUES (?, ?, ?, ?)
            """, tratamientos_base)

        cursor.execute("SELECT COUNT(*) FROM Pacientes")
        if cursor.fetchone()[0] == 0:
            print("Insertando pacientes de prueba...")
            pacientes_base = [
                (1, 'Juan Pérez', '5555-1234', '123456-7', 0, None, None),
                (2, 'Maria Lopez', '4444-5678', '987654-3', 1, 'Seguros Roble', 'P-1001'),
                (3, 'Carlos Martinez', '1234-4321', 'CF', 0, None, None)
            ]
            cursor.executemany("""
                    INSERT INTO Pacientes (id_paciente, nombre, telefono, nit, tiene_seguro, aseguradora, poliza) 
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, pacientes_base)

    conn = crear_conexion()

    if conn is not None:
        try:
            cursor = conn.cursor()

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
            cursor.execute(sql_tabla_nomina)

            insertar_datos_prueba(cursor)

            conn.commit()
            print("Tablas listas.")

        except Error as exc:
            print(f"Error al crear las tablas: {exc}")
        finally:
            if conn:
                conn.close()
    else:
        print("Error: No se pudo crear la conexión a la base de datos.")
