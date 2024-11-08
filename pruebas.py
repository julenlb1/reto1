import modelos
from modelos import ResTerminados
from collections import OrderedDict
sesion = modelos.abrir_sesion() # Abro la sesión de queries
juegos = sesion.query(ResTerminados).order_by(ResTerminados.matchday.desc(), ResTerminados.dia.desc()).all()
datosJerarquizados = OrderedDict()

for juego in juegos:
    if juego.matchday not in datosJerarquizados:
        datosJerarquizados[juego.matchday] = OrderedDict()
    if juego.dia not in datosJerarquizados[juego.matchday]:
        datosJerarquizados[juego.matchday][juego.dia] = []
    datosJerarquizados[juego.matchday][juego.dia].append(juego)
print(datosJerarquizados)
modelos.cerrar_sesion(sesion)
sesion = None
    
    