from sqlalchemy import create_engine, Column, Float, Integer, String, Date, Time
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import declarative_base 
from datetime import datetime
import psycopg2
# Configurar la conexión a la base de datos PostgreSQL
# engine = create_engine('postgresql://usuario:contraseña@localhost/nombre_de_la_bd')

try:
    import psycopg2
    print("Psycopg2 is installed")
except ImportError:
    print(ImportError)
    print("Psycopg2 is not installed")

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
        #return sesion.query(cls).all()
    def readJornadas(cls, sesion, **consulta):
        return sesion.query(cls).group_by(**consulta).all()
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

class Noticias(Base):
    __tablename__ = 'noticias'
    id = Column(Integer, primary_key=True)
    nombrenot = Column(String)
    cuerponot = Column(String)
    Likes = Column(Integer)

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
class escribeNot(Base):
    __tablename__ = 'escribenot'
    id = Column(Integer, primary_key=True)
    idusuario = Column(Integer, ForeignKey('usuarios.id'))
    usuario = relationship('Usuarios', backref='escribeNot')
    nombreusuario = Column(String)
    comentario = Column(String)
    likes = Column(Integer)

class escribeRes(Base):
    __tablename__ = 'escriberes'
    id = Column(Integer, primary_key=True)
    idusuario = Column(Integer, ForeignKey('usuarios.id'))
    usuario = relationship('Usuarios', backref='escribeRes')
    nombreusuario = Column(String)
    comentario = Column(String)
    likes = Column(Integer)

class evFuturos(Base, miCRUD):
    __tablename__ = 'evfuturos'
    id = Column(Integer, primary_key=True)
    eq1 = Column(String)
    eq2 = Column(String)
    horainicio = Column(Time) 
    dia = Column(Date)
    matchday = Column(String)
    mipartido = Column(String)
# Crear la tabla en la base de datos (esto solo se hace una vez)"""
# Base.metadata.create_all(engine)

# Ejemplos de uso:


'''# crear 3 productos
for i in range(1,4):
    # crear una nueva instancia de Producto en cada iteración del bucle, de modo que cada instancia tenga su propio valor de id
    product = Producto()
    product.producto = f"Producto{i}"
    product.modelo = f"Modelo{i}"
    product.precio = 90-4*i
    product.create(sesion)  # Crear un nuevo producto

# crear un producto de otra manera:
product = Producto(producto='Producto4', modelo='Modelo4', precio=99.55)
product.create(sesion)  # Crear un nuevo producto
'''


'''
sesion = abrir_sesion()
# Leer un producto por ID
consulta = {"id": 2}
product = Producto.read(sesion,**consulta)[0]
print(product.producto, product.modelo, product.precio)

# Actualizar el producto encontrado (id=2)
product.producto = 'NuevoProducto2'
product.update(sesion)

# Borrar el producto con id=3
consulta = {"id": 3}
product = Producto.read(sesion, **consulta)[0]
product.delete(sesion)

cerrar_sesion(sesion)
sesion = None'''
