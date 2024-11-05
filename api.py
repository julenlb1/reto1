## Este codigo se ejecutará cada cierto tiempo para actualizar las tablas de partidos futuros cuando dichos partidos ya se hayan disputado y moverá esos datos de la tabla de 
# evFuturos a la de ResTerminados, además de poner un evento en vivo si un partido se está disputando 

from sqlalchemy import create_engine, Column, Float, Integer, String, Date, Time
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import declarative_base 
import requests
import psycopg2
from datetime import datetime
from datetime import date
from datetime import timedelta
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

hoy = date.today()
ahora = datetime.now()


terminar = ahora + timedelta(minutes=90) 

# URL de la API de fútbol para obtener datos de partidos
url = "https://raw.githubusercontent.com/openfootball/football.json/refs/heads/master/2024-25/es.1.json"

# Realiza una solicitud GET a la API y abre la sesión de queries sql
response = requests.get(url)
sesion = abrir_sesion()

# Aparte de hacer un fetch asíncrono a la api, utiliza esos datos para insertarlos en la BBDD
if response.status_code == 200:
    data = response.json()

    i = 0
    for match in data["matches"]:
        
        match_date = match["date"] # La fecha del partido de json
        print(f"{match} ola")
        match_time = match["time"] # La hora del partido de json
        match_datetime_str = f"{match_date} {match_time}" # Uniendo las dos para hacer un datetime
        match_datetime = datetime.strptime(match_datetime_str, "%Y-%m-%d %H:%M") # Formateo a datetime

        if match_datetime.date() < hoy: # Si el dia del json es menor al actual, insertará los datos en la tabla de ResTerminados
            esmipartido = sesion.query(modelos.ResTerminados).filter_by(id=i,mipartido="false").all() # Esta consulta comprueba si el partido que va actualizar no esta en la tabla y no ha sido creado por el usuario
            if esmipartido == "":
                # Partidos terminados
                resterminado = modelos.ResTerminados()
                resterminado.id = i
                if "ft" in match.get("score", {}):
                    resterminado.reseq1 = match["score"]["ft"][0]
                    resterminado.reseq2 = match["score"]["ft"][1]
                resterminado.eq1 = match["team1"]
                resterminado.eq2 = match["team2"]
                resterminado.horainicio = match_datetime.time()
                resterminado.dia = match_date
                resterminado.matchday = match["round"]
                resterminado.mipartido = "false"
                sesion.add(resterminado)
        elif match_datetime.date() == hoy: # Si el dia es el mismo, los insertará en enVivo
            esmipartido = sesion.query(modelos.enVivo).filter_by(id=i,mipartido="false").all()
            if esmipartido == "":
                # Partidos en vivo
                envivo = modelos.enVivo()
                envivo.id = i
                envivo.eq1 = match["team1"]
                envivo.eq2 = match["team2"]
                envivo.goleseq1 = 0
                envivo.goleseq2 = 0
                envivo.minactual = 0
                envivo.matchday = match["round"]
                envivo.mipartido = "false"
                sesion.add(envivo)

        else: # Si no, los insertará en evFuturos
            esmipartido = sesion.query(modelos.evFuturos).filter_by(id=i,mipartido="false").all()
            if esmipartido == "":
                # Partidos futuros
                evFuturo = modelos.evFuturos()
                evFuturo.id = i
                evFuturo.eq1 = match["team1"]
                evFuturo.eq2 = match["team2"]
                evFuturo.matchday = match["round"]
                evFuturo.dia = match_date
                evFuturo.horainicio = match_datetime.time()
                evFuturo.mipartido = "false"
                sesion.commit()
        i += 1
    sesion.commit()
else:
    print(f"Error en la solicitud. Código de respuesta: {response.status_code}")


cerrar_sesion(sesion)
sesion = None