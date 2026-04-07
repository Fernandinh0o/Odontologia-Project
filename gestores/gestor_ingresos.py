from sqlite3 import Error
from datetime import datetime

from database.conexion import crear_conexion


TIPO_PAGO_TRATAMIENTO = "Pago Tratamiento"
TIPO_ABONO_SEGURO = "Abono Seguro"


def _asegurar_tablas_caja():
    ok, _ = crear_tablas_caja()
    return ok


def crear_tablas_caja():
    """
    Crea las tablas mínimas para operar caja de ingresos.
    Si ya existen, no realiza cambios.
    """
    conn = crear_conexion()
    if conn is None:
        return False, "No hay conexión con la base de datos"

    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Pacientes (
                id_paciente INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                telefono TEXT,
                nit TEXT,
                tiene_seguro BOOLEAN DEFAULT 0,
                aseguradora TEXT,
                poliza TEXT
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Citas (
                id_cita INTEGER PRIMARY KEY AUTOINCREMENT,
                id_paciente INTEGER NOT NULL,
                fecha_cita TEXT NOT NULL,
                motivo TEXT,
                estado TEXT DEFAULT 'Programada',
                FOREIGN KEY (id_paciente) REFERENCES Pacientes(id_paciente)
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Ingresos_Caja (
                id_ingreso INTEGER PRIMARY KEY AUTOINCREMENT,
                id_paciente INTEGER NOT NULL,
                id_cita INTEGER,
                tipo_ingreso TEXT NOT NULL,
                monto REAL NOT NULL,
                metodo_pago TEXT,
                referencia TEXT,
                fecha_registro TEXT NOT NULL,
                observaciones TEXT,
                FOREIGN KEY (id_paciente) REFERENCES Pacientes(id_paciente),
                FOREIGN KEY (id_cita) REFERENCES Citas(id_cita)
            )
            """
        )

        conn.commit()
        return True, "Tablas de caja listas"
    except Error as e:
        return False, f"Error al crear tablas de caja: {e}"
    finally:
        conn.close()


def _obtener_paciente(cursor, id_paciente):
    cursor.execute(
        """
        SELECT id_paciente, nombre, tiene_seguro
        FROM Pacientes
        WHERE id_paciente = ?
        """,
        (id_paciente,),
    )
    return cursor.fetchone()


def _obtener_cita(cursor, id_cita):
    cursor.execute(
        """
        SELECT id_cita, id_paciente, fecha_cita, estado
        FROM Citas
        WHERE id_cita = ?
        """,
        (id_cita,),
    )
    return cursor.fetchone()


def registrar_pago_tratamiento(id_paciente, id_cita, monto, metodo_pago="Efectivo", referencia=None, observaciones=""):
    """
    Registra en caja un pago de tratamiento realizado por un paciente.
    """
    if monto <= 0:
        return False, "El monto debe ser mayor que cero"
    if not _asegurar_tablas_caja():
        return False, "No fue posible preparar tablas de caja"

    conn = crear_conexion()
    if conn is None:
        return False, "No hay conexión con la base de datos"

    try:
        cursor = conn.cursor()

        paciente = _obtener_paciente(cursor, id_paciente)
        if not paciente:
            return False, "Paciente no encontrado"

        cita = _obtener_cita(cursor, id_cita)
        if not cita:
            return False, "Cita no encontrada"

        if cita[1] != id_paciente:
            return False, "La cita no pertenece al paciente indicado"

        cursor.execute(
            """
            INSERT INTO Ingresos_Caja (
                id_paciente, id_cita, tipo_ingreso, monto, metodo_pago,
                referencia, fecha_registro, observaciones
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                id_paciente,
                id_cita,
                TIPO_PAGO_TRATAMIENTO,
                monto,
                metodo_pago,
                referencia,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                observaciones,
            ),
        )

        conn.commit()
        return True, "Pago de tratamiento registrado"
    except Error as e:
        return False, f"Error al registrar pago: {e}"
    finally:
        conn.close()


def registrar_abono_seguro(id_paciente, monto, referencia=None, observaciones=""):
    """
    Registra en caja un abono recibido por parte de la aseguradora.
    """
    if monto <= 0:
        return False, "El monto debe ser mayor que cero"
    if not _asegurar_tablas_caja():
        return False, "No fue posible preparar tablas de caja"

    conn = crear_conexion()
    if conn is None:
        return False, "No hay conexión con la base de datos"

    try:
        cursor = conn.cursor()

        paciente = _obtener_paciente(cursor, id_paciente)
        if not paciente:
            return False, "Paciente no encontrado"

        if not paciente[2]:
            return False, "El paciente no tiene seguro registrado"

        cursor.execute(
            """
            INSERT INTO Ingresos_Caja (
                id_paciente, id_cita, tipo_ingreso, monto, metodo_pago,
                referencia, fecha_registro, observaciones
            )
            VALUES (?, NULL, ?, ?, ?, ?, ?, ?)
            """,
            (
                id_paciente,
                TIPO_ABONO_SEGURO,
                monto,
                "Transferencia",
                referencia,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                observaciones,
            ),
        )

        conn.commit()
        return True, "Abono de seguro registrado"
    except Error as e:
        return False, f"Error al registrar abono: {e}"
    finally:
        conn.close()


def obtener_ingresos(fecha_inicio=None, fecha_fin=None, id_paciente=None):
    """
    Consulta ingresos registrados en caja.
    Permite filtrar por rango de fechas y paciente.
    """
    if not _asegurar_tablas_caja():
        return []

    conn = crear_conexion()
    if conn is None:
        return []

    try:
        cursor = conn.cursor()
        sql = """
            SELECT
                i.id_ingreso,
                i.fecha_registro,
                i.tipo_ingreso,
                i.monto,
                i.metodo_pago,
                i.referencia,
                p.id_paciente,
                p.nombre,
                c.id_cita,
                c.fecha_cita
            FROM Ingresos_Caja i
            INNER JOIN Pacientes p ON p.id_paciente = i.id_paciente
            LEFT JOIN Citas c ON c.id_cita = i.id_cita
            WHERE 1=1
        """

        parametros = []
        if fecha_inicio:
            sql += " AND date(i.fecha_registro) >= date(?)"
            parametros.append(fecha_inicio)
        if fecha_fin:
            sql += " AND date(i.fecha_registro) <= date(?)"
            parametros.append(fecha_fin)
        if id_paciente:
            sql += " AND i.id_paciente = ?"
            parametros.append(id_paciente)

        sql += " ORDER BY i.id_ingreso DESC"

        cursor.execute(sql, tuple(parametros))
        return cursor.fetchall()
    except Error:
        return []
    finally:
        conn.close()


def obtener_total_ingresos(fecha_inicio=None, fecha_fin=None):
    """
    Retorna el total de ingresos para el rango de fechas indicado.
    """
    if not _asegurar_tablas_caja():
        return 0.0

    conn = crear_conexion()
    if conn is None:
        return 0.0

    try:
        cursor = conn.cursor()
        sql = "SELECT COALESCE(SUM(monto), 0) FROM Ingresos_Caja WHERE 1=1"
        parametros = []

        if fecha_inicio:
            sql += " AND date(fecha_registro) >= date(?)"
            parametros.append(fecha_inicio)
        if fecha_fin:
            sql += " AND date(fecha_registro) <= date(?)"
            parametros.append(fecha_fin)

        cursor.execute(sql, tuple(parametros))
        return cursor.fetchone()[0]
    except Error:
        return 0.0
    finally:
        conn.close()


def obtener_total_ingresos_historico():
    """
    Retorna el total histórico acumulado de ingresos registrados en caja.
    """
    if not _asegurar_tablas_caja():
        return 0.0

    conn = crear_conexion()
    if conn is None:
        return 0.0

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COALESCE(SUM(monto), 0) FROM Ingresos_Caja")
        return float(cursor.fetchone()[0] or 0.0)
    except Error:
        return 0.0
    finally:
        conn.close()


def obtener_ingresos_estado_resultados():
    """
    Retorna los ingresos del mes actual para estado de resultados.
    """
    if not _asegurar_tablas_caja():
        return {
            "ingresos_tratamientos": 0.0,
            "ingresos_seguros": 0.0,
            "ingresos_totales": 0.0,
            "ingresos_historico": 0.0,
        }

    conn = crear_conexion()
    if conn is None:
        return {
            "ingresos_tratamientos": 0.0,
            "ingresos_seguros": 0.0,
            "ingresos_totales": 0.0,
            "ingresos_historico": 0.0,
        }

    try:
        cursor = conn.cursor()
        mes_actual = datetime.now().strftime("%m")
        anio_actual = datetime.now().strftime("%Y")

        cursor.execute(
            """
            SELECT
                COALESCE(SUM(CASE WHEN tipo_ingreso = ? THEN monto ELSE 0 END), 0),
                COALESCE(SUM(CASE WHEN tipo_ingreso = ? THEN monto ELSE 0 END), 0)
            FROM Ingresos_Caja
            WHERE strftime('%m', fecha_registro) = ?
              AND strftime('%Y', fecha_registro) = ?
            """,
            (TIPO_PAGO_TRATAMIENTO, TIPO_ABONO_SEGURO, mes_actual, anio_actual),
        )

        ingresos_tratamientos, ingresos_seguros = cursor.fetchone()
        ingresos_tratamientos = float(ingresos_tratamientos or 0.0)
        ingresos_seguros = float(ingresos_seguros or 0.0)
        ingresos_totales = ingresos_tratamientos + ingresos_seguros

        return {
            "ingresos_tratamientos": ingresos_tratamientos,
            "ingresos_seguros": ingresos_seguros,
            "ingresos_totales": ingresos_totales,
            "ingresos_historico": obtener_total_ingresos_historico(),
        }
    except Error:
        return {
            "ingresos_tratamientos": 0.0,
            "ingresos_seguros": 0.0,
            "ingresos_totales": 0.0,
            "ingresos_historico": 0.0,
        }
    finally:
        conn.close()
