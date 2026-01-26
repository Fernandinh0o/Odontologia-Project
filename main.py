import tkinter as tk

from interfaz.usuarios_controlador import iniciar_sistema
from interfaz.usuarios_vista import login


def main(root):
    iniciar_sistema()
    login(root)


if __name__ == "__main__":
    root = tk.Tk()
    main(root)
    root.mainloop()
