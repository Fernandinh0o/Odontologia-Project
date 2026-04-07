import tkinter as tk
from tkinter import messagebox

from interfaz.menu_secretaria import gestor_inventario, gestor_usuarios, mostrar_inventario
from interfaz.modulo_ventas import mostrar_modulo_ventas
from interfaz.rrhh_historial_vista import RRHHHistorialVista
from interfaz.rrhh_vista import RRHHVista
from interfaz.ingresos_odontologo_vista import IngresosOdontologoVista

MORADO_HEADER = "#5C2D91"
MORADO_SIDEBAR = "#6A3BA0"
LILA_CONTENIDO = "#F3ECF8"
LILA_PANEL = "#FFFFFF"
FUCSIA_ACCENTO = "#A40078"
MORADO = "#4B2A6A"


def mostrar_menu_admin(root, cerrar_app, cerrar_sesion):
    ventana = tk.Toplevel(root)
    ventana.title("Menú Odontólogo")
    ventana.configure(bg=MORADO_HEADER)

    ventana.state("zoomed")
    ventana.minsize(900, 600)
    ventana.resizable(True, True)

    cabecera = tk.Frame(ventana, bg=MORADO_HEADER, height=58)
    cabecera.pack(fill="x", side="top")

    tk.Label(
        cabecera,
        text="☰  Clínica Dental",
        bg=MORADO_HEADER,
        fg=FUCSIA_ACCENTO,
        font=("Arial", 22, "bold"),
    ).pack(side="left", padx=15, pady=8)

    cuerpo = tk.Frame(ventana, bg=LILA_CONTENIDO)
    cuerpo.pack(fill="both", expand=True)

    cuerpo.grid_columnconfigure(1, weight=1)
    cuerpo.grid_rowconfigure(0, weight=1)

    sidebar = tk.Frame(cuerpo, bg=MORADO_SIDEBAR, width=260)
    sidebar.grid(row=0, column=0, sticky="ns")

    tk.Label(
        sidebar,
        text="Secciones",
        bg=MORADO_SIDEBAR,
        fg="#F1DBFF",
        font=("Arial", 16, "bold"),
    ).pack(pady=(20, 5), anchor="w", padx=16)

    tk.Label(
        sidebar,
        text="Rol: Odontólogo",
        bg=MORADO_SIDEBAR,
        fg="#F6EFFF",
        font=("Arial", 11),
    ).pack(anchor="w", padx=16)

    contenido = tk.Frame(cuerpo, bg=LILA_CONTENIDO)
    contenido.grid(row=0, column=1, sticky="nsew")

    contenido.grid_rowconfigure(0, weight=1)
    contenido.grid_columnconfigure(0, weight=1)

    contenido_dinamico = tk.Frame(
        contenido,
        bg=LILA_PANEL,
        highlightbackground="#DCCAE8",
        highlightthickness=1,
    )
    contenido_dinamico.grid(row=0, column=0, padx=24, pady=20, sticky="nsew")

    def limpiar_contenido():
        for widget in contenido_dinamico.winfo_children():
            widget.destroy()

    def mostrar_inicio():
        limpiar_contenido()
        tk.Label(
            contenido_dinamico,
            text="Panel principal - Odontología",
            bg=LILA_PANEL,
            fg=MORADO,
            font=("Arial", 22, "bold"),
        ).pack(anchor="nw", padx=16, pady=(18, 5))

        tk.Label(
            contenido_dinamico,
            text="Selecciona una opción del menú lateral para abrir cada módulo.",
            bg=LILA_PANEL,
            fg="#6F558F",
            font=("Arial", 12),
        ).pack(anchor="nw", padx=16)

    def mostrar_rrhh():
        limpiar_contenido()
        vista = RRHHVista(contenido_dinamico)
        vista.pack(fill="both", expand=True)

    def mostrar_historial_pagos():
        limpiar_contenido()
        vista = RRHHHistorialVista(contenido_dinamico)
        vista.pack(fill="both", expand=True)

    def abrir_modulo_ingresos():
        for widget in contenido_dinamico.winfo_children():
            widget.destroy()
        vista = IngresosOdontologoVista(contenido_dinamico)
        vista.pack(fill="both", expand=True)

    def mostrar_en_desarrollo():
        messagebox.showinfo("En desarrollo", "Función en desarrollo")

    _boton_sidebar(sidebar, "🗂  Gestor de Usuarios", gestor_usuarios)
    _boton_sidebar(sidebar, "📦  Inventario (Agregar)", gestor_inventario)
    _boton_sidebar(sidebar, "📋  Ver Inventario", mostrar_inventario)
    _boton_sidebar(sidebar, "💳  Módulo de Ventas", mostrar_modulo_ventas)
    _boton_sidebar(sidebar, "🗓  Agenda", mostrar_en_desarrollo)
    _boton_sidebar(sidebar, "🧾  Gestión de Nómina", mostrar_rrhh, activo=True)
    _boton_sidebar(sidebar, "💵  Gestión de Ingresos", abrir_modulo_ingresos)
    _boton_sidebar(sidebar, "📋  Historial de Pagos", mostrar_historial_pagos)
    _boton_sidebar(sidebar, "↩  Cerrar Sesión", cerrar_sesion)

    mostrar_inicio()
    ventana.protocol("WM_DELETE_WINDOW", cerrar_sesion)


def _boton_sidebar(parent, texto, comando, activo=False):
    color_texto = "#FFFFFF" if activo else "#D8EBF5"
    color_fondo = FUCSIA_ACCENTO if activo else MORADO_SIDEBAR
    color_hover = "#83005F" if activo else "#5A3186"

    btn = tk.Button(
        parent,
        text=texto,
        command=comando,
        bg=color_fondo,
        activebackground=color_hover,
        fg=color_texto,
        activeforeground="#FFFFFF",
        bd=0,
        anchor="w",
        padx=14,
        font=("Arial", 10, "bold"),
        cursor="hand2",
    )
    btn.pack(fill="x", padx=15, pady=5, ipady=10)