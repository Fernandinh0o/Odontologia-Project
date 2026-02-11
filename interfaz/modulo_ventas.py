import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

# Importamos los gestores que SI tienes y el nuevo
from gestores.gestor_pacientes import buscar_pacientes
from gestores.gestor_tratamientos import obtener_tratamientos
from gestores.gestor_presupuestos import crear_presupuesto_cabecera, agregar_detalle_presupuesto, \
    obtener_presupuestos_recientes, cobrar_presupuesto

ROSA_SUAVE = "#E8D4E0"
TEXTO_CLARO = "#FFFFFF"
MORADO = "#4B2A6A"
TEXTO_GRIS = "#5B5B5B"


def _boton(panel, text, command, x, y, w=160, h=35):
    tk.Button(
        panel, text=text, bg=MORADO, fg=TEXTO_CLARO, bd=0,
        font=("Arial", 10, "bold"), command=command,
    ).place(x=x, y=y, width=w, height=h)


def mostrar_modulo_ventas():
    ventana = tk.Toplevel()
    ventana.title("Gestión de Tratamientos y Ventas")
    ventana.geometry("1100x600")
    ventana.configure(bg=ROSA_SUAVE)
    ventana.resizable(False, False)

    tk.Label(ventana, text="Presupuesto Clínico", bg=ROSA_SUAVE, fg=MORADO,
             font=("Arial", 16, "bold")).place(x=30, y=20)

    frame_paciente = tk.LabelFrame(ventana, text="Paciente", bg=ROSA_SUAVE, fg=TEXTO_GRIS)
    frame_paciente.place(x=30, y=60, width=500, height=80)

    tk.Label(frame_paciente, text="Buscar:", bg=ROSA_SUAVE).place(x=10, y=20)
    combo_pacientes = ttk.Combobox(frame_paciente, width=30)
    combo_pacientes.place(x=70, y=20)


    frame_trata = tk.Frame(ventana, bg=ROSA_SUAVE)
    frame_trata.place(x=30, y=150, width=500, height=180)

    tk.Label(frame_trata, text="Tratamiento", bg=ROSA_SUAVE, font=("Arial", 10, "bold")).grid(row=0, column=0,
                                                                                              sticky="w", pady=5)
    tk.Label(frame_trata, text="Pieza Dental", bg=ROSA_SUAVE, font=("Arial", 10, "bold")).grid(row=1, column=0,
                                                                                               sticky="w", pady=5)
    tk.Label(frame_trata, text="Precio (Q)", bg=ROSA_SUAVE, font=("Arial", 10, "bold")).grid(row=2, column=0,
                                                                                             sticky="w", pady=5)
    tk.Label(frame_trata, text="Notas", bg=ROSA_SUAVE, font=("Arial", 10, "bold")).grid(row=3, column=0, sticky="w",
                                                                                        pady=5)

    combo_tratamiento = ttk.Combobox(frame_trata, state="readonly", width=35)
    combo_tratamiento.grid(row=0, column=1, padx=10)

    entry_pieza = tk.Entry(frame_trata, font=("Arial", 11), width=15)
    entry_pieza.grid(row=1, column=1, padx=10, sticky="w")

    entry_precio = tk.Entry(frame_trata, font=("Arial", 11), width=15)
    entry_precio.grid(row=2, column=1, padx=10, sticky="w")

    entry_notas = tk.Entry(frame_trata, font=("Arial", 11), width=37)
    entry_notas.grid(row=3, column=1, padx=10, sticky="w")

    frame_detalle = tk.Frame(ventana, bg=ROSA_SUAVE)
    frame_detalle.place(x=30, y=340, width=500, height=200)

    cols = ("trata", "pieza", "precio")
    tree_detalle = ttk.Treeview(frame_detalle, columns=cols, show="headings")
    tree_detalle.heading("trata", text="Tratamiento")
    tree_detalle.heading("pieza", text="Pieza")
    tree_detalle.heading("precio", text="Precio")
    tree_detalle.column("trata", width=250)
    tree_detalle.column("pieza", width=80, anchor="center")
    tree_detalle.column("precio", width=100, anchor="e")
    tree_detalle.pack(side="left", fill="both", expand=True)

    scroll = ttk.Scrollbar(frame_detalle, command=tree_detalle.yview)
    tree_detalle.config(yscrollcommand=scroll.set)
    scroll.pack(side="right", fill="y")

    frame_hist = tk.LabelFrame(ventana, text="Historial de Presupuestos", bg=ROSA_SUAVE, fg=MORADO)
    frame_hist.place(x=550, y=60, width=520, height=480)

    cols_hist = ("id", "fecha", "paciente", "total")
    tree_hist = ttk.Treeview(frame_hist, columns=cols_hist, show="headings")
    tree_hist.heading("id", text="ID")
    tree_hist.heading("fecha", text="Fecha")
    tree_hist.heading("paciente", text="Paciente")
    tree_hist.heading("total", text="Total")

    tree_hist.column("id", width=50, anchor="center")
    tree_hist.column("fecha", width=120)
    tree_hist.column("paciente", width=180)
    tree_hist.column("total", width=100, anchor="e")
    tree_hist.pack(fill="both", expand=True)

    mapa_pacientes = {}
    mapa_tratamientos = {}
    items_actuales = []

    def cargar_datos():
        pacientes = buscar_pacientes()
        vals_pac = []
        for p in pacientes:
            texto = f"{p[1]} (NIT:{p[3]})"
            mapa_pacientes[texto] = p
            vals_pac.append(texto)
        combo_pacientes['values'] = vals_pac

        tratas = obtener_tratamientos()
        vals_trata = []
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

        if not trata_nombre: return

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
            messagebox.showerror("Error", "Agregue tratamientos primero")
            return

        id_paciente = mapa_pacientes[pac_texto][0]

        try:
            id_pres = crear_presupuesto_cabecera(id_paciente, "UsuarioActual")  # Pasar usuario real si lo tienes

            for it in items_actuales:
                agregar_detalle_presupuesto(id_pres, it['id_trata'], it['pieza'], it['precio'], it['notas'])

            messagebox.showinfo("Éxito", f"Presupuesto #{id_pres} guardado.")

            items_actuales.clear()
            for x in tree_detalle.get_children(): tree_detalle.delete(x)
            combo_pacientes.set("")
            cargar_datos()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def realizar_cobro():
        seleccionado = tree_hist.focus()
        if not seleccionado:
            messagebox.showwarning("Atención", "Seleccione un presupuesto del historial para cobrar.")
            return

        datos = tree_hist.item(seleccionado, 'values')
        id_presupuesto = datos[0]

        resp = messagebox.askyesno("Confirmar Cobro",
                                   f"¿Desea registrar el pago del Presupuesto #{id_presupuesto}?")
        if resp:
            exito, mensaje = cobrar_presupuesto(id_presupuesto)

            if exito:
                messagebox.showinfo("Pago Registrado", mensaje)
                cargar_datos()
            else:
                messagebox.showerror("Error", mensaje)

    btn_cobrar = tk.Button(frame_hist, text="💰 COBRAR SELECCIONADO", bg="green", fg="white",
                           font=("Arial", 10, "bold"), command=realizar_cobro)
    btn_cobrar.pack(side="bottom", fill="x", pady=5, padx=5)

    combo_pacientes.bind("<<ComboboxSelected>>", al_seleccionar_paciente)
    combo_tratamiento.bind("<<ComboboxSelected>>", al_seleccionar_tratamiento)

    _boton(ventana, "Agregar (+)", agregar_item, x=370, y=300, w=160, h=30)
    _boton(ventana, "GUARDAR TODO", guardar_presupuesto, x=30, y=550, w=200, h=40)
    _boton(ventana, "Cerrar", ventana.destroy, x=250, y=550, w=150, h=40)

    cargar_datos()