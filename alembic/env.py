from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
import sys
import os

# 1. Subimos a la raíz del proyecto para asegurar portabilidad en cualquier entorno
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# 2. Importaciones absolutas base
# PASO 1: Aquí importamos "SQLALCHEMY_DATABASE_URL" directamente de tu archivo database.py
from servcio.database import Base, SQLALCHEMY_DATABASE_URL

# NOTA PROFESIONAL: Para evitar líneas de "fuerza" individuales, asegúrese de que 
# su archivo servcio/models/__init__.py importe todos sus modelos (Usuario, etc.).
# Al hacer este import general, registramos todo el catálogo de golpe de forma limpia.
import servcio.models

config = context.config

# PASO 2: Esta línea toma el objeto de configuración de Alembic y le introduce a la fuerza
# la URL que importamos de tu database.py, rellenando el marcador vacío de alembic.ini.
config.set_main_option("sqlalchemy.url", SQLALCHEMY_DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 3. Asignamos la metadata unificada oficial
target_metadata = Base.metadata

# 🔍 LÍNEA DE CONTROL (Ahora colocada después de asegurar la carga de modelos)
print("\n==================================================")
print(f"TABLAS DETECTADAS POR ALEMBIC (RUTAS CORREGIDAS): {list(target_metadata.tables.keys())}")
print("==================================================\n")


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    # PASO 3: Al ejecutar de forma offline, este método extraerá la URL que inyectamos
    # en el Paso 2, garantizando que use siempre la misma ruta de FastAPI.
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    # Este método crea la conexión física con la base de datos utilizando la sección
    # de configuración que modificamos dinámicamente con tu URL de Python.
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()