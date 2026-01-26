from modulos.users.usuarios_modelo import (
    inicializar_bd,
    crear_usuario,
    login
)

def iniciar_sistema():
    inicializar_bd()

def registrar_usuario(datos):
    crear_usuario(
        datos["nombre"],
        datos["telefono"],
        datos["rol"],
        datos["contrasena"],
        datos.get("especialidad")
    )

def autenticar(nombre, contrasena):
    return login(nombre, contrasena)
