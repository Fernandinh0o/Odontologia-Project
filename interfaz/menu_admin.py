import tkinter as tk
from tkinter import messagebox

from interfaz.menu_secretaria import gestor_inventario, gestor_usuarios, mostrar_inventario
from interfaz.modulo_ventas import mostrar_modulo_ventas
from interfaz.rrhh_historial_vista import RRHHHistorialVista
from interfaz.rrhh_vista import RRHHVista

ANCHO = 900
ALTO = 520

MORADO_HEADER = "#5C2D91"
MORADO_SIDEBAR = "#6A3BA0"
LILA_CONTENIDO = "#F3ECF8"
LILA_PANEL = "#FFFFFF"
FUCSIA_ACCENTO = "#A40078"
MORADO = "#4B2A6A"


def mostrar_menu_admin(root, cerrar_app, cerrar_sesion):
    ventana = tk.Toplevel(root)
    ventana.title("Menú Odontólogo")
    ventana.geometry(f"{ANCHO}x{ALTO}")
    ventana.configure(bg=MORADO_HEADER)
    ventana.resizable(False, False)

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

    sidebar = tk.Frame(cuerpo, bg=MORADO_SIDEBAR)
    sidebar.place(x=0, y=0, width=260, height=ALTO - 58)

    tk.Label(
        sidebar,
        text="Secciones",
        bg=MORADO_SIDEBAR,
        fg="#F1DBFF",
        font=("Arial", 16, "bold"),
    ).place(x=16, y=20)
    tk.Label(
        sidebar,
        text="Rol: Odontólogo",
        bg=MORADO_SIDEBAR,
        fg="#F6EFFF",
        font=("Arial", 11),
    ).place(x=16, y=52)

    contenido = tk.Frame(cuerpo, bg=LILA_CONTENIDO)
    contenido.place(x=260, y=0, width=ANCHO - 260, height=ALTO - 58)

    contenido_dinamico = tk.Frame(
        contenido,
        bg=LILA_PANEL,
        highlightbackground="#DCCAE8",
        highlightthickness=1,
    )
    contenido_dinamico.place(x=24, y=20, width=ANCHO - 310, height=ALTO - 98)

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
        ).place(x=16, y=18)
        tk.Label(
            contenido_dinamico,
            text="Selecciona una opción del menú lateral para abrir cada módulo.",
            bg=LILA_PANEL,
            fg="#6F558F",
            font=("Arial", 12),
        ).place(x=16, y=62)

    def mostrar_rrhh():
        limpiar_contenido()
        vista = RRHHVista(contenido_dinamico)
        vista.grid(row=0, column=0, sticky="nsew")
        contenido_dinamico.grid_rowconfigure(0, weight=1)
        contenido_dinamico.grid_columnconfigure(0, weight=1)

    def mostrar_historial_pagos():
        limpiar_contenido()
        vista = RRHHHistorialVista(contenido_dinamico)
        vista.grid(row=0, column=0, sticky="nsew")
        contenido_dinamico.grid_rowconfigure(0, weight=1)
        contenido_dinamico.grid_columnconfigure(0, weight=1)

    def mostrar_en_desarrollo():
        messagebox.showinfo("En desarrollo", "Función en desarrollo")

    _boton_sidebar(sidebar, "🗂  Gestor de Usuarios", gestor_usuarios, y=95)
    _boton_sidebar(sidebar, "📦  Inventario (Agregar)", gestor_inventario, y=145)
    _boton_sidebar(sidebar, "📋  Ver Inventario", mostrar_inventario, y=195)
    _boton_sidebar(sidebar, "💳  Módulo de Ventas", mostrar_modulo_ventas, y=245)
    _boton_sidebar(sidebar, "🗓  Agenda", mostrar_en_desarrollo, y=295)
    _boton_sidebar(sidebar, "🧾  Gestión de Nómina", mostrar_rrhh, y=345, activo=True)
    _boton_sidebar(sidebar, "📋  Historial de Pagos", mostrar_historial_pagos, y=395)
    _boton_sidebar(sidebar, "↩  Cerrar Sesión", cerrar_sesion, y=445)

    mostrar_inicio()
    ventana.protocol("WM_DELETE_WINDOW", cerrar_sesion)


def _boton_sidebar(parent, texto, comando, y, activo=False):
    color_texto = "#FFFFFF" if activo else "#D8EBF5"
    color_fondo = FUCSIA_ACCENTO if activo else MORADO_SIDEBAR
    color_hover = "#83005F" if activo else "#5A3186"

    tk.Button(
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
    ).place(x=15, y=y, width=230, height=40)
