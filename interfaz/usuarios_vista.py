import tkinter as tk
from tkinter import messagebox

from interfaz.menu_admin import mostrar_menu_admin
from interfaz.menu_empleado import mostrar_menu_empleado
from interfaz.usuarios_controlador import autenticar


def login(root):
    ventana = root
    ventana.title("Login")
    ventana.geometry("300x200")

    def cerrar_app():
        ventana.destroy()

    ventana.protocol("WM_DELETE_WINDOW", cerrar_app)

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
            ventana.withdraw()
            menu_principal(ventana, rol)
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")

    tk.Button(ventana, text="Ingresar", command=ingresar).pack(pady=15)


def menu_principal(root, rol):
    ventana = tk.Toplevel()
    ventana.title("Menú Principal")
    ventana.geometry("300x250")

    tk.Label(ventana, text=f"Rol: {rol}", font=("Arial", 12)).pack(pady=10)

    def ejecutar():
        messagebox.showinfo("Ejecutar", "Función en desarrollo")

    def cerrar_app():
        ventana.destroy()
        root.destroy()

    tk.Button(ventana, text="▶ Ejecutar", command=ejecutar).pack(pady=5)

    ventana.protocol("WM_DELETE_WINDOW", cerrar_app)

    if rol == "Secretaria":
        mostrar_menu_empleado(root, cerrar_app)
    elif rol == "Odontologo":
        mostrar_menu_admin(root, cerrar_app)
    elif rol == "Usuario":
        tk.Label(ventana, text="Acceso de usuario").pack(pady=5)
        tk.Button(ventana, text="Salir", command=cerrar_app).pack(pady=5)
