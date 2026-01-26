import tkinter as tk
from tkinter import messagebox
from modulos.users.usuarios_controlador import autenticar

def login():
    ventana = tk.Toplevel()
    ventana.title("Login")
    ventana.geometry("300x200")

    tk.Label(ventana, text="Usuario").pack(pady=5)
    entry_user = tk.Entry(ventana)
    entry_user.pack()

    tk.Label(ventana, text="Contraseña").pack(pady=5)
    entry_pwd = tk.Entry(ventana, show="*")
    entry_pwd.pack()

    def ingresar():
        usuario = entry_user.get()
        pwd = entry_pwd.get()

        if not usuario or not pwd:
            messagebox.showerror("Error", "Complete todos los campos")
            return

        datos = autenticar(usuario, pwd)

        if datos:
            _, nombre, rol = datos
            messagebox.showinfo("Acceso", f"Bienvenido {nombre}\nRol: {rol}")
            ventana.destroy()
            menu_principal(rol)
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")

    tk.Button(ventana, text="Ingresar", command=ingresar).pack(pady=15)


def menu_principal(rol):
    ventana = tk.Toplevel()
    ventana.title("Menú Principal")
    ventana.geometry("300x250")

    tk.Label(ventana, text=f"Rol: {rol}", font=("Arial", 12)).pack(pady=10)

    if rol == "Secretaria":
        tk.Button(
    tk.Button(

    elif rol == "Odontologo":
        tk.Button(ventana, text="Agenda").pack(pady=5)
        tk.Button(ventana, text="Pacientes").pack(pady=5)

from modulos.users.usuarios_controlador import (
    listar_usuarios,
    borrar_usuario,
    registrar_usuario
)

def gestor_usuarios():
    ventana = tk.Toplevel()
    ventana.title("Gestor de Usuarios")
    ventana.geometry("600x400")

    # -------- Formulario --------
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

    # -------- Tabla --------
    frame_tabla = tk.Frame(ventana)
    frame_tabla.pack(fill="both", expand=True)

    tabla = tk.Listbox(frame_tabla)
    tabla.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(frame_tabla)
    scrollbar.pack(side="right", fill="y")

    tabla.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=tabla.yview)

    # -------- Funciones --------
    def cargar():
        tabla.delete(0, tk.END)
        for u in listar_usuarios():
            tabla.insert(tk.END, f"{u[0]} | {u[1]} | {u[2]} | {u[3]}")

    def crear():
        datos = {
            "nombre": entry_nombre.get(),
            "telefono": entry_tel.get(),
            "rol": entry_rol.get(),
            "contrasena": entry_pwd.get(),
            "especialidad": entry_esp.get()
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

    # -------- Botones --------
    frame_btn = tk.Frame(ventana)
    frame_btn.pack(pady=10)

    tk.Button(frame_btn, text="Crear", command=crear).grid(row=0, column=0, padx=5)
    tk.Button(frame_btn, text="Eliminar", command=eliminar).grid(row=0, column=1, padx=5)

    cargar()
