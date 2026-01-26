from dataclasses import dataclass
from typing import Optional


@dataclass
class Usuario:
    nombre: str
    telefono: Optional[str]
    rol: str
    contrasena: str
    especialidad: Optional[str] = None
    id_usuario: Optional[int] = None
