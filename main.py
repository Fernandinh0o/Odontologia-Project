import tkinter as tk
from modulos.users.usuarios_controlador import iniciar_sistema
from modulos.users.usuarios_vista import login

def main():
    iniciar_sistema()
    login()

root = tk.Tk()
root.withdraw()

main()
root.mainloop()
