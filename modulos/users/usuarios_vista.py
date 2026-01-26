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
        tk.Button(ventana, text="Usuarios").pack(pady=5)
        tk.Button(ventana, text="Pacientes").pack(pady=5)
        tk.Button(ventana, text="Citas").pack(pady=5)

    elif rol == "Odontologo":
        tk.Button(ventana, text="Agenda").pack(pady=5)
        tk.Button(ventana, text="Pacientes").pack(pady=5)
