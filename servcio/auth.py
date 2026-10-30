from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
import models, schemas
from database import get_db

SECRET_KEY = "tu_clave_secreta_super_segura"
ALGORITHM = "HS256"
EXPIRE_MINUTES = 30

pwd_context_ash = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/usuarios/login") # Ajustado para coincidir con tu prefijo

def hash_password(password: str) -> str:
    return pwd_context_ash.hash(password)

def verificar_password(password_plana: str, password_hasheada: str) -> bool:
    return pwd_context_ash.verify(password_plana, password_hasheada)

def crear_token_acceso(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy() # se hace una copia por que el dato es como  anclada a la base de datos y es moejo no tocarla
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def obtener_usuario_actual(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    excepcion_credenciales = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        correo: str = payload.get("sub")
        if correo is None:
            raise excepcion_credenciales
        token_data = schemas.TokenData(correo=correo)
    except JWTError: 
        raise excepcion_credenciales
        # el try se usa para manejar situaciones donde sabes de antemano que algo puede salir mal, pero el resultado no depende únicamente de la lógica de tu código, sino de factores externos
    usuario = db.query(models.Usuario).filter(models.Usuario.correo == token_data.correo).first()
    if usuario is None:
        raise excepcion_credenciales
    return usuario

class VerificadorRol:
    def __init__(self, roles_permitidos: list[str]):
        self.roles_permitidos = roles_permitidos

    def __call__(self, usuario_actual: models.Usuario = Depends(obtener_usuario_actual)):
        if usuario_actual.rol not in self.roles_permitidos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes los permisos necesarios para realizar esta acción."
            )
        return usuario_actual
    
    

    
         
         
                                
            
                
    
            
        
    
         

     

    
    
