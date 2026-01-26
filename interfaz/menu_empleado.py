import tkinter as tk
from tkinter import messagebox

from interfaz.usuarios_controlador import (
    borrar_usuario,
    listar_usuarios,
    registrar_usuario,
)


def mostrar_menu_empleado(root, cerrar_app):
    ventana = tk.Toplevel()
    ventana.title("Menú Empleado")
    ventana.geometry("300x250")

    tk.Label(ventana, text="Rol: Secretaria", font=("Arial", 12)).pack(pady=10)

    tk.Button(
        ventana,
        text="Gestor de Usuarios",
        command=gestor_usuarios,
    ).pack(pady=5)
    tk.Button(ventana, text="Salir", command=cerrar_app).pack(pady=5)

    ventana.protocol("WM_DELETE_WINDOW", cerrar_app)


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
