from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:MyNewPass1@127.0.0.1:3306/tiendamaker" #3

engine = create_engine(SQLALCHEMY_DATABASE_URL)#2
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)#1 el orden de dentro para afuera

Base = declarative_base() #libro de regestrio

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()