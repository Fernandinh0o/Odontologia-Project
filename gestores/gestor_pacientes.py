from sqlite3 import Error
from database.conexion import crear_conexion


def registrar_paciente(nombre, telefono, nit, tiene_seguro, aseguradora):
    conn = crear_conexion()
    if conn is None:
        return False, "No hay conexión con la base de datos"

    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Pacientes (nombre, telefono, nit, tiene_seguro, aseguradora)
            VALUES (?, ?, ?, ?, ?)
        """, (nombre, telefono, nit, tiene_seguro, aseguradora))
        conn.commit()
        return True, "Paciente registrado correctamente."
    except Error as e:
        return False, f"Error al registrar: {e}"
    finally:
        conn.close()


def buscar_pacientes(texto_busqueda=""):
    conn = crear_conexion()
    try:
        cursor = conn.cursor()
        sql = "SELECT * FROM Pacientes WHERE 1=1"
        if texto_busqueda:
            sql += f" AND (nombre LIKE '%{texto_busqueda}%' OR nit LIKE '%{texto_busqueda}%')"

        cursor.execute(sql)
        return cursor.fetchall()
    finally:
        conn.close()