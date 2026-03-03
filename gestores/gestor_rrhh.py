from sqlite3 import Error
from database.conexion import crear_conexion

PORCENTAJE_IGSS_LABORAL = 0.0483  # 4.83%
PORCENTAJE_CUOTA_PATRONAL = 0.1267  # 12.67%
BONIFICACION_LEY = 250.00


def obtener_empleados():
    conn = crear_conexion()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id_usuario, nombre_usuario, rol FROM Usuarios")
        return cursor.fetchall()
    finally:
        conn.close()


def calcular_nomina_teorica(salario_base, comisiones=0):

    total_afecto_igss = salario_base + comisiones

    igss_laboral = round(total_afecto_igss * PORCENTAJE_IGSS_LABORAL, 2)

    total_liquido = (salario_base + comisiones + BONIFICACION_LEY) - igss_laboral

    costo_patronal = round(total_afecto_igss * PORCENTAJE_CUOTA_PATRONAL, 2)

    return {
        "base": salario_base,
        "comisiones": comisiones,
        "bono_ley": BONIFICACION_LEY,
        "igss_laboral": igss_laboral,
        "total_liquido": total_liquido,
        "costo_patronal": costo_patronal
    }


def registrar_pago_nomina(id_usuario, concepto, base, comisiones, otros_descuentos):
    """
    Calcula y guarda el pago final.
    """
    calculos = calcular_nomina_teorica(base, comisiones)

    ingresos_totales = base + comisiones + BONIFICACION_LEY
    deducciones_totales = calculos['igss_laboral'] + otros_descuentos
    total_pagado = ingresos_totales - deducciones_totales

    conn = crear_conexion()
    try:
        cursor = conn.cursor()

        sql = """
            INSERT INTO Nominas (id_usuario, concepto, monto_base, bonificaciones, deducciones, total_pagado)
            VALUES (?, ?, ?, ?, ?, ?)
        """

        cursor.execute(sql, (
            id_usuario,
            concepto,
            base,
            (comisiones + BONIFICACION_LEY),
            deducciones_totales,
            total_pagado
        ))


        cursor.execute("""
            INSERT INTO Pagos_Gastos (tipo, monto, descripcion, es_confidencial)
            VALUES ('Sueldos', ?, ?, 1)
        """, (total_pagado, f"Nómina: {concepto} - Usuario {id_usuario}"))

        conn.commit()
        return True, f"Pago registrado. Líquido: Q{total_pagado:.2f}"
    except Error as e:
        return False, f"Error: {e}"
    finally:
        conn.close()


def obtener_historial_pagos(id_usuario):
    conn = crear_conexion()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id_pago, fecha, concepto, total_pagado 
            FROM Nominas 
            WHERE id_usuario = ? 
            ORDER BY id_pago DESC
        """, (id_usuario,))
        return cursor.fetchall()
    finally:
        conn.close()