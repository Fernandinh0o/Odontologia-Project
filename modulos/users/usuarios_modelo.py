import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from database.conexion import conectar
from utils.helpers import hash_contrasena, verificar_contrasena

def inicializar_bd():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE,
        telefono TEXT,
        rol TEXT CHECK(rol IN ('Odontologo','Secretaria')) NOT NULL,
        contrasena TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS odontologos (
        id_odontologo INTEGER PRIMARY KEY AUTOINCREMENT,
        id_usuario INTEGER NOT NULL,
        especialidad TEXT,
        FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
    )
    """)

    conn.commit()
    conn.close()


def crear_usuario(nombre, telefono, rol, contrasena, especialidad=None):
    conn = conectar()
    cursor = conn.cursor()

    pwd_hash = hash_contrasena(contrasena)

    cursor.execute("""
    INSERT INTO usuarios (nombre, telefono, rol, contrasena)
    VALUES (?, ?, ?, ?)
    """, (nombre, telefono, rol, pwd_hash))

    id_usuario = cursor.lastrowid

    if rol == "Odontologo":
        cursor.execute("""
        INSERT INTO odontologos (id_usuario, especialidad)
        VALUES (?, ?)
        """, (id_usuario, especialidad))

    conn.commit()
    conn.close()


def login(nombre, contrasena):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id_usuario, nombre, rol, contrasena
    FROM usuarios
    WHERE nombre = ?
    """, (nombre,))

    fila = cursor.fetchone()
    conn.close()

    if fila:
        id_usuario, nombre, rol, pwd_guardada = fila
        if verificar_contrasena(contrasena, pwd_guardada):
            return id_usuario, nombre, rol

    return None

def obtener_usuarios():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id_usuario, nombre, telefono, rol
    FROM usuarios
    ORDER BY id_usuario
    """)

    datos = cursor.fetchall()
    conn.close()
    return datos


def eliminar_usuario(id_usuario):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM usuarios
    WHERE id_usuario = ?
    """, (id_usuario,))

    conn.commit()
    conn.close()
