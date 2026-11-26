from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
import base64


def generar_clave_publica_privada():
    privada = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048)
    publica = privada.public_key()
    
    return publica, privada

def serializar_clave_publica(publica):
    der_data = publica.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    claveprimaria_b64 = base64.b64encode(der_data).decode()
    return claveprimaria_b64

def autenticacion_estacion(estacion_id, credencial):
    c_publica, c_privada = generar_clave_publica_privada()
    clave_publicab64 = serializar_clave_publica(c_publica)
    trama = f"REGISTRO#{estacion_id}#{credencial}#{clave_publicab64}"
    return trama, c_privada

def descencriptar_clave_sesion(privada, clave_Sesionb64):
    clave_Sesion_Cifrada = base64.b64decode(clave_Sesionb64)
    mensaje_descifrado = privada.decrypt(
        clave_Sesion_Cifrada,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    return mensaje_descifrado