from sqlite3 import Error
from database.conexion import crear_conexion
from datetime import datetime
import os

CARPETA_FACTURAS = "facturas"


def cobrar_presupuesto(id_presupuesto):
    conn = crear_conexion()
    try:
        cursor = conn.cursor()

        cursor.execute("SELECT estado, id_paciente, total FROM Presupuestos WHERE id_presupuesto = ?",
                       (id_presupuesto,))
        data = cursor.fetchone()

        if not data:
            return False, "El presupuesto no existe."
        if data[0] == 'PAGADO':
            return False, "Este presupuesto ya fue pagado anteriormente."

        cursor.execute("UPDATE Presupuestos SET estado = 'PAGADO' WHERE id_presupuesto = ?", (id_presupuesto,))
        conn.commit()

        ruta_factura = _generar_txt_factura(id_presupuesto, data[1], data[2])

        return True, f"Cobro exitoso. Factura generada en: {ruta_factura}"

    except Error as e:
        return False, f"Error al cobrar: {e}"
    finally:
        conn.close()


def _generar_txt_factura(id_presupuesto, id_paciente, total):
    if not os.path.exists(CARPETA_FACTURAS):
        os.makedirs(CARPETA_FACTURAS)

    nombre_archivo = f"{CARPETA_FACTURAS}/factura_{id_presupuesto}.txt"

    with open(nombre_archivo, "w") as f:
        f.write("=== CLINICA DENTAL - COMPROBANTE DE PAGO ===\n")
        f.write(f"No. Documento: {id_presupuesto}\n")
        f.write(f"ID Paciente: {id_paciente}\n")
        f.write(f"Fecha de Emisión: {datetime.now()}\n")
        f.write("--------------------------------------------\n")
        f.write(f"TOTAL PAGADO: Q. {total:.2f}\n")
        f.write("--------------------------------------------\n")
        f.write("Gracias por su visita.\n")

    return nombre_archivo

def crear_presupuesto_cabecera(id_paciente, usuario):
    conn = crear_conexion()
    if conn is None:
        raise Error("No hay conexión con BD")
    try:
        cursor = conn.cursor()
        sql = "INSERT INTO Presupuestos (id_paciente, fecha, total) VALUES (?, ?, 0)"
        cursor.execute(sql, (id_paciente, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def agregar_detalle_presupuesto(id_presupuesto, id_tratamiento, pieza, precio, notas):
    conn = crear_conexion()
    try:
        cursor = conn.cursor()
        sql_insert = """
            INSERT INTO Detalle_Presupuesto (id_presupuesto, id_tratamiento, pieza_dental, precio_final, notas)
            VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(sql_insert, (id_presupuesto, id_tratamiento, pieza, precio, notas))

        sql_update = """
            UPDATE Presupuestos 
            SET total = (SELECT SUM(precio_final) FROM Detalle_Presupuesto WHERE id_presupuesto = ?)
            WHERE id_presupuesto = ?
        """
        cursor.execute(sql_update, (id_presupuesto, id_presupuesto))
        conn.commit()
        return True
    finally:
        conn.close()


def obtener_presupuestos_recientes():
    conn = crear_conexion()
    try:
        cursor = conn.cursor()
        sql = """
            SELECT p.id_presupuesto, p.fecha, pac.nombre, p.total 
            FROM Presupuestos p
            JOIN Pacientes pac ON p.id_paciente = pac.id_paciente
            ORDER BY p.id_presupuesto DESC LIMIT 20
        """
        cursor.execute(sql)
        return cursor.fetchall()
    finally:
        conn.close()