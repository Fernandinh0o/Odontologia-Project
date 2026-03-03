import tkinter as tk
from tkinter import messagebox, ttk

from gestores.gestor_rrhh import calcular_nomina_teorica, obtener_empleados, registrar_pago_nomina

MORADO = "#4B2A6A"
FONDO = "#FFFFFF"
TEXTO = "#3D2A57"

IGSS_PATRONAL = 0.1267


class RRHHVista(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=FONDO)
        self.id_empleado = None
        self.empleados_map = {}
        self._crear_interfaz()
        self._cargar_empleados()

    def _crear_interfaz(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(7, weight=1)

        tk.Label(
            self,
            text="Gestión de Nómina",
            bg=FONDO,
            fg=MORADO,
            font=("Arial", 24, "bold"),
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=30, pady=(30, 20))

        tk.Label(
            self,
            text="Empleado",
            bg=FONDO,
            fg=MORADO,
            font=("Arial", 13, "bold"),
        ).grid(row=1, column=0, sticky="w", padx=30, pady=10)

        self.combo_empleado = ttk.Combobox(self, state="readonly")
        self.combo_empleado.grid(row=1, column=1, sticky="ew", padx=30, pady=10)
        self.combo_empleado.bind("<<ComboboxSelected>>", self._on_empleado_selected)

        self.entry_base = self._crear_campo("Salario Base", 2)
        self.entry_comisiones = self._crear_campo("Comisiones", 3, "0")
        self.entry_descuentos = self._crear_campo("Otros Descuentos", 4, "0")
        self.entry_concepto = self._crear_campo("Concepto", 5, "Pago mensual")

        botones = tk.Frame(self, bg=FONDO)
        botones.grid(row=6, column=0, columnspan=2, sticky="w", padx=30, pady=20)

        tk.Button(
            botones,
            text="Calcular",
            command=self._calcular_nomina,
            bg=MORADO,
            fg=FONDO,
            bd=0,
            font=("Arial", 13, "bold"),
            cursor="hand2",
            padx=25,
            pady=8,
        ).grid(row=0, column=0, padx=(0, 15))

        tk.Button(
            botones,
            text="Registrar Pago",
            command=self._registrar_pago,
            bg=MORADO,
            fg=FONDO,
            bd=0,
            font=("Arial", 13, "bold"),
            cursor="hand2",
            padx=25,
            pady=8,
        ).grid(row=0, column=1)

        self.label_resultado = tk.Label(
            self,
            text="",
            bg=FONDO,
            fg=TEXTO,
            font=("Arial", 13),
            justify="left",
            anchor="nw",
        )
        self.label_resultado.grid(
            row=7,
            column=0,
            columnspan=2,
            sticky="nsew",
            padx=30,
            pady=(20, 30),
        )

    def _crear_campo(self, etiqueta, fila, valor_inicial=""):
        tk.Label(
            self,
            text=etiqueta,
            bg=FONDO,
            fg=MORADO,
            font=("Arial", 13, "bold"),
        ).grid(row=fila, column=0, sticky="w", padx=30, pady=10)

        entry = tk.Entry(self, font=("Arial", 13), fg=TEXTO, relief="solid", bd=1)
        entry.grid(row=fila, column=1, sticky="ew", padx=30, pady=10)

        if valor_inicial:
            entry.insert(0, valor_inicial)

        return entry

    def _cargar_empleados(self):
        empleados = obtener_empleados()
        self.empleados_map = {f"{emp[0]} - {emp[1]} ({emp[2]})": emp[0] for emp in empleados}
        self.combo_empleado["values"] = list(self.empleados_map.keys())

        if self.empleados_map:
            primera_opcion = next(iter(self.empleados_map))
            self.combo_empleado.set(primera_opcion)
            self.id_empleado = self.empleados_map[primera_opcion]

    def _on_empleado_selected(self, _event=None):
        seleccion = self.combo_empleado.get()
        self.id_empleado = self.empleados_map.get(seleccion)

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

            total_devengado = salario_base + comisiones
            igss_laboral = calculo["igss_laboral"]
            bono_ley = calculo["bono_ley"]
            igss_patronal = total_devengado * IGSS_PATRONAL
            total_descuentos = igss_laboral + otros_descuentos
            total_liquido = calculo["total_liquido"] - otros_descuentos
            costo_empresa = total_devengado + bono_ley + igss_patronal

            self.label_resultado.config(
                text=(
                    f"Total Devengado: Q{total_devengado:.2f}\n"
                    f"IGSS Laboral: Q{igss_laboral:.2f}\n"
                    f"IGSS Patronal: Q{igss_patronal:.2f}\n"
                    f"Bono Ley: Q{bono_ley:.2f}\n"
                    f"Total Descuentos: Q{total_descuentos:.2f}\n"
                    f"Total Líquido: Q{total_liquido:.2f}\n"
                    f"Costo Total Empresa: Q{costo_empresa:.2f}"
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
            self._calcular_nomina()
        else:
            messagebox.showerror("Error", mensaje)