from sqlalchemy.orm import Session
from typing import List, Optional
import models
import schemas
import auth

#Optional[models.Usuario] es una anotación de tipo que especifica que la función puede devolver dos posibles resultados: un objeto de tipo Usuario (si se encuentra en la base de datos) o el valor None (si el correo electrónico no existe).Su propósito fundamental es la prevención de errores   esto de evitar errores no deberia aplicarse a los que no tienen optonial por que ya sabes que no pueden devolver none.


def get_user_by_email(db: Session, email: str) -> Optional[models.Usuario]:
    return db.query(models.Usuario).filter(models.Usuario.correo == email).first() # 1 se ubica en la  tabla  usarios 
#2 despues que se ubica usalmos el filtrador y busca en la tabla usarios en la seccion correo  y filtrado se pone la condicion y por ultimo el comando first lo agarra y regresa por el retur

def get_user_by_id(db: Session, user_id: int) -> Optional[models.Usuario]:
    return db.query(models.Usuario).filter(models.Usuario.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.Usuario]:
    return db.query(models.Usuario).offset(skip).limit(limit).all()

def search_users_by_name(db: Session, nombre: str) -> List[models.Usuario]:
    return db.query(models.Usuario).filter(models.Usuario.nombre.contains(nombre)).all()

def create_user(db: Session, usuario: schemas.UsuarioCreate) -> models.Usuario:
    hashed_password = auth.hash_password(usuario.contraseña)
    db_user = models.Usuario(**usuario.model_dump(exclude={"contraseña"}),
    contraseña=hashed_password
        
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, usuario_update: schemas.UsuarioUpdate) -> Optional[models.Usuario]:
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None
    update_data = usuario_update.model_dump(exclude_unset=True)
    if "contraseña" in update_data:
        update_data["contraseña"] = auth.hash_password(update_data["contraseña"])
    for key, value in update_data.items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int) -> bool:
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return False
    db.delete(db_user)
    db.commit()
    return True

def queryletra(nombre1 : str | None , tunel : Session) -> list[models.Usuario]:
    query = tunel.query(models.Usuario)
    if nombre1:
        queryf2 = query.filter(models.Usuario.nombre.ilike(f"%{nombre1}%"))
    else:
        queryf2 =query
    return queryf2.all()
    



# crud de tarea 
     
def crear_tarea_usuario(db: Session, tarea: schemas.tarea_clit, usuario_id: int):
    # Convertimos el esquema a diccionario y añadimos la clave foránea del usuario
    nueva_tarea = models.Tarea(**tarea.model_dump(), usuario_id=usuario_id)
    db.add(nueva_tarea)
    db.commit()
    db.refresh(nueva_tarea)
    return nueva_tarea