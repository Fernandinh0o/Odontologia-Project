import tkinter as tk
from tkinter import messagebox
import os

from interfaz.menu_admin import mostrar_menu_admin
from interfaz.menu_secretaria import mostrar_menu_secretaria
from interfaz.usuarios_controlador import autenticar



ancho = 900
alto = 520

rosa_suave = "#E8D4E0"   # Rosa frame
texto_claro = "#FFFFFF" # Texto para botones oscuros
morado = "#4B2A6A"      # Morado (botones)
fondo = "#FFFFFF"       # Fondo general
texto_gris = "#5B5B5B"

ruta_logo = "img/logo_clinica_dental.png"


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



def login(root):
    ventana = root
    ventana.title("Login - Clinica dental")
    ventana.geometry(f"{ancho}x{alto}")
    ventana.configure(bg=fondo)
    ventana.resizable(False, False)


    for w in ventana.winfo_children():
        w.destroy()

    def cerrar_app():
        ventana.destroy()

    ventana.protocol("WM_DELETE_WINDOW", cerrar_app)

    canvas = tk.Canvas(ventana, bg=fondo, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    ancho_panel = 660
    alto_panel = 400

    panel_x = (ancho - ancho_panel) // 2
    panel_y = (alto - alto_panel) // 2

    rounded_rect(
        canvas,
        panel_x, panel_y,
        panel_x + ancho_panel, panel_y + alto_panel,
        r=28,
        fill=rosa_suave,
        outline=rosa_suave
    )

    panel = tk.Frame(ventana, bg=rosa_suave)
    panel.place(x=panel_x, y=panel_y, width=ancho_panel, height=alto_panel)


    if os.path.exists(ruta_logo):
        logo_img = tk.PhotoImage(file=ruta_logo)
        lbl_logo = tk.Label(panel, image=logo_img, bg=rosa_suave)
        lbl_logo.image = logo_img
        lbl_logo.place(x=(ancho_panel - logo_img.width()) // 2, y=20)


    tk.Button(
        panel, text="X",
        bg=morado, fg=texto_claro,
        bd=0, font=("Arial", 10, "bold"),
        command=cerrar_app
    ).place(x=ancho_panel - 45, y=15, width=30, height=25)


    tk.Label(panel, text="Usuario", bg=rosa_suave, fg=texto_gris).place(x=140, y=160)
    entry_user = tk.Entry(panel, bd=0, font=("Arial", 12))
    entry_user.place(x=140, y=180, width=380, height=22)
    tk.Frame(panel, bg=texto_claro).place(x=140, y=205, width=380, height=2)

    # Contraseña
    tk.Label(panel, text="Contraseña", bg=rosa_suave, fg=texto_gris).place(x=140, y=220)
    entry_pwd = tk.Entry(panel, bd=0, font=("Arial", 12), show="*")
    entry_pwd.place(x=140, y=240, width=380, height=22)
    tk.Frame(panel, bg=texto_claro).place(x=140, y=265, width=380, height=2)


    lbl_error = tk.Label(panel, bg=rosa_suave, fg=texto_gris, font=("Arial", 9, "bold"))

    # Ojito
    mostrar = False

    def toggle_password():
        nonlocal mostrar
        mostrar = not mostrar
        entry_pwd.config(show="" if mostrar else "*")

    btn_eye = tk.Button(
        panel, text="👁",
        bg="white", fg=morado, bd=0,
        font=("Arial", 12),
        command=toggle_password
    )
    btn_eye.place(x=530, y=236, width=40, height=25)


    def recuperar():
        messagebox.showinfo("Recuperar contraseña", "Contacta con administración")

    tk.Button(
        panel, text="Recuperar contraseña",
        bg=morado, fg=texto_claro,
        bd=0, font=("Arial", 8, "bold"),
        command=recuperar
    ).place(x=140, y=275, width=130, height=18)


    def ingresar():
        usuario = entry_user.get().strip()
        pwd = entry_pwd.get().strip()

        if not usuario or not pwd:
            lbl_error.config(text="Complete todos los campos")
            lbl_error.place(x=260, y=278)
            return

        datos = autenticar(usuario, pwd)

        if datos:

            _, nombre, rol = datos
            lbl_error.place_forget()

            messagebox.showinfo("Acceso", f"Bienvenido {nombre}\nRol: {rol}")
            ventana.withdraw()
            menu_principal(ventana, rol)
        else:
            lbl_error.config(text="Credenciales incorrectas")
            lbl_error.place(x=285, y=278)

    tk.Button(
        panel, text="Iniciar sesión",
        bg=morado, fg=texto_claro,
        bd=0, font=("Arial", 10, "bold"),
        command=ingresar
    ).place(x=(ancho_panel - 120) // 2, y=320, width=120, height=25)

    ventana.bind("<Return>", lambda e: ingresar())
    entry_user.focus()



def menu_principal(root, rol):
    def cerrar_app():
        root.destroy()

    def cerrar_sesion():

        for widget in root.winfo_children():
            widget.destroy()
        root.deiconify()
        login(root)

    if rol in {"Secretaria", "Empleado"}:
        mostrar_menu_secretaria(root, cerrar_app, rol, cerrar_sesion)
        return

    if rol == "Odontologo":
        mostrar_menu_admin(root, cerrar_app, cerrar_sesion)
        return

    ventana = tk.Toplevel()
    ventana.title("Menú Principal")
    ventana.geometry("300x250")

    tk.Label(ventana, text=f"Rol: {rol}", font=("Arial", 12)).pack(pady=10)

    def ejecutar():
        messagebox.showinfo("Ejecutar", "Función en desarrollo")

    tk.Button(ventana, text="▶ Ejecutar", command=ejecutar).pack(pady=5)

    ventana.protocol("WM_DELETE_WINDOW", cerrar_app)

    if rol == "Usuario":
        tk.Label(ventana, text="Acceso de usuario").pack(pady=5)
        tk.Button(ventana, text="Salir", command=cerrar_app).pack(pady=5)
