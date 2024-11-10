# Código encargado de gestionar las tablas y ciertas consultas a la base de datos (No todas), también crea las tablas una sola vez para que estén en la base de datos
# Posdata: Este código, aún con su corta longitud, proporcionalmente es el que más cambios ha sufrido porque hemos cambiado mucho las tablas de la base de datos

# Todos los imports necesarios para el buen funcionamiento del programa
from sqlalchemy import create_engine, Column, Float, Integer, String, Date, Time
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import declarative_base 
from datetime import datetime
import psycopg2

# Un try/except por los problemas que causó psycopg2
try:
    import psycopg2
    print("Psycopg2 esta instalado")
except ImportError:
    print(ImportError)
    print("Psycopg2 no esta instalado")

# Configurar la conexión a la base de datos PostgreSQL
DATABASE_URL = "postgresql://benat:12345678@localhost/elrincondelaliga?port=5432"
engine = create_engine(DATABASE_URL)

# Crear una sesión para interactuar con la base de datos
sesion = sessionmaker(bind=engine)
def abrir_sesion():
    return sesion()
3
def cerrar_sesion(sesion):
    # Cerrar la sesión al terminar
    sesion.close()

class miCRUD:
    def create(self, sesion):
        sesion.add(self)
        sesion.commit()

    @classmethod
    def readAlgunos(cls, sesion, **consulta):
        return sesion.query(cls).filter_by(**consulta).all() #devuelve una lista de objetos
    def read(cls, sesion):
        return sesion.query(cls).all()
    def update(self,sesion):
        sesion.commit()
    def delete(self, sesion):
        sesion.delete(self)
        sesion.commit()

Base = declarative_base()

class enVivo(Base, miCRUD):
    __tablename__ = 'envivo'
    id = Column(Integer, primary_key=True)
    minactual = Column(Integer)
    eq1 = Column(String)
    eq2 = Column(String)
    goleseq1 = Column(Integer)
    goleseq2 = Column(Integer)
    matchday = Column(String)
    mipartido = Column(String)

class Usuarios(Base, miCRUD):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    email = Column(String)
    passwd = Column(String)

class ResTerminados(Base, miCRUD):
    __tablename__ = 'resterminados'
    id = Column(Integer, primary_key=True)
    eq1 = Column(String)
    eq2 = Column(String)
    reseq1 = Column(Integer)
    reseq2 = Column(Integer)
    horainicio = Column(Time) 
    dia = Column(Date)
    matchday = Column(String)
    mipartido = Column(String)

class escribeRes(Base, miCRUD):
    __tablename__ = 'escriberes'
    id = Column(Integer, primary_key=True)
    idusuario = Column(Integer, ForeignKey('usuarios.id'))
    usuario = relationship('Usuarios', backref='escribeRes')
    nombreusuario = Column(String)
    comentario = Column(String)

class evFuturos(Base, miCRUD):
    __tablename__ = 'evfuturos'
    id = Column(Integer, primary_key=True)
    eq1 = Column(String)
    eq2 = Column(String)
    horainicio = Column(Time) 
    dia = Column(Date)
    matchday = Column(String)
    mipartido = Column(String)
# Crear la tabla en la base de datos (esto solo se hace una vez)
# Base.metadata.create_all(engine)
