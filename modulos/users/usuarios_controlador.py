import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

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

from modulos.users.usuarios_modelo import obtener_usuarios, eliminar_usuario

def listar_usuarios():
    return obtener_usuarios()

def borrar_usuario(id_usuario):
    eliminar_usuario(id_usuario)
