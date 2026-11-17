import os
import sqlite3

DB_PATH = os.getenv("DB_PATH", "../data/WM.db")

def guardar_estacion(id_estacion, ubicacion, direccion, credencial):
    conexion = sqlite3.connect(DB_PATH)

    try:
        conexion.execute(
            "INSERT INTO aspersores (id, estado, ubicacion, direccion, credencial_hash)"
            "VALUES (?, 'DESCONECTADA', ?, ?, ?)",
            (id_estacion, ubicacion, direccion, credencial))
        
        conexion.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conexion.close()

def obtener_estacion(id_estacion):
    conexion = sqlite3.connect(DB_PATH)
    
    fila = conexion.execute("SELECT id, ubicacion, direccion FROM aspersores"
                            " WHERE id = ? AND credencial_hash IS NOT NULL", (id_estacion,)).fetchone()
    conexion.close()
    if fila is None:
        return None

    return {"id": fila[0], "ubicacion": fila[1], "direccion": fila[2]}

def obtener_credencial(id_estacion):
    conexion = sqlite3.connect(DB_PATH)
    
    fila = conexion.execute("SELECT credencial_hash FROM aspersores WHERE id = ?", (id_estacion,)).fetchone()
    conexion.close()
    
    if fila is None:
        return None
    
    return fila[0]

def borrar_estacion(id_estacion):
    conexion = sqlite3.connect(DB_PATH)
    
    conexion.execute("DELETE FROM aspersores WHERE id = ?", (id_estacion,))
    conexion.commit()
    conexion.close()