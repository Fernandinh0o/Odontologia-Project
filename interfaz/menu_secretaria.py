import tkinter as tk
from tkinter import messagebox, ttk

from gestores.gestor_inventario import obtener_productos, registrar_producto
from interfaz.usuarios_controlador import (
    borrar_usuario,
    listar_usuarios,
    registrar_usuario,
)
from modelos.producto import Producto



ANCHO = 900
ALTO = 520

ROSA_SUAVE = "#E8D4E0"
TEXTO_CLARO = "#FFFFFF"
MORADO = "#4B2A6A"
FONDO = "#FFFFFF"
TEXTO_GRIS = "#5B5B5B"


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
    ventana.configure(bg=FONDO)
    ventana.resizable(False, False)

    panel, ancho_panel, _ = _crear_panel(ventana, "Menú Secretaria")

    tk.Label(panel, text=f"Rol: {rol}", bg=ROSA_SUAVE, fg=TEXTO_GRIS,
             font=("Arial", 11)).place(x=25, y=55)

    _boton(panel, "Gestor de Usuarios", gestor_usuarios, x=60, y=120, w=260)
    _boton(panel, "Inventario (Agregar)", gestor_inventario, x=60, y=170, w=260)
    _boton(panel, "Ver Inventario", mostrar_inventario, x=60, y=220, w=260)

    _boton(panel, "Cerrar Sesión", cerrar_sesion, x=60, y=300, w=260)


    tk.Button(
        panel, text="X",
        bg=MORADO, fg=TEXTO_CLARO,
        bd=0, font=("Arial", 10, "bold"),
        command=cerrar_sesion
    ).place(x=ancho_panel - 55, y=20, width=35, height=28)

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
    frame_form.place(x=60, y=120, width=420, height=220)

    tk.Label(frame_form, text="Nombre", bg=ROSA_SUAVE, fg=TEXTO_GRIS,
             font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", pady=10)
    tk.Label(frame_form, text="Cantidad", bg=ROSA_SUAVE, fg=TEXTO_GRIS,
             font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="w", pady=10)
    tk.Label(frame_form, text="Precio", bg=ROSA_SUAVE, fg=TEXTO_GRIS,
             font=("Arial", 10, "bold")).grid(row=2, column=0, sticky="w", pady=10)

    entry_nombre = tk.Entry(frame_form, bd=0, font=("Arial", 12))
    entry_cantidad = tk.Entry(frame_form, bd=0, font=("Arial", 12))
    entry_precio = tk.Entry(frame_form, bd=0, font=("Arial", 12))

    entry_nombre.grid(row=0, column=1, padx=15)
    entry_cantidad.grid(row=1, column=1, padx=15)
    entry_precio.grid(row=2, column=1, padx=15)

    def guardar():
        nombre = entry_nombre.get().strip()
        cantidad = entry_cantidad.get().strip()
        precio = entry_precio.get().strip()

        if not nombre or not cantidad or not precio:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        try:
            cantidad_int = int(cantidad)
            precio_float = float(precio)
        except ValueError:
            messagebox.showerror("Error", "Cantidad y precio deben ser números válidos")
            return

        producto = Producto(
            nombre=nombre,
            cantidad=cantidad_int,
            precio=precio_float,
        )

        try:
            registrar_producto(producto)
        except Exception as exc:
            messagebox.showerror("Error", str(exc))
            return

        messagebox.showinfo("OK", "Producto registrado")
        entry_nombre.delete(0, tk.END)
        entry_cantidad.delete(0, tk.END)
        entry_precio.delete(0, tk.END)

    _boton(panel, "Guardar", guardar, x=60, y=360, w=180, h=35)
    _boton(panel, "Cerrar", ventana.destroy, x=260, y=360, w=180, h=35)

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

    frame_tabla = tk.Frame(panel, bg=ROSA_SUAVE)
    frame_tabla.place(x=30, y=90, width=ancho_panel - 60, height=310)

    columnas = ("id", "nombre", "cantidad", "precio", "descripcion")
    tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")
    tabla.heading("id", text="ID")
    tabla.heading("nombre", text="Nombre")
    tabla.heading("cantidad", text="Cantidad")
    tabla.heading("precio", text="Precio")
    tabla.heading("descripcion", text="Descripción")

    tabla.column("id", width=60, anchor="center")
    tabla.column("nombre", width=200, anchor="w")
    tabla.column("cantidad", width=100, anchor="center")
    tabla.column("precio", width=100, anchor="center")
    tabla.column("descripcion", width=260, anchor="w")

    scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
    tabla.configure(yscrollcommand=scrollbar.set)

    tabla.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    try:
        productos = obtener_productos()
    except Exception as exc:
        messagebox.showerror("Error", str(exc))
        return

    for producto in productos:
        tabla.insert("", "end", values=producto)

    _boton(panel, "Cerrar", ventana.destroy, x=30, y=410, w=180, h=35)

    tk.Button(
        panel, text="X",
        bg=MORADO, fg=TEXTO_CLARO,
        bd=0, font=("Arial", 10, "bold"),
        command=ventana.destroy
    ).place(x=ancho_panel - 55, y=20, width=35, height=28)
