from gestores.usuarios_gestor import (
    crear_usuario,
    eliminar_usuario,
    inicializar_bd,
    login,
    obtener_usuarios,
)
from database.tablas import crear_tablas_iniciales
from modelos.usuario import Usuario


def iniciar_sistema():
    crear_tablas_iniciales()
    inicializar_bd()


def registrar_usuario(datos):
    usuario = Usuario(
        nombre=datos["nombre"],
        telefono=datos["telefono"],
        rol=datos["rol"],
        contrasena=datos["contrasena"],
        especialidad=datos.get("especialidad"),
    )
    crear_usuario(usuario)


def autenticar(nombre, contrasena):
    return login(nombre, contrasena)


def listar_usuarios():
    return obtener_usuarios()


def borrar_usuario(id_usuario):
    eliminar_usuario(id_usuario)