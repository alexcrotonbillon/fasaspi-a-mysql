from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
import auth
import crud                    
from database import get_db

router = APIRouter(prefix="/usuarios", tags=["usuario"])        

@router.get("/letra",response_model= list[schemas.Usuario],tags=["prueba"])
def prueba_query(nombre : str | None = None , tunel : Session = Depends(get_db)):
    letra = crud.queryletra (nombre ,tunel)
    if not letra:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail= "no se encontro nigunga considencia")
    return letra


@router.post("/login", response_model=schemas.Token, tags=["autenticacion"])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = crud.get_user_by_email(db, form_data.username)
    if not usuario or not auth.verificar_password(form_data.password, usuario.contraseña):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
    token = auth.crear_token_acceso(data={"sub": usuario.correo})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/registrar", response_model=schemas.Usuario, status_code=status.HTTP_201_CREATED, tags=["registrar"])
def registrar_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_email(db, usuario.correo):
        raise HTTPException(status_code=400, detail="El correo ya está registrado.")
    
    nuevo_usuario = crud.create_user(db, usuario)
    return nuevo_usuario

@router.get("/listas/", response_model=List[schemas.Usuario], tags=["busqueda"])
def obtener_usuarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), 
                     usuario_actual: models.Usuario = Depends(auth.VerificadorRol(["admin", "moderador"]))): 
    return crud.get_users(db, skip=skip, limit=limit)

@router.get("/id/{usuario_id}", response_model=schemas.Usuario, tags=["busqueda"])
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = crud.get_user_by_id(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.put("/actulaizar/{usuario_id}", response_model=schemas.Usuario, tags=["actualizar"])  
def actualizar_usuario(usuario_id: int, usuario_actualizado: schemas.UsuarioUpdate, db: Session = Depends(get_db),
                       usuario_actual: models.Usuario = Depends(auth.obtener_usuario_actual)):
    
    if usuario_actual.id != usuario_id and usuario_actual.rol != "admin":
        raise HTTPException(status_code=403, detail="No tienes permiso para actualizar este perfil.")

    usuario = crud.update_user(db, usuario_id, usuario_actualizado)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.delete("/borrar/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["borrar"])
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db),
                     usuario_actual: models.Usuario = Depends(auth.VerificadorRol(["admin"]))): 
    success = crud.delete_user(db, usuario_id)
    if not success:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return None

@router.get("/buscar/{nombre}", response_model=List[schemas.Usuario], tags=["busqueda"])
def buscar_usuario_por_nombre(nombre: str, db: Session = Depends(get_db),
                              usuario_actual: models.Usuario = Depends(auth.VerificadorRol(["admin", "moderador"]))): 
    usuarios = crud.search_users_by_name(db, nombre)
    if not usuarios:
        raise HTTPException(status_code=404, detail="No se encontraron usuarios con ese nombre")
    return usuarios 


@router.get("/me", response_model=schemas.UsuarioConTareas, tags=["usuarios"])
def obtener_mi_perfil(
    db: Session = Depends(get_db), 
    usuario_actual: models.Usuario = Depends(auth.obtener_usuario_actual)
):
    return usuario_actual