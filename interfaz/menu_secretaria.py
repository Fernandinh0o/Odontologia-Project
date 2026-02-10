import tkinter as tk
from tkinter import messagebox, ttk
import importlib
import importlib.util

from gestores.gestor_inventario import (
    actualizar_producto,
    obtener_productos,
    registrar_producto,
)
from interfaz.usuarios_controlador import (
    borrar_usuario,
    listar_usuarios,
    registrar_usuario,
)
from modelos.producto import Producto
from interfaz.modulo_ventas import mostrar_modulo_ventas



ANCHO = 900
ALTO = 520

ROSA_SUAVE = "#E8D4E0"
TEXTO_CLARO = "#FFFFFF"
MORADO = "#4B2A6A"
FONDO = "#FFFFFF"
TEXTO_GRIS = "#5B5B5B"
AZUL_CLARO = "#80D8FF"

MORADO_HEADER = "#5C2D91"
MORADO_SIDEBAR = "#6A3BA0"
LILA_CONTENIDO = "#F3ECF8"
LILA_PANEL = "#FFFFFF"
FUCSIA_ACCENTO = "#A40078"
FUCSIA_BOTON = "#8F0066"
TEXTO_OSCURO = "#3D2A57"


CTK_DISPONIBLE = importlib.util.find_spec("customtkinter") is not None
ctk = importlib.import_module("customtkinter") if CTK_DISPONIBLE else None


def rounded_rect(canvas, x1, y1, x2, y2, r=25, **kwargs):
    points = [
        x1 + r, y1,
        x2 - r, y1,
        x2, y1,
        x2, y1 + r,
        x2, y2 - r,
        x2, y2,
        x2 - r, y2,
        x1 + r, y2,
        x1, y2,
        x1, y2 - r,
        x1, y1 + r,
        x1, y1
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)


def _crear_panel(ventana, titulo=""):

    ventana.configure(bg=FONDO)
    ventana.resizable(False, False)

    canvas = tk.Canvas(ventana, bg=FONDO, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    ancho_panel = 720
    alto_panel = 420

    panel_x = (ANCHO - ancho_panel) // 2
    panel_y = (ALTO - alto_panel) // 2

    rounded_rect(
        canvas,
        panel_x, panel_y,
        panel_x + ancho_panel, panel_y + alto_panel,
        r=28,
        fill=ROSA_SUAVE,
        outline=ROSA_SUAVE
    )

    panel = tk.Frame(ventana, bg=ROSA_SUAVE)
    panel.place(x=panel_x, y=panel_y, width=ancho_panel, height=alto_panel)

    if titulo:
        tk.Label(panel, text=titulo, bg=ROSA_SUAVE, fg=MORADO,
                 font=("Arial", 16, "bold")).place(x=25, y=20)

    return panel, ancho_panel, alto_panel


def _boton(panel, text, command, x, y, w=180, h=35):
    tk.Button(
        panel,
        text=text,
        bg=MORADO,
        fg=TEXTO_CLARO,
        bd=0,
        font=("Arial", 11, "bold"),
        command=command
    ).place(x=x, y=y, width=w, height=h)


# ================== MENÚ SECRETARIA ==================
def _boton_sidebar_tk(parent, texto, comando, y, activo=False):
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


def mostrar_menu_secretaria(root, cerrar_app, rol, cerrar_sesion):
    if rol not in {"Secretaria", "Empleado"}:
        messagebox.showerror(
            "Acceso denegado",
            "Esta vista solo está disponible para usuarios con rol Secretaria.",
        )
        return

    ventana = tk.Toplevel()
    ventana.title("Menú Secretaria")
    ventana.geometry(f"{ANCHO}x{ALTO}")
    ventana.configure(bg=MORADO_HEADER)
    ventana.resizable(False, False)

    if CTK_DISPONIBLE:
        ctk.set_appearance_mode("light")

        contenedor = ctk.CTkFrame(
            ventana,
            fg_color=MORADO_HEADER,
            corner_radius=0,
        )
        contenedor.pack(fill="both", expand=True)

        cabecera = ctk.CTkFrame(
            contenedor,
            fg_color=MORADO_HEADER,
            corner_radius=0,
            height=58,
        )
        cabecera.pack(fill="x", side="top")
        ctk.CTkLabel(
            cabecera,
            text="☰  Clínica Dental",
            text_color=FUCSIA_ACCENTO,
            font=("Arial", 24, "bold"),
        ).pack(side="left", padx=18, pady=10)

        frame_principal = ctk.CTkFrame(
            contenedor,
            fg_color=LILA_CONTENIDO,
            corner_radius=0,
        )
        frame_principal.pack(fill="both", expand=True)

        frame_principal.grid_rowconfigure(0, weight=1)
        frame_principal.grid_columnconfigure(0, weight=0)
        frame_principal.grid_columnconfigure(1, weight=1)

        sidebar = ctk.CTkFrame(
            frame_principal,
            fg_color=MORADO_SIDEBAR,
            corner_radius=0,
            width=250,
        )
        sidebar.grid(row=0, column=0, sticky="ns")
        sidebar.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            sidebar,
            text="Secciones",
            text_color="#F1DBFF",
            font=("Arial", 16, "bold"),
        ).grid(row=0, column=0, padx=24, pady=(24, 10), sticky="w")

        ctk.CTkLabel(
            sidebar,
            text=f"Rol: {rol}",
            text_color="#F6EFFF",
            font=("Arial", 12),
        ).grid(row=1, column=0, padx=24, pady=(0, 20), sticky="w")

        botones = [
            ("🗂  Gestor de Usuarios", gestor_usuarios, False),
            ("📦  Inventario (Agregar)", gestor_inventario, False),
            ("📋  Ver Inventario", mostrar_inventario, False),
            ("💳  Módulo de Ventas", mostrar_modulo_ventas, True),
            ("↩  Cerrar Sesión", cerrar_sesion, False),
        ]

        for fila, (texto, comando, seleccionado) in enumerate(botones, start=2):
            ctk.CTkButton(
                sidebar,
                text=texto,
                command=comando,
                corner_radius=8,
                height=40,
                anchor="w",
                font=("Arial", 12, "bold"),
                fg_color=FUCSIA_ACCENTO if seleccionado else "transparent",
                text_color="#FFFFFF" if seleccionado else "#D8EBF5",
                hover_color="#83005F" if seleccionado else "#5A3186",
            ).grid(row=fila, column=0, padx=24, pady=8, sticky="ew")

        area_contenido = ctk.CTkFrame(
            frame_principal,
            fg_color=LILA_CONTENIDO,
            corner_radius=0,
        )
        area_contenido.grid(row=0, column=1, sticky="nsew", padx=24, pady=20)

        ctk.CTkLabel(
            area_contenido,
            text="Panel principal - Secretaría",
            text_color=TEXTO_OSCURO,
            font=("Arial", 24, "bold"),
        ).pack(anchor="nw", pady=(4, 8))

        ctk.CTkLabel(
            area_contenido,
            text="Selecciona una opción del menú lateral para abrir cada módulo.",
            text_color="#6F558F",
            font=("Arial", 13),
        ).pack(anchor="nw")

        tarjetas = ctk.CTkFrame(
            area_contenido,
            fg_color=LILA_PANEL,
            corner_radius=10,
            border_color="#DCCAE8",
            border_width=1,
            height=280,
        )
        tarjetas.pack(fill="x", pady=(22, 0))
        tarjetas.pack_propagate(False)

        ctk.CTkLabel(
            tarjetas,
            text="Accesos rápidos",
            text_color=TEXTO_OSCURO,
            font=("Arial", 16, "bold"),
        ).pack(anchor="nw", padx=20, pady=(16, 8))

        for texto, comando in [
            ("Abrir gestor de usuarios", gestor_usuarios),
            ("Agregar producto al inventario", gestor_inventario),
            ("Ver inventario completo", mostrar_inventario),
        ]:
            ctk.CTkButton(
                tarjetas,
                text=texto,
                command=comando,
                fg_color=FUCSIA_BOTON,
                hover_color="#790055",
                corner_radius=8,
                height=34,
                font=("Arial", 12, "bold"),
                width=280,
            ).pack(anchor="nw", padx=20, pady=6)

    else:
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

        tk.Label(sidebar, text="Secciones", bg=MORADO_SIDEBAR, fg="#F1DBFF",
                 font=("Arial", 16, "bold")).place(x=16, y=20)
        tk.Label(sidebar, text=f"Rol: {rol}", bg=MORADO_SIDEBAR, fg="#F6EFFF",
                 font=("Arial", 11)).place(x=16, y=52)

        _boton_sidebar_tk(sidebar, "🗂  Gestor de Usuarios", gestor_usuarios, y=95)
        _boton_sidebar_tk(sidebar, "📦  Inventario (Agregar)", gestor_inventario, y=145)
        _boton_sidebar_tk(sidebar, "📋  Ver Inventario", mostrar_inventario, y=195)
        _boton_sidebar_tk(sidebar, "💳  Módulo de Ventas", mostrar_modulo_ventas, y=245, activo=True)
        _boton_sidebar_tk(sidebar, "↩  Cerrar Sesión", cerrar_sesion, y=295)

        contenido = tk.Frame(cuerpo, bg=LILA_CONTENIDO)
        contenido.place(x=260, y=0, width=ANCHO - 260, height=ALTO - 58)
        tk.Label(
            contenido,
            text="Panel principal - Secretaría",
            bg=LILA_CONTENIDO,
            fg=TEXTO_OSCURO,
            font=("Arial", 24, "bold"),
        ).place(x=24, y=20)
        tk.Label(
            contenido,
            text="Selecciona una opción del menú lateral para abrir cada módulo.",
            bg=LILA_CONTENIDO,
            fg="#6F558F",
            font=("Arial", 12),
        ).place(x=24, y=62)

        tarjeta = tk.Frame(contenido, bg=LILA_PANEL, highlightbackground="#DCCAE8", highlightthickness=1)
        tarjeta.place(x=24, y=100, width=ANCHO - 310, height=260)
        tk.Label(
            tarjeta,
            text="Accesos rápidos",
            bg=LILA_PANEL,
            fg=TEXTO_OSCURO,
            font=("Arial", 15, "bold"),
        ).place(x=16, y=16)

        botones = [
            ("Abrir gestor de usuarios", gestor_usuarios),
            ("Agregar producto al inventario", gestor_inventario),
            ("Ver inventario completo", mostrar_inventario),
        ]
        for i, (texto, comando) in enumerate(botones):
            tk.Button(
                tarjeta,
                text=texto,
                command=comando,
                bg=FUCSIA_BOTON,
                activebackground="#790055",
                fg="#FFFFFF",
                activeforeground="#FFFFFF",
                bd=0,
                font=("Arial", 11, "bold"),
                cursor="hand2",
            ).place(x=16, y=56 + (i * 46), width=280, height=32)

    ventana.protocol("WM_DELETE_WINDOW", cerrar_sesion)



def gestor_usuarios():
    ventana = tk.Toplevel()
    ventana.title("Gestor de Usuarios")
    ventana.geometry(f"{ANCHO}x{ALTO}")

    panel, ancho_panel, _ = _crear_panel(ventana, "Gestor de Usuarios")


    frame_form = tk.Frame(panel, bg=ROSA_SUAVE)
    frame_form.place(x=30, y=90, width=320, height=280)

    def label(txt, r):
        tk.Label(frame_form, text=txt, bg=ROSA_SUAVE, fg=TEXTO_GRIS,
                 font=("Arial", 10, "bold")).grid(row=r, column=0, sticky="w", pady=6)

    label("Nombre", 0)
    label("Teléfono", 1)
    label("Rol", 2)
    label("Contraseña", 3)
    label("Especialidad", 4)

    entry_nombre = tk.Entry(frame_form, bd=0, font=("Arial", 11))
    entry_tel = tk.Entry(frame_form, bd=0, font=("Arial", 11))
    entry_rol = tk.Entry(frame_form, bd=0, font=("Arial", 11))
    entry_pwd = tk.Entry(frame_form, bd=0, font=("Arial", 11), show="*")
    entry_esp = tk.Entry(frame_form, bd=0, font=("Arial", 11))

    entry_nombre.grid(row=0, column=1, padx=10)
    entry_tel.grid(row=1, column=1, padx=10)
    entry_rol.grid(row=2, column=1, padx=10)
    entry_pwd.grid(row=3, column=1, padx=10)
    entry_esp.grid(row=4, column=1, padx=10)

    # Lista (derecha)
    frame_lista = tk.Frame(panel, bg=ROSA_SUAVE)
    frame_lista.place(x=380, y=90, width=480, height=280)

    tabla = tk.Listbox(frame_lista, font=("Arial", 10))
    tabla.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(frame_lista)
    scrollbar.pack(side="right", fill="y")

    tabla.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=tabla.yview)

    def cargar():
        tabla.delete(0, tk.END)
        for usuario in listar_usuarios():
            tabla.insert(tk.END, f"{usuario[0]} | {usuario[1]} | {usuario[2]} | {usuario[3]}")

    def crear():
        datos = {
            "nombre": entry_nombre.get(),
            "telefono": entry_tel.get(),
            "rol": entry_rol.get(),
            "contrasena": entry_pwd.get(),
            "especialidad": entry_esp.get(),
        }

        if not datos["nombre"] or not datos["rol"] or not datos["contrasena"]:
            messagebox.showerror("Error", "Campos obligatorios faltantes")
            return

        registrar_usuario(datos)
        cargar()
        messagebox.showinfo("OK", "Usuario creado")

    def eliminar():
        seleccion = tabla.curselection()
        if not seleccion:
            return

        linea = tabla.get(seleccion)
        id_usuario = int(linea.split("|")[0].strip())

        borrar_usuario(id_usuario)
        cargar()

    _boton(panel, "Crear", crear, x=30, y=385, w=150, h=35)
    _boton(panel, "Eliminar", eliminar, x=200, y=385, w=150, h=35)

    # Botón cerrar
    tk.Button(
        panel, text="X",
        bg=MORADO, fg=TEXTO_CLARO,
        bd=0, font=("Arial", 10, "bold"),
        command=ventana.destroy
    ).place(x=ancho_panel - 55, y=20, width=35, height=28)

    cargar()



def gestor_inventario():
    ventana = tk.Toplevel()
    ventana.title("Inventario - Agregar")
    ventana.geometry(f"{ANCHO}x{ALTO}")

    panel, ancho_panel, _ = _crear_panel(ventana, "Inventario")

    frame_form = tk.Frame(panel, bg=ROSA_SUAVE)
    frame_form.place(x=40, y=100, width=520, height=260)

    def etiqueta(txt, r):
        tk.Label(
            frame_form,
            text=txt,
            bg=ROSA_SUAVE,
            fg=TEXTO_GRIS,
            font=("Arial", 10, "bold"),
        ).grid(row=r, column=0, sticky="w", pady=6)

    etiqueta("ID Producto", 0)
    etiqueta("Nombre", 1)
    etiqueta("Categoría", 2)
    etiqueta("Cantidad", 3)
    etiqueta("Precio Unitario", 4)
    etiqueta("Stock Mínimo", 5)
    etiqueta("Proveedor", 6)
    etiqueta("Descripción", 7)

    entry_id = tk.Entry(frame_form, bd=0, font=("Arial", 12))
    entry_nombre = tk.Entry(frame_form, bd=0, font=("Arial", 12))
    entry_categoria = tk.Entry(frame_form, bd=0, font=("Arial", 12))
    entry_cantidad = tk.Entry(frame_form, bd=0, font=("Arial", 12))
    entry_precio = tk.Entry(frame_form, bd=0, font=("Arial", 12))
    entry_stock = tk.Entry(frame_form, bd=0, font=("Arial", 12))
    entry_proveedor = tk.Entry(frame_form, bd=0, font=("Arial", 12))
    entry_descripcion = tk.Entry(frame_form, bd=0, font=("Arial", 12))

    entry_id.grid(row=0, column=1, padx=15)
    entry_nombre.grid(row=1, column=1, padx=15)
    entry_categoria.grid(row=2, column=1, padx=15)
    entry_cantidad.grid(row=3, column=1, padx=15)
    entry_precio.grid(row=4, column=1, padx=15)
    entry_stock.grid(row=5, column=1, padx=15)
    entry_proveedor.grid(row=6, column=1, padx=15)
    entry_descripcion.grid(row=7, column=1, padx=15)

    def _leer_formulario():
        id_producto = entry_id.get().strip()
        nombre = entry_nombre.get().strip()
        categoria = entry_categoria.get().strip()
        cantidad = entry_cantidad.get().strip()
        precio = entry_precio.get().strip()
        stock_minimo = entry_stock.get().strip()
        proveedor = entry_proveedor.get().strip()
        descripcion = entry_descripcion.get().strip()

        if (
            not id_producto
            or not nombre
            or not categoria
            or not cantidad
            or not precio
            or not stock_minimo
            or not proveedor
        ):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        try:
            id_producto_int = int(id_producto)
            cantidad_int = int(cantidad)
            precio_float = float(precio)
            stock_minimo_int = int(stock_minimo)
        except ValueError:
            messagebox.showerror(
                "Error",
                "ID, cantidad, stock mínimo y precio deben ser numéricos válidos",
            )
            return None

        return Producto(
            id_producto=id_producto_int,
            nombre=nombre,
            categoria=categoria,
            cantidad=cantidad_int,
            precio_unitario=precio_float,
            stock_minimo=stock_minimo_int,
            proveedor=proveedor,
            descripcion=descripcion,
        )

    def _limpiar():
        for entry in (
            entry_id,
            entry_nombre,
            entry_categoria,
            entry_cantidad,
            entry_precio,
            entry_stock,
            entry_proveedor,
            entry_descripcion,
        ):
            entry.delete(0, tk.END)

    def guardar():
        producto = _leer_formulario()
        if not producto:
            return

        try:
            registrar_producto(producto)
        except Exception as exc:
            messagebox.showerror("Error", str(exc))
            return

        messagebox.showinfo("OK", "Producto registrado")
        _limpiar()

    def actualizar():
        producto = _leer_formulario()
        if not producto:
            return

        try:
            actualizar_producto(producto)
        except Exception as exc:
            messagebox.showerror("Error", str(exc))
            return

        messagebox.showinfo("OK", "Producto actualizado")
        _limpiar()

    _boton(panel, "Guardar", guardar, x=60, y=375, w=160, h=35)
    _boton(panel, "Actualizar", actualizar, x=240, y=375, w=160, h=35)
    _boton(panel, "Cerrar", ventana.destroy, x=420, y=375, w=160, h=35)

    tk.Button(
        panel, text="X",
        bg=MORADO, fg=TEXTO_CLARO,
        bd=0, font=("Arial", 10, "bold"),
        command=ventana.destroy
    ).place(x=ancho_panel - 55, y=20, width=35, height=28)



def mostrar_inventario():
    ventana = tk.Toplevel()
    ventana.title("Inventario - Productos")
    ventana.geometry(f"{ANCHO}x{ALTO}")

    panel, ancho_panel, _ = _crear_panel(ventana, "Inventario - Productos")

    frame_filtros = tk.Frame(panel, bg=ROSA_SUAVE)
    frame_filtros.place(x=30, y=60, width=ancho_panel - 60, height=80)

    tk.Label(frame_filtros, text="Buscar:", bg=ROSA_SUAVE, fg=TEXTO_GRIS,
             font=("Arial", 10, "bold")).place(x=0, y=5)

    entry_buscar = tk.Entry(frame_filtros, font=("Arial", 10))
    entry_buscar.place(x=60, y=5, width=200)

    var_stock_bajo = tk.BooleanVar()
    check_bajo = tk.Checkbutton(frame_filtros, text="Solo Stock Bajo (< 5)",
                                variable=var_stock_bajo, bg=ROSA_SUAVE,
                                activebackground=ROSA_SUAVE, font=("Arial", 9))
    check_bajo.pack(side="right", padx=10)

    tk.Label(frame_filtros, text="Ordenar por:", bg=ROSA_SUAVE, fg=TEXTO_GRIS,
             font=("Arial", 10, "bold")).place(x=0, y=40)

    opciones_orden = [
        "ID (Por defecto)",
        "Nombre (A - Z)",
        "Nombre (Z - A)",
        "Precio (Mayor a Menor)",
        "Precio (Menor a Mayor)",
        "Cantidad (Mayor a Menor)",
        "Cantidad (Menor a Mayor)"
    ]
    combo_orden = ttk.Combobox(frame_filtros, values=opciones_orden, state="readonly", font=("Arial", 9))
    combo_orden.current(0)
    combo_orden.place(x=100, y=40, width=180)

    frame_tabla = tk.Frame(panel, bg=ROSA_SUAVE)
    frame_tabla.place(x=30, y=120, width=ancho_panel - 60, height=310)

    columnas = (
        "id",
        "nombre",
        "categoria",
        "cantidad",
        "precio_unitario",
        "stock_minimo",
        "proveedor",
        "descripcion",
    )
    tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")
    tabla.heading("id", text="ID")
    tabla.heading("nombre", text="Nombre")
    tabla.heading("categoria", text="Categoría")
    tabla.heading("cantidad", text="Cantidad")
    tabla.heading("precio_unitario", text="Precio Unitario")
    tabla.heading("stock_minimo", text="Stock Mínimo")
    tabla.heading("proveedor", text="Proveedor")
    tabla.heading("descripcion", text="Descripción")

    tabla.column("id", width=60, anchor="center")
    tabla.column("nombre", width=200, anchor="w")
    tabla.column("categoria", width=140, anchor="w")
    tabla.column("cantidad", width=90, anchor="center")
    tabla.column("precio_unitario", width=120, anchor="center")
    tabla.column("stock_minimo", width=110, anchor="center")
    tabla.column("proveedor", width=140, anchor="w")
    tabla.column("descripcion", width=200, anchor="w")

    scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
    tabla.configure(yscrollcommand=scrollbar.set)

    tabla.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def ejecutar_busqueda():
        for item in tabla.get_children():
            tabla.delete(item)

        try:
            todos = obtener_productos()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        texto_busqueda = entry_buscar.get().lower()
        solo_bajo = var_stock_bajo.get()
        criterio_orden = combo_orden.get()

        lista_filtrada = []


        for prod in todos:
            nombre_prod = str(prod[1]).lower()
            categoria_prod = str(prod[2])
            cantidad_prod = int(prod[3])
            precio_prod = float(prod[4])

            if texto_busqueda and texto_busqueda not in nombre_prod:
                continue

            if solo_bajo and cantidad_prod > 5:
                continue
            lista_filtrada.append(prod)

        if criterio_orden == "Nombre (A - Z)":
            lista_filtrada.sort(key=lambda x: x[1].lower())

        elif criterio_orden == "Nombre (Z - A)":
            lista_filtrada.sort(key=lambda x: x[1].lower(), reverse=True)

        elif criterio_orden == "Precio (Mayor a Menor)":
            lista_filtrada.sort(key=lambda x: x[3], reverse=True)

        elif criterio_orden == "Precio (Menor a Mayor)":
            lista_filtrada.sort(key=lambda x: x[3])

        elif criterio_orden == "Cantidad (Mayor a Menor)":
            lista_filtrada.sort(key=lambda x: x[2], reverse=True)

        elif criterio_orden == "Cantidad (Menor a Mayor)":
            lista_filtrada.sort(key=lambda x: x[2])


        for prod in lista_filtrada:
            tabla.insert("", "end", values=prod)
    btn_buscar = tk.Button(frame_filtros, text="🔍", bg=MORADO, fg=TEXTO_CLARO,
                           font=("Arial", 9, "bold"), command=ejecutar_busqueda)
    btn_buscar.pack(side="right", padx=5)

    entry_buscar.bind("<Return>", lambda e: ejecutar_busqueda())
    combo_orden.bind("<<ComboboxSelected>>", lambda e: ejecutar_busqueda())
    check_bajo.config(command=ejecutar_busqueda)

    ejecutar_busqueda()

    _boton(panel, "Cerrar", ventana.destroy, x=30, y=410, w=180, h=35)

    tk.Button(panel, text="X", bg=MORADO, fg=TEXTO_CLARO, bd=0,
              font=("Arial", 10, "bold"), command=ventana.destroy
              ).place(x=ancho_panel - 55, y=20, width=35, height=28)
