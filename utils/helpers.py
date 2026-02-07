import hashlib
import os


def _hash_with_salt(contrasena, salt):
    return hashlib.sha256((salt + contrasena).encode("utf-8")).hexdigest()


def hash_contrasena(contrasena):
    salt = os.urandom(16).hex()
    hashed = _hash_with_salt(contrasena, salt)
    return f"{salt}${hashed}"


def verificar_contrasena(contrasena, hash_guardado):
    try:
        salt, hashed = hash_guardado.split("$", 1)
    except ValueError:
        return False
    return _hash_with_salt(contrasena, salt) == hashed
