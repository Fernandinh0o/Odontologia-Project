import tkinter as tk
from tkinter import messagebox, ttk

from gestores.gestor_pacientes import buscar_pacientes
from gestores.gestor_tratamientos import obtener_tratamientos
from gestores.gestor_presupuestos import (
    crear_presupuesto_cabecera,
    agregar_detalle_presupuesto,
    obtener_presupuestos_recientes,
    cobrar_presupuesto
)

FONDO_VENTANA = "#F5EAF1"
FONDO_PANEL = "#FDF7FA"
FONDO_TARJETA = "#E8F6FA"
FONDO_TARJETA_SECUNDARIA = "#F7E9F2"
ACENTO_PRIMARIO = "#8C78D9"
ACENTO_SECUNDARIO = "#5EC9D8"
ACENTO_ACCION = "#FF9FB4"
TEXTO_PRINCIPAL = "#493B61"
TEXTO_SECUNDARIO = "#766B8A"
BLANCO = "#FFFFFF"


def _configurar_estilos():
    style = ttk.Style()
    style.theme_use("clam")

    style.configure(
        "Ventas.Treeview",
        background=BLANCO,
        foreground=TEXTO_PRINCIPAL,
        fieldbackground=BLANCO,
        borderwidth=0,
        rowheight=28,
        font=("Arial", 10),
    )
    style.configure(
        "Ventas.Treeview.Heading",
        background=ACENTO_PRIMARIO,
        foreground=BLANCO,
        font=("Arial", 10, "bold"),
        relief="flat",
    )
    style.map(
        "Ventas.Treeview",
        background=[("selected", "#D9F4F8")],
        foreground=[("selected", TEXTO_PRINCIPAL)],
    )

    style.configure(
        "Ventas.TCombobox",
        fieldbackground=BLANCO,
        background=BLANCO,
        foreground=TEXTO_PRINCIPAL,
        arrowsize=14,
        bordercolor="#E0D7E8",
        relief="flat",
        padding=5,
    )


def _crear_tarjeta(parent, x, y, w, h, color):
    tarjeta = tk.Frame(parent, bg=color, highlightthickness=0)
    tarjeta.place(x=x, y=y, width=w, height=h)
    return tarjeta


def _titulo(parent, text, x, y):
    tk.Label(
        parent,
        text=text,
        bg=parent.cget("bg"),
        fg=TEXTO_PRINCIPAL,
        font=("Arial", 11, "bold"),
    ).place(x=x, y=y)


def _boton(parent, text, command, x, y, w=150, h=35, color=ACENTO_PRIMARIO):
    tk.Button(
        parent,
        text=text,
        bg=color,
        fg=BLANCO,
        activebackground="#7A66C9",
        activeforeground=BLANCO,
        bd=0,
        relief="flat",
        font=("Arial", 10, "bold"),
        cursor="hand2",
        command=command,
    ).place(x=x, y=y, width=w, height=h)


def _input(parent, x, y, w=200):
    entrada = tk.Entry(
        parent,
        font=("Arial", 10),
        bd=0,
        relief="flat",
        fg=TEXTO_PRINCIPAL,
        bg=BLANCO,
        insertbackground=TEXTO_PRINCIPAL,
    )
    entrada.place(x=x, y=y, width=w, height=30)
    return entrada


def _etiqueta(parent, text, x, y):
    tk.Label(
        parent,
        text=text,
        bg=parent.cget("bg"),
        fg=TEXTO_SECUNDARIO,
        font=("Arial", 9, "bold"),
    ).place(x=x, y=y)


def mostrar_modulo_ventas():
    ventana = tk.Toplevel()
    ventana.title("Gestión Clínica - Presupuestos")
    ventana.geometry("1100x650")
    ventana.configure(bg=FONDO_VENTANA)
    ventana.resizable(False, False)

    _configurar_estilos()

    panel = tk.Frame(ventana, bg=FONDO_PANEL)
    panel.place(x=20, y=20, width=1060, height=610)

    tk.Label(panel, text="Presupuesto Clínico", bg=FONDO_PANEL, fg=TEXTO_PRINCIPAL, font=("Arial", 20, "bold")).place(
        x=30, y=20)
    tk.Label(panel, text="Gestión de pacientes y tratamientos", bg=FONDO_PANEL, fg=TEXTO_SECUNDARIO,
             font=("Arial", 10)).place(x=32, y=55)


    card_paciente = _crear_tarjeta(panel, x=30, y=90, w=500, h=80, color=FONDO_TARJETA_SECUNDARIA)
    _titulo(card_paciente, "1. Seleccionar Paciente", 15, 10)

    combo_pacientes = ttk.Combobox(card_paciente, state="readonly", style="Ventas.TCombobox")
    combo_pacientes.place(x=15, y=35, width=280, height=30)

    card_trata = _crear_tarjeta(panel, x=30, y=185, w=500, h=180, color=FONDO_TARJETA)
    _titulo(card_trata, "2. Agregar Tratamiento", 15, 10)

    _etiqueta(card_trata, "Tratamiento", 15, 35)
    combo_tratamiento = ttk.Combobox(card_trata, state="readonly", style="Ventas.TCombobox")
    combo_tratamiento.place(x=15, y=55, width=260, height=30)

    _etiqueta(card_trata, "Pieza", 290, 35)
    entry_pieza = _input(card_trata, x=290, y=55, w=80)

    _etiqueta(card_trata, "Precio (Q)", 390, 35)
    entry_precio = _input(card_trata, x=390, y=55, w=90)

    _etiqueta(card_trata, "Notas adicionales", 15, 95)
    entry_notas = _input(card_trata, x=15, y=115, w=350)

    def _accion_agregar():
        agregar_item()

    tk.Button(card_trata, text="+ AGREGAR", bg=ACENTO_SECUNDARIO, fg=BLANCO, font=("Arial", 9, "bold"),
              bd=0, cursor="hand2", command=_accion_agregar).place(x=380, y=115, width=100, height=30)

    card_detalle = _crear_tarjeta(panel, x=30, y=380, w=500, h=210, color=BLANCO)
    _titulo(card_detalle, "Detalle del Presupuesto Actual", 0, 0)  # Título fuera o dentro según gusto

    cols = ("trata", "pieza", "precio")
    tree_detalle = ttk.Treeview(card_detalle, columns=cols, show="headings", style="Ventas.Treeview")
    tree_detalle.heading("trata", text="Tratamiento")
    tree_detalle.heading("pieza", text="Pieza")
    tree_detalle.heading("precio", text="Precio")

    tree_detalle.column("trata", width=240)
    tree_detalle.column("pieza", width=80, anchor="center")
    tree_detalle.column("precio", width=100, anchor="e")

    tree_detalle.place(x=0, y=30, width=480, height=170)

    scroll_det = ttk.Scrollbar(card_detalle, orient="vertical", command=tree_detalle.yview)
    scroll_det.place(x=480, y=30, height=170)
    tree_detalle.configure(yscrollcommand=scroll_det.set)

    card_hist = _crear_tarjeta(panel, x=550, y=90, w=480, h=500, color="#F0F4F8")  # Gris muy suave
    _titulo(card_hist, "Historial de Presupuestos", 15, 10)

    cols_hist = ("id", "fecha", "paciente", "total")
    tree_hist = ttk.Treeview(card_hist, columns=cols_hist, show="headings", style="Ventas.Treeview")

    tree_hist.heading("id", text="ID")
    tree_hist.heading("fecha", text="Fecha")
    tree_hist.heading("paciente", text="Paciente")
    tree_hist.heading("total", text="Total")

    tree_hist.column("id", width=40, anchor="center")
    tree_hist.column("fecha", width=110)
    tree_hist.column("paciente", width=160)
    tree_hist.column("total", width=90, anchor="e")

    tree_hist.place(x=15, y=40, width=450, height=400)

    btn_cobrar = tk.Button(card_hist, text="💰 COBRAR SELECCIONADO", bg="#59C9A5", fg=BLANCO,
                           font=("Arial", 11, "bold"), bd=0, cursor="hand2", command=lambda: realizar_cobro())
    btn_cobrar.place(x=15, y=450, width=450, height=40)

    _boton(panel, "GUARDAR NUEVO", command=lambda: guardar_presupuesto(), x=300, y=550, w=180, color=ACENTO_PRIMARIO)

    tk.Button(panel, text="✕", bg=ACENTO_PRIMARIO, fg=BLANCO, bd=0, font=("Arial", 12, "bold"),
              cursor="hand2", command=ventana.destroy).place(x=1010, y=20, width=30, height=30)

    mapa_pacientes = {}
    mapa_tratamientos = {}
    items_actuales = []

    def cargar_datos():
        pacientes = buscar_pacientes()
        vals_pac = []
        mapa_pacientes.clear()
        for p in pacientes:
            texto = f"{p[1]} (NIT:{p[3]})"
            mapa_pacientes[texto] = p
            vals_pac.append(texto)
        combo_pacientes['values'] = vals_pac


        tratas = obtener_tratamientos()
        vals_trata = []
        mapa_tratamientos.clear()
        for t in tratas:
            mapa_tratamientos[t[1]] = t
            vals_trata.append(t[1])
        combo_tratamiento['values'] = vals_trata

        hist = obtener_presupuestos_recientes()
        for item in tree_hist.get_children():
            tree_hist.delete(item)
        for h in hist:
            tree_hist.insert("", "end", values=(h[0], h[1], h[2], f"Q{h[3]:.2f}"))

    def al_seleccionar_paciente(event):
        texto = combo_pacientes.get()
        if texto in mapa_pacientes:
            pac = mapa_pacientes[texto]

    def al_seleccionar_tratamiento(event):
        nombre = combo_tratamiento.get()
        if nombre in mapa_tratamientos:
            precio_base = mapa_tratamientos[nombre][2]
            entry_precio.delete(0, tk.END)
            entry_precio.insert(0, str(precio_base))

    def agregar_item():
        trata_nombre = combo_tratamiento.get()
        pieza = entry_pieza.get()
        try:
            precio = float(entry_precio.get())
        except:
            messagebox.showerror("Error", "Precio inválido")
            return
        notas = entry_notas.get()

        if not trata_nombre:
            messagebox.showwarning("Faltan datos", "Seleccione un tratamiento")
            return

        id_trata = mapa_tratamientos[trata_nombre][0]

        item = {
            "id_trata": id_trata,
            "nombre": trata_nombre,
            "pieza": pieza,
            "precio": precio,
            "notas": notas
        }
        items_actuales.append(item)
        tree_detalle.insert("", "end", values=(trata_nombre, pieza, f"Q{precio:.2f}"))

        entry_pieza.delete(0, tk.END)
        entry_notas.delete(0, tk.END)

    def guardar_presupuesto():
        pac_texto = combo_pacientes.get()
        if pac_texto not in mapa_pacientes:
            messagebox.showerror("Error", "Seleccione un paciente válido")
            return

        if not items_actuales:
            messagebox.showerror("Error", "La lista de tratamientos está vacía")
            return

        id_paciente = mapa_pacientes[pac_texto][0]

        try:
            id_pres = crear_presupuesto_cabecera(id_paciente, "UsuarioActual")

            for it in items_actuales:
                agregar_detalle_presupuesto(id_pres, it['id_trata'], it['pieza'], it['precio'], it['notas'])

            messagebox.showinfo("Éxito", f"Presupuesto #{id_pres} creado correctamente.")

            items_actuales.clear()
            for x in tree_detalle.get_children(): tree_detalle.delete(x)
            combo_pacientes.set("")
            combo_tratamiento.set("")
            lbl_seguro.config(text="---", bg=BLANCO, fg=TEXTO_SECUNDARIO)
            entry_precio.delete(0, tk.END)

            cargar_datos()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def realizar_cobro():
        seleccionado = tree_hist.focus()
        if not seleccionado:
            messagebox.showwarning("Atención", "Seleccione un presupuesto del historial (derecha) para cobrar.")
            return

        datos = tree_hist.item(seleccionado, 'values')
        id_presupuesto = datos[0]

        resp = messagebox.askyesno("Confirmar Cobro", f"¿Desea marcar como PAGADO el Presupuesto #{id_presupuesto}?")
        if resp:
            exito, mensaje = cobrar_presupuesto(id_presupuesto)
            if exito:
                messagebox.showinfo("Pago Registrado", mensaje)
                cargar_datos()
            else:
                messagebox.showerror("Error", mensaje)

    combo_pacientes.bind("<<ComboboxSelected>>", al_seleccionar_paciente)
    combo_tratamiento.bind("<<ComboboxSelected>>", al_seleccionar_tratamiento)

    cargar_datos()