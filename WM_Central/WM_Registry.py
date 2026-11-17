from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
import os
import secrets
import bd
import bcrypt

app = FastAPI(
    title = "API de registro",
    version = "0.1.0"
)

DB_PATH = os.getenv("DB_PATH", "registry.db")

class Estacion(BaseModel):
    id: str
    ubicacion: str
    direccion: str

class RespuestaAlta(BaseModel):
    id: str
    credencial: str

def hashear_credencial(credencial: str):
    sal = bcrypt.gensalt()
    credencial_hasheada = bcrypt.hashpw(credencial.encode(), sal).decode()
    return credencial_hasheada

@app.get('/')
def inicio():
    return {"message": "Validación de las estaciones de riego"}

@app.get("/estaciones/{estacion_id}")
def get_estacion(estacion_id: str) -> Estacion:
    estacion = bd.obtener_estacion(estacion_id)
    if estacion is None:
        raise HTTPException(status_code=404, detail="La id de la estación no existe")
    return estacion

@app.post("/estaciones/", status_code=201)
def registrar_estacion(estacion: Estacion) -> RespuestaAlta:
    credencial = secrets.token_urlsafe(32)
    credencial_hasheada = hashear_credencial(credencial)
    guardado_ok = bd.guardar_estacion(estacion.id, estacion.ubicacion, estacion.direccion, credencial_hasheada)
    
    if not guardado_ok:
        raise HTTPException(status_code=409, detail="La id de la estación ya existe")
    return {"id": estacion.id, "credencial": credencial}

@app.delete("/estaciones/{estacion_id}")
def eliminar_estacion(estacion_id: str, x_credencial: str = Header(...)):
    credencial_obtenido = bd.obtener_credencial(estacion_id)
    
    if credencial_obtenido is None:
        raise HTTPException(status_code=404, detail="La id de la estación no existe")
    if not bcrypt.checkpw(x_credencial.encode() ,credencial_obtenido.encode()):
        raise HTTPException(status_code=401, detail="La credencial no coincide")
    bd.borrar_estacion(estacion_id)
    
    return {"message": "Estación eliminada", "id": estacion_id}

@app.post("/estaciones/{estacion_id}/autenticar")
def autenticar_estacion(estacion_id: str, x_credencial: str = Header(...)):
    credencial_hasheada = bd.obtener_credencial(estacion_id)
    
    if credencial_hasheada is None:
        raise HTTPException(status_code=404, detail="La id de la estación no existe")
    if not bcrypt.checkpw(x_credencial.encode(), credencial_hasheada.encode()):
        raise HTTPException(status_code=401, detail="Las credenciales no coinciden")
    return {"id": estacion_id, "autenticacion": True}