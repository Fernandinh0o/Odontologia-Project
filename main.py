import tkinter as tk

from interfaz.usuarios_controlador import iniciar_sistema #Crea, inicializa y deja listo el sistemaw
from interfaz.usuarios_vista import login   #Importa la pantalla inicial del programa


def main(root): #CVentana raiz 
    iniciar_sistema() #Llama al controlador. que crea tabalas e inicializa la base de datos.
    login(root) #Centana del login-


if __name__ == "__main__":
    root = tk.Tk()  #Ventana base
    main(root)
    root.mainloop()
