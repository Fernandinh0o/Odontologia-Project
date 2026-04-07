import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

from gestores.gestor_ingresos import (
    registrar_pago_tratamiento,
    registrar_abono_seguro,
    obtener_ingresos,
    obtener_total_ingresos,
)

# Paleta simple para mantener consistencia visual con el resto del proyecto.
MORADO = "#4B2A6A"
FONDO = "#FFFFFF"
TEXTO = "#3D2A57"
GRIS = "#6D6D6D"


class IngresosOdontologoVista(tk.Frame):
    """
    Vista de Odontología para registrar y consultar ingresos de caja.

    Esta clase solo se encarga de interfaz (captura/visualización).
    Toda la lógica de negocio y persistencia vive en `gestor_ingresos.py`.
    """

    def __init__(self, master):
        super().__init__(master, bg=FONDO)
        self._crear_interfaz()
        self._cargar_ingresos_hoy()

    def _crear_interfaz(self):
        """Construye la pantalla completa con formulario y tabla de consulta."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        tk.Label(
            self,
            text="Caja de Ingresos - Odontología",
            bg=FONDO,
            fg=MORADO,
            font=("Arial", 22, "bold"),
        ).grid(row=0, column=0, sticky="w", padx=25, pady=(20, 5))

        tk.Label(
            self,
            text="Registro de pagos de tratamientos y abonos de seguros",
            bg=FONDO,
            fg=GRIS,
            font=("Arial", 11),
        ).grid(row=1, column=0, sticky="w", padx=25, pady=(0, 15))

        self._crear_formulario()
        self._crear_consulta()

    def _crear_formulario(self):
        """Formulario simple para captura de ingresos."""
        card = tk.Frame(self, bg=FONDO, highlightbackground="#D9D9D9", highlightthickness=1)
        card.grid(row=2, column=0, sticky="ew", padx=25, pady=(0, 12))
        card.grid_columnconfigure(0, weight=1)

        tk.Label(
            card,
            text="Registrar ingreso",
            bg=FONDO,
            fg=TEXTO,
            font=("Arial", 14, "bold"),
        ).grid(row=0, column=0, columnspan=4, sticky="w", padx=15, pady=(12, 8))

        # Tipo de ingreso: determina qué función lógica se dispara.
        self.tipo_ingreso = tk.StringVar(value="tratamiento")
        tk.Radiobutton(
            card,
            text="Pago de tratamiento",
            variable=self.tipo_ingreso,
            value="tratamiento",
            bg=FONDO,
            fg=TEXTO,
            selectcolor=FONDO,
            activebackground=FONDO,
            font=("Arial", 10),
        ).grid(row=1, column=0, sticky="w", padx=15, pady=(0, 6))

        tk.Radiobutton(
            card,
            text="Abono de seguro",
            variable=self.tipo_ingreso,
            value="seguro",
            bg=FONDO,
            fg=TEXTO,
            selectcolor=FONDO,
            activebackground=FONDO,
            font=("Arial", 10),
        ).grid(row=1, column=1, sticky="w", padx=15, pady=(0, 6))

        self.entry_paciente = self._crear_campo(card, "ID Paciente", 2, 0)
        self.entry_cita = self._crear_campo(card, "ID Cita", 2, 1)
        self.entry_monto = self._crear_campo(card, "Monto", 2, 2)

        tk.Label(card, text="Método de pago", bg=FONDO, fg=TEXTO, font=("Arial", 10, "bold")).grid(
            row=2, column=3, sticky="w", padx=15, pady=(5, 0)
        )
        self.combo_metodo = ttk.Combobox(
            card,
            state="readonly",
            values=["Efectivo", "Tarjeta", "Transferencia"],
        )
        self.combo_metodo.grid(row=3, column=3, sticky="ew", padx=15, pady=(4, 12))
        self.combo_metodo.set("Efectivo")

        botones = tk.Frame(card, bg=FONDO)
        botones.grid(row=4, column=0, columnspan=4, sticky="w", padx=15, pady=(0, 12))

        # Botón principal: ejecuta la función de registro correspondiente.
        tk.Button(
            botones,
            text="Registrar ingreso",
            command=self._registrar_ingreso,
            bg=MORADO,
            fg=FONDO,
            bd=0,
            font=("Arial", 11, "bold"),
            cursor="hand2",
            padx=20,
            pady=6,
        ).grid(row=0, column=0, padx=(0, 10))

        tk.Button(
            botones,
            text="Limpiar",
            command=self._limpiar_formulario,
            bg="#ECECEC",
            fg=TEXTO,
            bd=0,
            font=("Arial", 11),
            cursor="hand2",
            padx=20,
            pady=6,
        ).grid(row=0, column=1)

    def _crear_consulta(self):
        """Sección para consulta diaria/rango y tabla de ingresos recientes."""
        card = tk.Frame(self, bg=FONDO, highlightbackground="#D9D9D9", highlightthickness=1)
        card.grid(row=3, column=0, sticky="nsew", padx=25, pady=(0, 20))
        card.grid_columnconfigure(0, weight=1)
        card.grid_rowconfigure(2, weight=1)

        tk.Label(
            card,
            text="Consulta de ingresos",
            bg=FONDO,
            fg=TEXTO,
            font=("Arial", 14, "bold"),
        ).grid(row=0, column=0, sticky="w", padx=15, pady=(12, 6))

        filtros = tk.Frame(card, bg=FONDO)
        filtros.grid(row=1, column=0, sticky="ew", padx=15, pady=(0, 8))

        hoy = datetime.now().strftime("%Y-%m-%d")
        tk.Label(filtros, text="Fecha inicio (YYYY-MM-DD)", bg=FONDO, fg=TEXTO).grid(row=0, column=0, sticky="w")
        self.entry_inicio = tk.Entry(filtros)
        self.entry_inicio.grid(row=1, column=0, padx=(0, 10), pady=(2, 0))
        self.entry_inicio.insert(0, hoy)

        tk.Label(filtros, text="Fecha fin (YYYY-MM-DD)", bg=FONDO, fg=TEXTO).grid(row=0, column=1, sticky="w")
        self.entry_fin = tk.Entry(filtros)
        self.entry_fin.grid(row=1, column=1, padx=(0, 10), pady=(2, 0))
        self.entry_fin.insert(0, hoy)

        tk.Button(
            filtros,
            text="Consultar",
            command=self._consultar_ingresos,
            bg=MORADO,
            fg=FONDO,
            bd=0,
            font=("Arial", 10, "bold"),
            cursor="hand2",
            padx=16,
            pady=4,
        ).grid(row=1, column=2)

        self.label_total = tk.Label(
            filtros,
            text="Total: Q0.00",
            bg=FONDO,
            fg=MORADO,
            font=("Arial", 11, "bold"),
        )
        self.label_total.grid(row=1, column=3, padx=(15, 0), sticky="w")

        columnas = ("id", "fecha", "tipo", "paciente", "cita", "metodo", "monto")
        self.tree_ingresos = ttk.Treeview(card, columns=columnas, show="headings")

        self.tree_ingresos.heading("id", text="ID")
        self.tree_ingresos.heading("fecha", text="Fecha")
        self.tree_ingresos.heading("tipo", text="Tipo")
        self.tree_ingresos.heading("paciente", text="Paciente")
        self.tree_ingresos.heading("cita", text="Cita")
        self.tree_ingresos.heading("metodo", text="Método")
        self.tree_ingresos.heading("monto", text="Monto")

        self.tree_ingresos.column("id", width=50, anchor="center")
        self.tree_ingresos.column("fecha", width=150)
        self.tree_ingresos.column("tipo", width=130)
        self.tree_ingresos.column("paciente", width=200)
        self.tree_ingresos.column("cita", width=80, anchor="center")
        self.tree_ingresos.column("metodo", width=100)
        self.tree_ingresos.column("monto", width=100, anchor="e")

        self.tree_ingresos.grid(row=2, column=0, sticky="nsew", padx=15, pady=(0, 12))

        scroll = ttk.Scrollbar(card, orient="vertical", command=self.tree_ingresos.yview)
        scroll.place(relx=0.985, rely=0.18, relheight=0.75)
        self.tree_ingresos.configure(yscrollcommand=scroll.set)

    def _crear_campo(self, parent, etiqueta, fila, columna):
        """Helper de UI para evitar repetir código de etiquetas/entries."""
        tk.Label(parent, text=etiqueta, bg=FONDO, fg=TEXTO, font=("Arial", 10, "bold")).grid(
            row=fila, column=columna, sticky="w", padx=15, pady=(5, 0)
        )
        entry = tk.Entry(parent)
        entry.grid(row=fila + 1, column=columna, sticky="ew", padx=15, pady=(4, 12))
        return entry

    def _registrar_ingreso(self):
        """Toma datos del formulario y llama al módulo lógico de ingresos."""
        try:
            id_paciente = int(self.entry_paciente.get().strip())
            monto = float(self.entry_monto.get().strip())
        except ValueError:
            messagebox.showerror("Datos inválidos", "ID Paciente y Monto deben ser numéricos.")
            return

        metodo = self.combo_metodo.get().strip() or "Efectivo"
        tipo = self.tipo_ingreso.get()

        if tipo == "tratamiento":
            try:
                id_cita = int(self.entry_cita.get().strip())
            except ValueError:
                messagebox.showerror("Datos inválidos", "Para pago de tratamiento debe ingresar ID Cita.")
                return

            ok, mensaje = registrar_pago_tratamiento(
                id_paciente=id_paciente,
                id_cita=id_cita,
                monto=monto,
                metodo_pago=metodo,
            )
        else:
            # Para abonos de seguro, el campo cita no es obligatorio.
            ok, mensaje = registrar_abono_seguro(
                id_paciente=id_paciente,
                monto=monto,
                referencia=f"Abono UI - {metodo}",
            )

        if ok:
            messagebox.showinfo("Caja", mensaje)
            self._limpiar_formulario()
            self._consultar_ingresos()
        else:
            messagebox.showerror("Caja", mensaje)

    def _consultar_ingresos(self):
        """Carga tabla y total con filtros de fecha usando el gestor lógico."""
        fecha_inicio = self.entry_inicio.get().strip() or None
        fecha_fin = self.entry_fin.get().strip() or None

        ingresos = obtener_ingresos(fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)
        total = obtener_total_ingresos(fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)

        for item in self.tree_ingresos.get_children():
            self.tree_ingresos.delete(item)

        for ing in ingresos:
            self.tree_ingresos.insert(
                "",
                "end",
                values=(
                    ing[0],
                    ing[1],
                    ing[2],
                    f"{ing[6]} - {ing[7]}",
                    ing[8] if ing[8] is not None else "-",
                    ing[4] if ing[4] else "-",
                    f"Q{ing[3]:.2f}",
                ),
            )

        self.label_total.config(text=f"Total: Q{float(total):.2f}")

    def _cargar_ingresos_hoy(self):
        """Consulta inicial al abrir la vista (flujo rápido para uso diario)."""
        self._consultar_ingresos()

    def _limpiar_formulario(self):
        """Limpia campos de captura para registrar un nuevo ingreso."""
        self.entry_paciente.delete(0, tk.END)
        self.entry_cita.delete(0, tk.END)
        self.entry_monto.delete(0, tk.END)
        self.combo_metodo.set("Efectivo")
        self.tipo_ingreso.set("tratamiento")
