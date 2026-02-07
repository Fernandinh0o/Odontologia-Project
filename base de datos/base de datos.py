import sqlite3
DB_NAME = "clinica.db"

#Gestión de Accesos
class Usuario:
    def __init__(self, nombre, telefono, rol, contraseña, id_usuario = None):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.telefono = telefono
        self.rol = rol
        self.contraseña = contraseña

    @staticmethod
    def crear_tabla():
        with sqlite3.connect(DB_NAME) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT, 
                    nombre TEXT NOT NULL,
                    telefono TEXT,
                    rol TEXT NOT NULL,
                    contraseña TEXT NOT NULL 
                );
            """)

    def guardar(self):
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO usuarios (nombre, telefono, rol, contraseña) VALUES (?,?,?,?)",
                (self.nombre, self.telefono, self.rol, self.contraseña)
            )
            self.id_usuario = cursor.lastrowid

    @classmethod
    def login(Usuario,nombre, contraseña_ingresada):
        with sqlite3.connect(DB_NAME) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *FROM usuarios 
                WHERE nombre = ? AND contraseña = ?
            """, (nombre, contraseña_ingresada))
            row = cursor.fetchone()
            if row:
                return Usuario(row['nombre'], row['telefono'], row['rol'], row['contrasena'], row['id_usuario'])
            else:
                return None

class Odontologo(Usuario):
    def __init__(self, nombre, telefono, rol, contraseña, especialidad, id_usuario = None, id_odontologo = None ):
        super().__init__(nombre,telefono, "Odontologo", contraseña, id_usuario)
        self.id_odontologo = id_odontologo
        self.especialidad = especialidad

    @staticmethod
    def crear_tabla():
        with sqlite3.connect(DB_NAME) as conn:
            conn.execute("""
                    CREATE TABLE IF NOT EXISTS odontologos (
                        id_odontologo INTEGER PRIMARY KEY AUTOINCREMENT, 
                        id_usuario INTEGER UNIQUE, 
                        especialidad TEXT NOT NULL, 
                        FOREIGN KEY(id_usuario) REFERENCES usuarios(id_usuario) 
                    );
                """)
    def guardar(self):
        conn = sqlite3.connect(DB_NAME)
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO usuarios (nombre, telefono, rol, contraseña) VALUES (?,?,?,?)",
                (self.nombre, self.telefono, self.rol, self.contraseña)
            )
            self.id_usuario = cursor.lastrowid
            cursor.execute(
                "INSERT INTO odontologos (id_usuario, especialidad, no_colegiado) VALUES (?,?,?)",
                (self.id_usuario, self.especialidad, self.no_colegiado)
            )
            self.id_odontologo = cursor.lastrowid

#Inventario
class Proveedor:
    def __init__(self, nombre, telefono, id_proveedor= None):
        self.nombre = nombre
        self.telefono = telefono
        self.id_proveedor = id_proveedor

    @staticmethod
    def crear_tabla():
        with sqlite3.connect(DB_NAME) as conn:
            conn.execute("""
                   CREATE TABLE IF NOT EXISTS proveedores (
                       id_proveedor INTEGER PRIMARY KEY AUTOINCREMENT, 
                       nombre TEXT NOT NULL,
                       telefono TEXT
                   );
               """)

    def guardar(self):
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO proveedores (nombre, telefono) VALUES (?,?)",
                (self.nombre, self.telefono)
            )
            self.id_proveedor = cursor.lastrowid

class Producto:
    def __init__(self, id_proveedor, nombre, tipo, precio_compra, precio_venta, stock, id_producto = None):
        self.id_producto = id_producto
        self.id_proveedor = id_proveedor
        self.nombre = nombre
        self.tipo = tipo
        self.precio_compra = precio_compra
        self.precio_venta = precio_venta
        self.stock = stock

    @staticmethod
    def crear_tabla():
        Proveedor.crear_tabla()

        with sqlite3.connect(DB_NAME) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS inventario (
                    id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_proveedor INTEGER,
                    nombre TEXT NOT NULL,
                    tipo TEXT,
                    precio_compra REAL,
                    precio_venta REAL,
                    stock INTEGER DEFAULT 0,

                    FOREIGN KEY(id_proveedor) REFERENCES proveedores(id_proveedor)
                );
            """)

    def guardar(self):
        conn = sqlite3.connect(DB_NAME)
        with conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO inventario (id_proveedor, nombre, tipo, precio_compra, precio_venta, stock)
                VALUES (?,?,?,?,?,?)
            """, (self.id_proveedor, self.nombre, self.tipo, self.precio_compra, self.precio_venta, self.stock))
            self.id_producto = cursor.lastrowid