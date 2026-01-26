import sqlite3
DB_NAME = "clinica.db"

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