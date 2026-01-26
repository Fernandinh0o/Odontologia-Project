import tkinter as tk
from modulos.users.usuarios_controlador import iniciar_sistema
from modulos.users.usuarios_vista import login

def main(root):
    iniciar_sistema()
    login(root)


root = tk.Tk()
main(root)
root.mainloop()
