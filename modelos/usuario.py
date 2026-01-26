from dataclasses import dataclass
""""Aqui se van a importar un metodo el cual crea los init de manera automatica"""
from typing import Optional
""""Permite que haya datos opcionales en blanco"""

@dataclass
class Usuario:
    nombre: str
    telefono: Optional[str]
    rol: str
    contrasena: str
    especialidad: Optional[str] = None
    id_usuario: Optional[int] = None

"""" Esta clase se ve utilizada generalmente por los usuarios, el gestor y el controlador 
solo que no guarda especificamente solo es para definir datos"""