import tkinter as tk
from tkinter import messagebox, ttk

from gestores.gestor_inventario import obtener_productos, registrar_producto
from interfaz.usuarios_controlador import (
    borrar_usuario,
    listar_usuarios,
    registrar_usuario,
)
from modelos.producto import Producto


def mostrar_menu_secretaria(root, cerrar_app, rol, cerrar_sesion):
    if rol not in {"Secretaria", "Empleado"}:
        messagebox.showerror(
            "Acceso denegado",
            "Esta vista solo está disponible para usuarios con rol Secretaria.",
        )
        return

    ventana = tk.Toplevel()
    ventana.title("Menú Secretaria")
    ventana.geometry("300x250")

    tk.Label(ventana, text="Rol: Secretaria", font=("Arial", 12)).pack(pady=10)

    tk.Button(
        ventana,
        text="Gestor de Usuarios",
        command=gestor_usuarios,
    ).pack(pady=5)
    tk.Button(
        ventana,
        text="Inventario",
        command=gestor_inventario,
    ).pack(pady=5)
    tk.Button(
        ventana,
        text="Ver Inventario",
        command=mostrar_inventario,
    ).pack(pady=5)
    tk.Button(ventana, text="Cerrar Sesión", command=cerrar_sesion).pack(pady=5)

    ventana.protocol("WM_DELETE_WINDOW", cerrar_sesion)


def gestor_usuarios():
    ventana = tk.Toplevel()
    ventana.title("Gestor de Usuarios")
    ventana.geometry("600x400")

    frame_form = tk.Frame(ventana)
    frame_form.pack(pady=10)

    tk.Label(frame_form, text="Nombre").grid(row=0, column=0)
    tk.Label(frame_form, text="Teléfono").grid(row=1, column=0)
    tk.Label(frame_form, text="Rol").grid(row=2, column=0)
    tk.Label(frame_form, text="Contraseña").grid(row=3, column=0)
    tk.Label(frame_form, text="Especialidad").grid(row=4, column=0)

    entry_nombre = tk.Entry(frame_form)
    entry_tel = tk.Entry(frame_form)
    entry_rol = tk.Entry(frame_form)
    entry_pwd = tk.Entry(frame_form, show="*")
    entry_esp = tk.Entry(frame_form)

    entry_nombre.grid(row=0, column=1)
    entry_tel.grid(row=1, column=1)
    entry_rol.grid(row=2, column=1)
    entry_pwd.grid(row=3, column=1)
    entry_esp.grid(row=4, column=1)

    frame_tabla = tk.Frame(ventana)
    frame_tabla.pack(fill="both", expand=True)

    tabla = tk.Listbox(frame_tabla)
    tabla.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(frame_tabla)
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
        id_usuario = int(linea.split("|")[0])

        borrar_usuario(id_usuario)
        cargar()

    frame_btn = tk.Frame(ventana)
    frame_btn.pack(pady=10)

    tk.Button(frame_btn, text="Crear", command=crear).grid(row=0, column=0, padx=5)
    tk.Button(frame_btn, text="Eliminar", command=eliminar).grid(row=0, column=1, padx=5)

    cargar()


def gestor_inventario():
    ventana = tk.Toplevel()
    ventana.title("Inventario")
    ventana.geometry("400x250")

    frame_form = tk.Frame(ventana)
    frame_form.pack(pady=10)

    tk.Label(frame_form, text="Nombre").grid(row=0, column=0, sticky="e")
    tk.Label(frame_form, text="Cantidad").grid(row=1, column=0, sticky="e")
    tk.Label(frame_form, text="Precio").grid(row=2, column=0, sticky="e")

    entry_nombre = tk.Entry(frame_form)
    entry_cantidad = tk.Entry(frame_form)
    entry_precio = tk.Entry(frame_form)

    entry_nombre.grid(row=0, column=1)
    entry_cantidad.grid(row=1, column=1)
    entry_precio.grid(row=2, column=1)

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
            messagebox.showerror(
                "Error",
                "Cantidad y precio deben ser valores numéricos válidos",
            )
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

    tk.Button(ventana, text="Guardar", command=guardar).pack(pady=10)


def mostrar_inventario():
    ventana = tk.Toplevel()
    ventana.title("Inventario - Productos")
    ventana.geometry("700x350")

    frame_tabla = tk.Frame(ventana)
    frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)

    columnas = ("id", "nombre", "cantidad", "precio", "descripcion")
    tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")
    tabla.heading("id", text="ID")
    tabla.heading("nombre", text="Nombre")
    tabla.heading("cantidad", text="Cantidad")
    tabla.heading("precio", text="Precio")
    tabla.heading("descripcion", text="Descripción")

    tabla.column("id", width=60, anchor="center")
    tabla.column("nombre", width=160, anchor="w")
    tabla.column("cantidad", width=90, anchor="center")
    tabla.column("precio", width=90, anchor="center")
    tabla.column("descripcion", width=220, anchor="w")

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
