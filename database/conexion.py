import sqlite3

def conectar():
    conn = sqlite3.connect("odontologia.db")
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
