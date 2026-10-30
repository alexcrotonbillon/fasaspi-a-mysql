from fastapi import FastAPI
# from database import engine, Base  <-- Ya no lo necesitamos
from routers import usuarios,tareas

# 🔥 NOTA: Comentamos esto porque ahora ALEMBIC controla la base de datos
# Base.metadata.create_all(bind=engine)

app = FastAPI(title="mi inicio", version="2.0")

app.include_router(usuarios.router)

app.include_router(tareas.router)