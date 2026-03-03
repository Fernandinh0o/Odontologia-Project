import tkinter as tk
from tkinter import messagebox, ttk

from gestores.gestor_rrhh import (
    calcular_nomina_teorica,
    obtener_empleados,
    obtener_historial_pagos,
    registrar_pago_nomina,
)

MORADO = "#4B2A6A"
FONDO = "#FFFFFF"
TEXTO = "#3D2A57"


class RRHHVista(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=FONDO)
        self.id_empleado = None
        self.empleados_map = {}
        self._crear_interfaz()
        self._cargar_empleados()

    def _crear_interfaz(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(7, weight=1)

        tk.Label(
            self,
            text="Gestión de Nómina",
            bg=FONDO,
            fg=MORADO,
            font=("Arial", 20, "bold"),
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=18, pady=(18, 12))

        tk.Label(self, text="Empleado", bg=FONDO, fg=MORADO, font=("Arial", 11, "bold")).grid(
            row=1, column=0, sticky="w", padx=18, pady=6
        )
        self.combo_empleado = ttk.Combobox(self, state="readonly", width=48)
        self.combo_empleado.grid(row=1, column=1, sticky="ew", padx=18, pady=6)
        self.combo_empleado.bind("<<ComboboxSelected>>", self._on_empleado_selected)

        self.entry_base = self._crear_campo("Salario Base", 2)
        self.entry_comisiones = self._crear_campo("Comisiones", 3, "0")
        self.entry_descuentos = self._crear_campo("Otros Descuentos", 4, "0")
        self.entry_concepto = self._crear_campo("Concepto", 5, "Pago mensual")

        botones = tk.Frame(self, bg=FONDO)
        botones.grid(row=6, column=0, columnspan=2, sticky="w", padx=18, pady=8)

        tk.Button(
            botones,
            text="Calcular",
            command=self._calcular_nomina,
            bg=MORADO,
            fg=FONDO,
            activebackground=MORADO,
            activeforeground=FONDO,
            bd=0,
            font=("Arial", 11, "bold"),
            cursor="hand2",
        ).grid(row=0, column=0, padx=(0, 10), ipadx=16, ipady=5)

        tk.Button(
            botones,
            text="Registrar Pago",
            command=self._registrar_pago,
            bg=MORADO,
            fg=FONDO,
            activebackground=MORADO,
            activeforeground=FONDO,
            bd=0,
            font=("Arial", 11, "bold"),
            cursor="hand2",
        ).grid(row=0, column=1, ipadx=16, ipady=5)

        self.label_resultado = tk.Label(
            self,
            text="",
            bg=FONDO,
            fg=TEXTO,
            font=("Arial", 10),
            justify="left",
            anchor="w",
        )
        self.label_resultado.grid(row=7, column=0, columnspan=2, sticky="new", padx=18, pady=(0, 8))

        historial_frame = tk.Frame(self, bg=FONDO)
        historial_frame.grid(row=8, column=0, columnspan=2, sticky="nsew", padx=18, pady=(0, 18))
        historial_frame.grid_columnconfigure(0, weight=1)
        historial_frame.grid_rowconfigure(1, weight=1)

        tk.Label(
            historial_frame,
            text="Historial de Pagos",
            bg=FONDO,
            fg=MORADO,
            font=("Arial", 13, "bold"),
        ).grid(row=0, column=0, sticky="w", pady=(0, 8))

        columnas = ("id", "fecha", "concepto", "total")
        self.tabla_historial = ttk.Treeview(historial_frame, columns=columnas, show="headings", height=7)
        self.tabla_historial.heading("id", text="ID")
        self.tabla_historial.heading("fecha", text="Fecha")
        self.tabla_historial.heading("concepto", text="Concepto")
        self.tabla_historial.heading("total", text="Total Pagado")

        self.tabla_historial.column("id", width=60, anchor="center")
        self.tabla_historial.column("fecha", width=110, anchor="center")
        self.tabla_historial.column("concepto", width=260, anchor="w")
        self.tabla_historial.column("total", width=120, anchor="e")

        scrollbar = ttk.Scrollbar(historial_frame, orient="vertical", command=self.tabla_historial.yview)
        self.tabla_historial.configure(yscrollcommand=scrollbar.set)
        self.tabla_historial.grid(row=1, column=0, sticky="nsew")
        scrollbar.grid(row=1, column=1, sticky="ns")

    def _crear_campo(self, etiqueta, fila, valor_inicial=""):
        tk.Label(self, text=etiqueta, bg=FONDO, fg=MORADO, font=("Arial", 11, "bold")).grid(
            row=fila, column=0, sticky="w", padx=18, pady=6
        )
        entry = tk.Entry(self, font=("Arial", 11), fg=TEXTO, relief="solid", bd=1)
        entry.grid(row=fila, column=1, sticky="ew", padx=18, pady=6)
        if valor_inicial:
            entry.insert(0, valor_inicial)
        return entry

    def _cargar_empleados(self):
        empleados = obtener_empleados()
        self.empleados_map = {
            f"{emp[0]} - {emp[1]} ({emp[2]})": emp[0]
            for emp in empleados
        }
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

    def _leer_valores(self):
        if not self.id_empleado:
            raise ValueError("Selecciona un empleado.")

        salario_base = float(self.entry_base.get().strip())
        comisiones = float(self.entry_comisiones.get().strip() or 0)
        otros_descuentos = float(self.entry_descuentos.get().strip() or 0)
        concepto = self.entry_concepto.get().strip()

        if salario_base < 0 or comisiones < 0 or otros_descuentos < 0:
            raise ValueError("No se permiten valores negativos.")
        if not concepto:
            raise ValueError("Ingresa un concepto de pago.")

        return salario_base, comisiones, otros_descuentos, concepto

    def _calcular_nomina(self):
        try:
            salario_base, comisiones, otros_descuentos, _ = self._leer_valores()
            calculo = calcular_nomina_teorica(salario_base, comisiones)
            total_final = calculo["total_liquido"] - otros_descuentos

            self.label_resultado.config(
                text=(
                    f"Bono Ley: Q{calculo['bono_ley']:.2f} | "
                    f"IGSS: Q{calculo['igss_laboral']:.2f} | "
                    f"Costo Patronal: Q{calculo['costo_patronal']:.2f}\n"
                    f"Total líquido estimado (con descuentos): Q{total_final:.2f}"
                )
            )
        except ValueError as exc:
            messagebox.showerror("Datos inválidos", str(exc))

    def _registrar_pago(self):
        try:
            salario_base, comisiones, otros_descuentos, concepto = self._leer_valores()
        except ValueError as exc:
            messagebox.showerror("Datos inválidos", str(exc))
            return

        ok, mensaje = registrar_pago_nomina(
            self.id_empleado,
            concepto,
            salario_base,
            comisiones,
            otros_descuentos,
        )

        if ok:
            messagebox.showinfo("Nómina", mensaje)
            self._cargar_historial()
            self._calcular_nomina()
        else:
            messagebox.showerror("Error", mensaje)

    def _cargar_historial(self):
        for item in self.tabla_historial.get_children():
            self.tabla_historial.delete(item)

        if not self.id_empleado:
            return

        for pago in obtener_historial_pagos(self.id_empleado):
            self.tabla_historial.insert(
                "",
                "end",
                values=(pago[0], pago[1], pago[2], f"Q{float(pago[3]):.2f}"),
            )
