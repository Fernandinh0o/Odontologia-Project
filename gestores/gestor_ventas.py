from sqlite3 import Error
from database.conexion import crear_conexion


def crear_nuevo_presupuesto(id_paciente):
    conn = crear_conexion()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Presupuestos (id_paciente, total, estado) VALUES (?, 0, 'Pendiente')",
                       (id_paciente,))
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def agregar_item_presupuesto(id_presupuesto, id_tratamiento, pieza, precio_final, notas):
    conn = crear_conexion()
    try:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO Detalle_Presupuesto (id_presupuesto, id_tratamiento, pieza_dental, precio_final, notas)
            VALUES (?, ?, ?, ?, ?)
        """, (id_presupuesto, id_tratamiento, pieza, precio_final, notas))

        cursor.execute("""
            UPDATE Presupuestos 
            SET total = (SELECT SUM(precio_final) FROM Detalle_Presupuesto WHERE id_presupuesto = ?)
            WHERE id_presupuesto = ?
        """, (id_presupuesto, id_presupuesto))

        conn.commit()
        return True, "Item agregado."
    except Error as e:
        return False, f"Error: {e}"
    finally:
        conn.close()


def obtener_detalle_presupuesto(id_presupuesto):
    conn = crear_conexion()
    try:
        cursor = conn.cursor()
        sql = """
            SELECT d.pieza_dental, t.nombre, d.precio_final, d.notas
            FROM Detalle_Presupuesto d
            JOIN Tratamientos t ON d.id_tratamiento = t.id_tratamiento
            WHERE d.id_presupuesto = ?
        """
        cursor.execute(sql, (id_presupuesto,))
        return cursor.fetchall()
    finally:
        conn.close()