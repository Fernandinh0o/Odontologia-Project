from sqlite3 import Error
from database.conexion import crear_conexion

def registrar_tratamiento(nombre, precio_base):
    conn = crear_conexion()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Tratamientos (nombre, precio_base) VALUES (?, ?)",
                       (nombre, precio_base))
        conn.commit()
        return True, "Tratamiento agregado."
    except Error as e:
        return False, f"Error: {e}"
    finally:
        conn.close()

def obtener_tratamientos():
    conn = crear_conexion()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Tratamientos ORDER BY nombre ASC")
        return cursor.fetchall()
    finally:
        conn.close()