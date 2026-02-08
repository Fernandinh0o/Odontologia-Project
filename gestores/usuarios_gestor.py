from database.conexion import crear_conexion
from modelos.usuario import Usuario
from utils.helpers import hash_contrasena, verificar_contrasena

""" Este modulo crea las tablas relacionadas con los usuarios, ademas inserta los usuarios, lista y elimina usuarios
practicamente es la conexion con la base de datos y la interfaz"""

def inicializar_bd(): #Verifica la base de datos. y la conecta
    conn = crear_conexion()
    cursor = conn.cursor()

    _migrar_usuarios(cursor) #Adapta otras versiones de la tabla de usuarios para no perder datos.

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_usuario TEXT NOT NULL UNIQUE,
            telefono TEXT,
            rol TEXT CHECK(rol IN ('Odontologo','Secretaria','Usuario')) NOT NULL,
            contrasena TEXT NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS odontologos (
            id_odontologo INTEGER PRIMARY KEY AUTOINCREMENT,
            id_usuario INTEGER NOT NULL,
            especialidad TEXT,
            FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
        )
        """
    )

    _asegurar_usuarios_base(cursor)
    conn.commit()
    conn.close()


def _migrar_usuarios(cursor):
    cursor.execute(
        """
        SELECT sql
        FROM sqlite_master
        WHERE type = 'table' AND name = 'usuarios'
        """
    )
    fila = cursor.fetchone()
    if not fila:
        return

    if "Usuario" in (fila[0] or ""):
        return

    cursor.execute("PRAGMA foreign_keys=OFF")
    cursor.execute("ALTER TABLE usuarios RENAME TO usuarios_old")

    cursor.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table' AND name = 'odontologos'
        """
    )
    existe_odontologos = cursor.fetchone() is not None
    if existe_odontologos:
        cursor.execute("ALTER TABLE odontologos RENAME TO odontologos_old")

    cursor.execute(
        """
        CREATE TABLE usuarios (
            id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_usuario TEXT NOT NULL UNIQUE,
            telefono TEXT,
            rol TEXT CHECK(rol IN ('Odontologo','Secretaria','Usuario')) NOT NULL,
            contrasena TEXT NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE odontologos (
            id_odontologo INTEGER PRIMARY KEY AUTOINCREMENT,
            id_usuario INTEGER NOT NULL,
            especialidad TEXT,
            FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
        )
        """
    )

    cursor.execute(
        """
        INSERT INTO usuarios (id_usuario, nombre, telefono, rol, contrasena)
        SELECT id_usuario, nombre, telefono, rol, contrasena
        FROM usuarios_old
        """
    )

    if existe_odontologos:
        cursor.execute(
            """
            INSERT INTO odontologos (id_odontologo, id_usuario, especialidad)
            SELECT id_odontologo, id_usuario, especialidad
            FROM odontologos_old
            """
        )
        cursor.execute("DROP TABLE odontologos_old")

    cursor.execute("DROP TABLE usuarios_old")
    cursor.execute("PRAGMA foreign_keys=ON")


def _asegurar_usuarios_base(cursor):
    usuarios_base = [
        Usuario(nombre="luis", telefono=None, rol="Odontologo", contrasena="123", especialidad="General"),
        Usuario(nombre="jose", telefono=None, rol="Secretaria", contrasena="123"),
        Usuario(nombre="fer", telefono=None, rol="Usuario", contrasena="123"),
    ]

    for usuario in usuarios_base:
        cursor.execute(
            "SELECT 1 FROM usuarios WHERE nombre_usuario = ?",
            (usuario.nombre,),
        )
        if cursor.fetchone():
            continue

        pwd_hash = hash_contrasena(usuario.contrasena)
        cursor.execute(
            """
            INSERT INTO usuarios (nombre_usuario, telefono, rol, password_hash)
            VALUES (?, ?, ?, ?)
            """,
            (usuario.nombre, usuario.telefono, usuario.rol, pwd_hash),
        )

        id_usuario = cursor.lastrowid
        if usuario.rol == "Odontologo":
            cursor.execute(
                """
                INSERT INTO odontologos (id_usuario, especialidad)
                VALUES (?, ?)
                """,
                (id_usuario, usuario.especialidad),
            )


def crear_usuario(usuario: Usuario):
    conn = crear_conexion()
    cursor = conn.cursor()

    pwd_hash = hash_contrasena(usuario.contrasena)

    cursor.execute(
        """
        INSERT INTO usuarios (nombre, telefono, rol, contrasena)
        VALUES (?, ?, ?, ?)
        """,
        (usuario.nombre, usuario.telefono, usuario.rol, pwd_hash),
    )

    id_usuario = cursor.lastrowid

    if usuario.rol == "Odontologo":
        cursor.execute(
            """
            INSERT INTO odontologos (id_usuario, especialidad)
            VALUES (?, ?)
            """,
            (id_usuario, usuario.especialidad),
        )

    conn.commit()
    conn.close()


def login(nombre, contrasena):
    conn = crear_conexion()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id_usuario, nombre_usuario, rol, password_hash
        FROM usuarios
        WHERE nombre_usuario = ?
        """,
        (nombre,),
    )

    fila = cursor.fetchone()
    conn.close()

    if fila:
        id_usuario, nombre, rol, pwd_guardada = fila
        if verificar_contrasena(contrasena, pwd_guardada):
            return id_usuario, nombre, rol

    return None


def obtener_usuarios():
    conn = crear_conexion()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id_usuario, nombre_usuario, telefono, rol
        FROM usuarios
        ORDER BY id_usuario
        """
    )

    datos = cursor.fetchall()
    conn.close()
    return datos


def eliminar_usuario(id_usuario):
    conn = crear_conexion()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM usuarios
        WHERE id_usuario = ?
        """,
        (id_usuario,),
    )

    conn.commit()
    conn.close()
