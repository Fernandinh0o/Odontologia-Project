import tkinter as tk
from tkinter import messagebox


def mostrar_menu_admin(root, cerrar_app):
    ventana = tk.Toplevel()
    ventana.title("Menú Administrador")
    ventana.geometry("300x250")

    tk.Label(ventana, text="Rol: Odontólogo", font=("Arial", 12)).pack(pady=10)

    def mostrar_en_desarrollo():
        messagebox.showinfo("En desarrollo", "Función en desarrollo")

    tk.Button(ventana, text="Agenda", command=mostrar_en_desarrollo).pack(pady=5)
    tk.Button(ventana, text="Pacientes", command=mostrar_en_desarrollo).pack(pady=5)
    tk.Button(ventana, text="Salir", command=cerrar_app).pack(pady=5)

    ventana.protocol("WM_DELETE_WINDOW", cerrar_app)
