import tkinter as tk
from tkinter import ttk

from database.conexion import crear_conexion
from gestores.gestor_rrhh import obtener_empleados

MORADO = "#4B2A6A"
FONDO = "#FFFFFF"
TEXTO = "#3D2A57"


class RRHHHistorialVista(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=FONDO)
        self.id_empleado = None
        self.empleados_map = {}
        self._crear_interfaz()
        self._cargar_empleados()

    def _crear_interfaz(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        tk.Label(
            self,
            text="Historial de Pagos",
            bg=FONDO,
            fg=MORADO,
            font=("Arial", 20, "bold"),
        ).grid(row=0, column=0, sticky="w", padx=18, pady=(18, 10))

        filtro = tk.Frame(self, bg=FONDO)
        filtro.grid(row=1, column=0, sticky="ew", padx=18, pady=(0, 10))
        filtro.grid_columnconfigure(1, weight=1)

        tk.Label(
            filtro,
            text="Empleado",
            bg=FONDO,
            fg=MORADO,
            font=("Arial", 11, "bold"),
        ).grid(row=0, column=0, sticky="w", padx=(0, 10))

        self.combo_empleado = ttk.Combobox(filtro, state="readonly", width=55)
        self.combo_empleado.grid(row=0, column=1, sticky="ew")
        self.combo_empleado.bind("<<ComboboxSelected>>", self._on_empleado_selected)

        tabla_frame = tk.Frame(self, bg=FONDO)
        tabla_frame.grid(row=2, column=0, sticky="nsew", padx=18, pady=(0, 18))
        tabla_frame.grid_columnconfigure(0, weight=1)
        tabla_frame.grid_rowconfigure(0, weight=1)

        columnas = ("id", "fecha", "concepto", "base", "bonos", "deducciones", "total")
        self.tabla_historial = ttk.Treeview(tabla_frame, columns=columnas, show="headings")

        encabezados = {
            "id": "ID",
            "fecha": "Fecha",
            "concepto": "Concepto",
            "base": "Salario Base",
            "bonos": "Bonos",
            "deducciones": "Deducciones",
            "total": "Total Pagado",
        }
        anchos = {
            "id": 70,
            "fecha": 120,
            "concepto": 260,
            "base": 130,
            "bonos": 110,
            "deducciones": 120,
            "total": 130,
        }

        for col in columnas:
            self.tabla_historial.heading(col, text=encabezados[col])
            anchor = "w" if col == "concepto" else "center"
            if col in {"base", "bonos", "deducciones", "total"}:
                anchor = "e"
            self.tabla_historial.column(col, width=anchos[col], anchor=anchor, stretch=True)

        scroll_y = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.tabla_historial.yview)
        scroll_x = ttk.Scrollbar(tabla_frame, orient="horizontal", command=self.tabla_historial.xview)
        self.tabla_historial.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        self.tabla_historial.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")

    def _cargar_empleados(self):
        empleados = obtener_empleados()
        self.empleados_map = {f"{emp[0]} - {emp[1]} ({emp[2]})": emp[0] for emp in empleados}
        self.combo_empleado["values"] = list(self.empleados_map.keys())

        if self.empleados_map:
            primera_opcion = next(iter(self.empleados_map))
            self.combo_empleado.set(primera_opcion)
            self.id_empleado = self.empleados_map[primera_opcion]
            self._cargar_historial()

    def _on_empleado_selected(self, _event=None):
        seleccion = self.combo_empleado.get()
        self.id_empleado = self.empleados_map.get(seleccion)
        self._cargar_historial()

    def _obtener_historial_detallado(self, id_usuario):
        conn = crear_conexion()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id_pago, fecha, concepto, monto_base, bonificaciones, deducciones, total_pagado
                FROM Nominas
                WHERE id_usuario = ?
                ORDER BY id_pago DESC
                """,
                (id_usuario,),
            )
            return cursor.fetchall()
        finally:
            conn.close()

    def _cargar_historial(self):
        for item in self.tabla_historial.get_children():
            self.tabla_historial.delete(item)

        if not self.id_empleado:
            return

        for pago in self._obtener_historial_detallado(self.id_empleado):
            self.tabla_historial.insert(
                "",
                "end",
                values=(
                    pago[0],
                    pago[1],
                    pago[2],
                    f"Q{float(pago[3]):.2f}",
                    f"Q{float(pago[4]):.2f}",
                    f"Q{float(pago[5]):.2f}",
                    f"Q{float(pago[6]):.2f}",
                ),
            )
