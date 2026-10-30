from pydantic import BaseModel, field_validator
from typing import Optional,List

class UsuarioBase(BaseModel):
    nombre: str
    correo: str
    rol: Optional[str] = "usuario"  # 🔥 Rol por defecto
    
    @field_validator('correo')
    @classmethod
    def dominio_institucional(cls, valor: str):
        if "@empresa.com" not in valor:
            raise ValueError("Solo se permiten correos institucionales")
        return valor

class UsuarioCreate(UsuarioBase):
    contraseña: str

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    correo: Optional[str] = None
    contraseña: Optional[str] = None
    rol: Optional[str] = None  # 🔥 Permitir actualizar rol

    @field_validator('correo')
    @classmethod
    def dominio_institucional(cls, valor: str):
        if valor is not None and "@empresa.com" not in valor:
            raise ValueError("Solo se permiten correos institucionales")
        return valor

class Usuario(UsuarioBase):
    id: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    correo: Optional[str] = None
    


#aqui empiesa el scheemes  de tareas 
# Esquema base con los atributos esenciales de una tarea
class tareas(BaseModel):
    titulo: str
    descripcion: Optional[str] = None

# Esquema para la creación de tareas por parte del cliente
class tarea_clit(tareas):
    pass

# Esquema para devolver los datos de la tarea, incluyendo identificadores y mapeo de SQLAlchemy
class tarea_response(tareas):
    id: int
    usuario_id: int

    class Config:
        from_attributes = True

# Esquema que extiende el perfil del usuario para incluir su lista de tareas asociadas
class UsuarioConTareas(Usuario):
    tareas: List[tarea_response] = []

    class Config:
        from_attributes = True
    
