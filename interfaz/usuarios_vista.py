import tkinter as tk
from tkinter import messagebox
import os
import json
from PIL import Image, ImageTk  # ✅ para redimensionar bien

from interfaz.menu_admin import mostrar_menu_admin
from interfaz.menu_secretaria import mostrar_menu_secretaria
from interfaz.usuarios_controlador import autenticar

BG = "#F8F6FB"
CARD_BG = "#FFFFFF"
CARD_BORDER = "#E5DDF3"

TITLE_COLOR = "#5E2D91"
SUBTLE = "#7B3FB3"

INPUT_BG = "#F2ECFA"
INPUT_FG = "#3B215A"
INPUT_PLACEHOLDER = "#9A9AAA"

BTN_BG = "#C21875"
BTN_BG_HOVER = "#A31563"
BTN_FG = "#FFFFFF"

LINK = "#6C63FF"
ERROR = "#C0392B"

REMEMBER_FILE = "remember_me.json"


def _get_logo_path():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    p1 = os.path.join(base_dir, "logo.png")
    if os.path.exists(p1):
        return p1


    p2 = os.path.join(base_dir, "..", "img", "logo_clinica_dental.png")
    if os.path.exists(p2):
        return p2

    return None


def _load_remembered_user():
    try:
        if os.path.exists(REMEMBER_FILE):
            with open(REMEMBER_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("username", "")
    except Exception:
        pass
    return ""


def _save_remembered_user(username: str, enabled: bool):
    try:
        if enabled:
            with open(REMEMBER_FILE, "w", encoding="utf-8") as f:
                json.dump({"username": username}, f, ensure_ascii=False, indent=2)
        else:
            if os.path.exists(REMEMBER_FILE):
                os.remove(REMEMBER_FILE)
    except Exception:
        pass


def _add_placeholder(entry: tk.Entry, placeholder: str, is_password=False):
    def set_placeholder():
        entry.delete(0, tk.END)
        entry.insert(0, placeholder)
        entry.config(fg=INPUT_PLACEHOLDER)
        if is_password:
            entry.config(show="")

    def on_focus_in(_):
        if entry.get() == placeholder and entry.cget("fg") == INPUT_PLACEHOLDER:
            entry.delete(0, tk.END)
            entry.config(fg=INPUT_FG)
            if is_password:
                entry.config(show="*")

    def on_focus_out(_):
        if not entry.get().strip():
            set_placeholder()

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)
    set_placeholder()


def _is_placeholder(entry: tk.Entry, placeholder: str):
    return entry.get() == placeholder and entry.cget("fg") == INPUT_PLACEHOLDER


def add_hover(btn: tk.Button, normal_bg: str, hover_bg: str):
    btn.bind("<Enter>", lambda e: btn.config(bg=hover_bg))
    btn.bind("<Leave>", lambda e: btn.config(bg=normal_bg))


def fade_in(win: tk.Tk, step=0.05, delay=10):
    try:
        win.attributes("-alpha", 0.0)
    except Exception:
        return

    def _up(a=0.0):
        a = a + step
        if a >= 1.0:
            try:
                win.attributes("-alpha", 1.0)
            except Exception:
                pass
            return
        try:
            win.attributes("-alpha", a)
        except Exception:
            return
        win.after(delay, _up, a)

    _up()


def login(root):
    ventana = root
    ventana.title("Login - Clínica Dental")
    ventana.configure(bg=BG)

    ventana.state("zoomed")   # Windows
    ventana.minsize(600, 450)
    ventana.resizable(True, True)

    for w in ventana.winfo_children():
        w.destroy()

    def cerrar_app():
        ventana.destroy()

    ventana.protocol("WM_DELETE_WINDOW", cerrar_app)

    container = tk.Frame(ventana, bg=BG)
    container.pack(fill="both", expand=True)

    container.grid_rowconfigure(0, weight=1)
    container.grid_rowconfigure(2, weight=1)
    container.grid_columnconfigure(0, weight=1)
    container.grid_columnconfigure(2, weight=1)

    card = tk.Frame(container, bg=CARD_BG, highlightthickness=1, highlightbackground=CARD_BORDER)
    card.grid(row=1, column=1, sticky="nsew")
    card.pack_propagate(False)

    def resize_card(event):
        w = max(360, min(560, int(event.width * 0.45)))
        h = max(320, min(420, int(event.height * 0.65)))
        card.config(width=w, height=h)

    container.bind("<Configure>", resize_card)

    # ===== LOGO PEQUEÑO EN ESQUINA (NO ESTORBA) =====
    logo_img = None
    logo_path = _get_logo_path()

    if logo_path:
        try:
            img = Image.open(logo_path)

            # ✅ TAMAÑO MÁXIMO DEL LOGO (ajusta aquí si quieres)
            img.thumbnail((120, 90))

            logo_img = ImageTk.PhotoImage(img)

            # Lo colocamos en la esquina superior izquierda del card
            lbl_logo = tk.Label(card, image=logo_img, bg=CARD_BG)
            lbl_logo.image = logo_img
            lbl_logo.place(x=14, y=12)  # ✅ esquina

        except Exception as e:
            print("Error cargando logo:", e)

    # ===== contenido del card =====
    tk.Label(card, text="LOGIN", bg=CARD_BG, fg=TITLE_COLOR, font=("Arial", 18, "bold")).pack(
        pady=(34, 18)  # deja espacio arriba por el logo en esquina
    )

    body = tk.Frame(card, bg=CARD_BG)
    body.pack(padx=50, fill="x")

    entry_user = tk.Entry(body, bd=0, bg=INPUT_BG, fg=INPUT_FG, font=("Arial", 11))
    entry_user.pack(fill="x", ipady=10)
    _add_placeholder(entry_user, "Username")

    tk.Frame(body, height=14, bg=CARD_BG).pack()

    mostrar = {"on": False}

    def toggle_password():
        if _is_placeholder(entry_pwd, "Password"):
            return
        mostrar["on"] = not mostrar["on"]
        entry_pwd.config(show="" if mostrar["on"] else "*")

    pwd_wrap = tk.Frame(body, bg=CARD_BG)
    pwd_wrap.pack(fill="x")

    entry_pwd = tk.Entry(pwd_wrap, bd=0, bg=INPUT_BG, fg=INPUT_FG, font=("Arial", 11))
    entry_pwd.pack(side="left", fill="x", expand=True, ipady=10)

    btn_eye = tk.Button(
        pwd_wrap, text="👁",
        bg=INPUT_BG, fg=SUBTLE,
        bd=0, cursor="hand2",
        command=toggle_password
    )
    btn_eye.pack(side="right", ipadx=10, ipady=6)

    _add_placeholder(entry_pwd, "Password", is_password=True)

    row = tk.Frame(body, bg=CARD_BG)
    row.pack(fill="x", pady=(12, 0))

    remember_var = tk.BooleanVar(value=False)
    tk.Checkbutton(
        row, text="Remember me",
        variable=remember_var,
        bg=CARD_BG, fg=SUBTLE,
        activebackground=CARD_BG,
        activeforeground=SUBTLE,
        bd=0, font=("Arial", 9),
        cursor="hand2"
    ).pack(side="left")

    def recuperar(_=None):
        messagebox.showinfo("Recuperar contraseña", "Contacta con administración.")

    lbl_forgot = tk.Label(
        row, text="Forgot?",
        bg=CARD_BG, fg=LINK,
        font=("Arial", 9, "underline"),
        cursor="hand2"
    )
    lbl_forgot.pack(side="right")
    lbl_forgot.bind("<Button-1>", recuperar)

    lbl_error = tk.Label(body, text="", bg=CARD_BG, fg=ERROR, font=("Arial", 9, "bold"))
    lbl_error.pack(pady=(10, 0))

    def ingresar():
        usuario = "" if _is_placeholder(entry_user, "Username") else entry_user.get().strip()
        pwd = "" if _is_placeholder(entry_pwd, "Password") else entry_pwd.get().strip()

        if not usuario or not pwd:
            lbl_error.config(text="Complete todos los campos.")
            return

        datos = autenticar(usuario, pwd)
        if datos:
            _, nombre, rol = datos
            lbl_error.config(text="")
            _save_remembered_user(usuario, remember_var.get())

            messagebox.showinfo("Acceso", f"Bienvenido {nombre}\nRol: {rol}")
            ventana.withdraw()
            menu_principal(ventana, rol)
        else:
            lbl_error.config(text="Credenciales incorrectas.")

    btn_login = tk.Button(
        card, text="LOGIN",
        bg=BTN_BG, fg=BTN_FG,
        bd=0, font=("Arial", 10, "bold"),
        cursor="hand2",
        activebackground=BTN_BG_HOVER,
        activeforeground=BTN_FG,
        command=ingresar
    )
    btn_login.pack(pady=(18, 0), ipadx=35, ipady=10)

    add_hover(btn_login, BTN_BG, BTN_BG_HOVER)

    remembered = _load_remembered_user()
    if remembered:
        remember_var.set(True)
        entry_user.config(fg=INPUT_FG)
        entry_user.delete(0, tk.END)
        entry_user.insert(0, remembered)

    ventana.bind("<Return>", lambda e: ingresar())
    entry_user.focus_set()

    fade_in(ventana, step=0.06, delay=10)


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

    ventana = tk.Toplevel(root)
    ventana.title("Menú Principal")
    ventana.geometry("300x250")
    ventana.configure(bg=BG)
    ventana.resizable(False, False)

    tk.Label(ventana, text=f"Rol: {rol}", font=("Arial", 12, "bold"), bg=BG, fg=TITLE_COLOR).pack(pady=12)

    def ejecutar():
        messagebox.showinfo("Ejecutar", "Función en desarrollo")

    tk.Button(ventana, text="▶ Ejecutar", command=ejecutar).pack(pady=6)

    if rol == "Usuario":
        tk.Label(ventana, text="Acceso de usuario", bg=BG, fg=SUBTLE).pack(pady=6)
        tk.Button(ventana, text="Salir", command=cerrar_app).pack(pady=6)

    ventana.protocol("WM_DELETE_WINDOW", cerrar_app)


if __name__ == "__main__":
    root = tk.Tk()
    login(root)
    root.mainloop()
