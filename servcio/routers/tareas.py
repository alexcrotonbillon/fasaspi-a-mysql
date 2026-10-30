from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import crud, schemas, models, auth
from database import get_db

router = APIRouter(prefix="/tareas", tags=["Tareas"])

@router.post("/crear", response_model=schemas.tarea_response, status_code=status.HTTP_201_CREATED)
def crear_tarea(
    tarea: schemas.tarea_clit,db: Session = Depends(get_db),usuario_actual: models.Usuario = Depends(auth.obtener_usuario_actual)):
    # La tarea se asigna automáticamente al usuario autenticado
    return crud.crear_tarea_usuario(db=db, tarea=tarea, usuario_id=usuario_actual.id)