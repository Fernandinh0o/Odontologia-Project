from gestores.usuarios_gestor import (
    crear_usuario,
    eliminar_usuario,
    inicializar_bd,
    login,
    obtener_usuarios,
)
from database.tablas import crear_tablas_iniciales
from modelos.usuario import Usuario

""" Aqui se reciben los datos de la interfaz, llama al gestor y devuelvce los resultados, ademas como no usa sql
llama practicamente a funciones que si lo hacen todo lo primero practicamente"""

def iniciar_sistema():
    crear_tablas_iniciales()
    inicializar_bd()
#Aqui inicia el programa y garantiza las tablas.

def registrar_usuario(datos):
    usuario = Usuario(
        nombre=datos["nombre"],
        telefono=datos["telefono"],
        rol=datos["rol"],
        contrasena=datos["contrasena"],
        especialidad=datos.get("especialidad"),
    )
    crear_usuario(usuario)  #SAe guarda en la base ded atos


def autenticar(nombre, contrasena):
    return login(nombre, contrasena)


def listar_usuarios():
    return obtener_usuarios()


def borrar_usuario(id_usuario):
    eliminar_usuario(id_usuario)
