# primero instalar requests desde la consola
# conda install requests ; pip install requests
from sqlalchemy import create_engine, Column, Float, Integer, String, Date, Time
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import declarative_base 
import requests
import json
import psycopg2
from datetime import date

import modelos

DATABASE_URL = "postgresql://benat:12345678@localhost/elrincondelaliga?port=5432"
engine = create_engine(DATABASE_URL)

# Crear una sesión para interactuar con la base de datos
sesion = sessionmaker(bind=engine)
def abrir_sesion():
    return sesion()

def cerrar_sesion(sesion):
    # Cerrar la sesión al terminar
    sesion.close()
sesion = abrir_sesion()

hoy = date.today()
#ahora = x.strftime("%H")+":"+x.strftime("%M")
# URL de la API de JSONPlaceholder para obtener datos de usuarios
url = "https://raw.githubusercontent.com/openfootball/football.json/refs/heads/master/2024-25/es.1.json"

# Realiza una solicitud GET a la API
response = requests.get(url)

# Verifica si la solicitud fue exitosa (código de respuesta 200)
if response.status_code == 200:
    # Utiliza json.loads() para analizar la respuesta JSON
    #data = json.loads(response.text)
    data = response.json()
    i = 0
    while(i < len(data["matches"])):
        i+=1
        if data["matches"][i]["date"] <= str(hoy):
            resterminado = modelos.ResTerminados()
            resterminado.eq1 = data["matches"][i]["team1"]
            resterminado.eq2 = data["matches"][i]["team2"]
            resterminado.resEq1 = int(data["matches"][i]["score"]["ft"][0])
            resterminado.resEq2 = int(data["matches"][i]["score"]["ft"][1])
            resterminado.horaInicio = data["matches"][i]["date"]
            resterminado.dia = data["matches"][i]["date"]

        else:
            evFuturo = modelos.evFuturos()
            evFuturo.eq1 = data["matches"][i]["team1"]
            evFuturo.eq2 = data["matches"][i]["team2"]
            evFuturo.horaInicio = data["matches"][i]["date"]
            evFuturo.dia = data["matches"][i]["date"]

else:
    print(f"Error en la solicitud. Código de respuesta: {response.status_code}")

cerrar_sesion(sesion)
sesion = None