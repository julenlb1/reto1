from wsgiref.simple_server import make_server
from urllib.parse import parse_qs
import vistas
#import vistasEquipos
#import vistasNoticias
#import vistasPlantilla
import modelos
from modelos import ResTerminados
from modelos import enVivo
from modelos import evFuturos

def leerResTerminados(environ, start_response): # Función para hacer una query de la base de datos a la tabla de resultados terminados
                                                # y plasmar esos datos en el html mediante jinja
    sesion = modelos.abrir_sesion() # Abro la sesión de queries
    juegos = sesion.query(ResTerminados).order_by(ResTerminados.matchday.asc(), ResTerminados.dia.asc()).all() # Esta consulta obtendrá los datos con un orden jerárquico ordenado por matchday > dia > partido 
    datosJerarquizados = {} # Este diccionario guardara los datos en ese orden jerárquico                                                                          
    for juego in juegos:
        if juego.matchday not in datosJerarquizados:
            datosJerarquizados[juego.matchday] = {}
        if juego.dia not in datosJerarquizados[juego.matchday]:
            datosJerarquizados[juego.matchday][juego.dia] = []
        datosJerarquizados[juego.matchday][juego.dia].append(juego)
    modelos.cerrar_sesion(sesion)
    sesion = None
    return datosJerarquizados # Devolver el diccionario

def leerEnVivo(environ, start_response): # Función para hacer una query de la base de datos a la tabla de partidos en vivo
    sesion = modelos.abrir_sesion()      # y plasmar esos datos en el html mediante jinja
    directos = sesion.query(enVivo).order_by(enVivo.matchday.asc()).all()
    datosJerarquizadosDirecto = {}
    for directo in directos:
        if directo.matchday not in datosJerarquizadosDirecto:
            datosJerarquizadosDirecto[directo.matchday] = []
        datosJerarquizadosDirecto[directo.matchday].append(directo)
    modelos.cerrar_sesion(sesion)
    sesion = None
    return datosJerarquizadosDirecto

def leerCalendario(environ, start_response):# Función para hacer una query de la base de datos a la tabla de partidos por disputar
    sesion = modelos.abrir_sesion()         # y plasmar esos datos en el html mediante jinja   
    juegos = sesion.query(evFuturos).order_by(evFuturos.matchday.asc(), evFuturos.dia.asc()).all()
    datosJerarquizadosCalendario = {}
    for juego in juegos:
        if juego.matchday not in datosJerarquizadosCalendario:
            datosJerarquizadosCalendario[juego.matchday] = {}
        if juego.dia not in datosJerarquizadosCalendario[juego.matchday]:
            datosJerarquizadosCalendario[juego.matchday][juego.dia] = []
        datosJerarquizadosCalendario[juego.matchday][juego.dia].append(juego)
    modelos.cerrar_sesion(sesion)
    sesion = None
    return datosJerarquizadosCalendario

def ponerComentarioNot(environ, start_response):
    if environ['REQUEST_METHOD'] == 'POST':
        print("funcion ponerComentario()")
        try:
            size = int(environ.get('CONTENT_LENGTH', 0))
            data = environ['wsgi.input'].read(size).decode()
            paramsComentario = parse_qs(data)      
            
            if params['nombre'][0] == "" or params['email'][0] == "" or params['password'][0] == "" or params['password-2'][0] == "":
                return["hola"]
            else:
                sesion = modelos.abrir_sesion()
                consulta = {"nombre": nombreUsuario}
                idUsuario = modelos.Usuarios.read(sesion, **consulta)
                consulta = {"nombreNot": paramsComentario['noticia'][0]}
                idNoticia = modelos.Noticias.read(sesion, **consulta)
                modelos.cerrar_sesion(sesion)
                sesion = None
                escribeNot = modelos.escribeNot(
                idNot=idNoticia,
                idUsuario=idUsuario,
                usuario=nombreUsuario,
                comentario=paramsComentario['comentario'][0],
                likes=0
                )
            
                sesion = modelos.abrir_sesion()
                escribeNot.create(sesion)
                modelos.cerrar_sesion(sesion)
                sesion = None
                start_response('303 See Other', [('Location', '/es')])
                return [b'']
        except Exception as e:
            start_response('500 Internal Server Error', [('Content-type', 'text/plain')])
            return [str(e).encode('utf-8')]
    else:
        return vistas.handle_404(environ, start_response)

def ponerComentarioRes(environ, start_response):
    if environ['REQUEST_METHOD'] == 'POST':
        print("funcion ponerComentario()")
        try:
            size = int(environ.get('CONTENT_LENGTH', 0))
            data = environ['wsgi.input'].read(size).decode()
            paramsComentario = parse_qs(data)      
            
            if params['nombre'] == "" or params['email'] == "" or params['password'] == "" or params['password-2'] == "":
                return["hola"]
            else:
                sesion = modelos.abrir_sesion()
                consulta = {"nombre": nombreUsuario}
                idUsuario = modelos.Usuarios.read(sesion, **consulta)
                modelos.cerrar_sesion(sesion)
                sesion = None
                escribeRes = modelos.escribeRes(
                idUsuario=idUsuario,
                usuario=nombreUsuario,
                comentario=paramsComentario['comentario'],
                likes=0
                )
            
                sesion = modelos.abrir_sesion()
                escribeRes.create(sesion)
                modelos.cerrar_sesion(sesion)
                sesion = None
                start_response('303 See Other', [('Location', '/es')])
                return [b'']
        except Exception as e:
            start_response('500 Internal Server Error', [('Content-type', 'text/plain')])
            return [str(e).encode('utf-8')]
    else:
        return vistas.handle_404(environ, start_response)

def crearUsuario(environ, start_response):
    if environ['REQUEST_METHOD'] == 'POST':
        try:
            print("aaaaaa")
            size = int(environ.get('CONTENT_LENGTH', 0))
            data = environ['wsgi.input'].read(size).decode()
            paramsUsuario = parse_qs(data)      
            if paramsUsuario['nombre'] == "" or paramsUsuario['email'] == "" or paramsUsuario['password'] == "" or paramsUsuario['password-2'] == "":
                return[b"alert('Todos los campos deben de estar completos')"]
            else:
                usuario = modelos.Usuarios(
                nombre=paramsUsuario['nombre'],
                email=paramsUsuario['email'],
                passwd=paramsUsuario['password']
                )
                sesion = modelos.abrir_sesion()
                usuario.create(sesion)
                modelos.cerrar_sesion(sesion)
                sesion = None
                start_response('303 See Other', [('Location', '/contacto')])
                return [b"<script>alert('Cuenta creada correctamente')</script>"]
        except Exception as e:
            start_response('500 Internal Server Error', [('Content-type', 'text/plain')])
            return [str(e).encode('utf-8')]
    else:
        return vistas.handle_404(environ, start_response)

def iniciarSesion(environ, start_response):
    if environ['REQUEST_METHOD'] == 'POST':
        try:
            size = int(environ.get('CONTENT_LENGTH', 0))
            data = environ['wsgi.input'].read(size).decode()
            paramsUsuario = parse_qs(data)      
            if paramsUsuario['nombre'] == "" or paramsUsuario['email'] == "" or paramsUsuario['password'] == "":
                return[b"<script>alert('Todos los campos deben de estar completos')</script>"]
            else:
                
                sesion = modelos.abrir_sesion()
                #consulta = {"nombre" = paramsUsuario['nombre'], "email" = paramsUsuario['email'], "passwd" = paramsUsuario['password']}
                #inicioSesion = modelos.Usuarios.readAlgunos(sesion, **consulta)                   
                modelos.cerrar_sesion(sesion)
                sesion = None
                

                start_response('303 See Other', [('Location', '/contacto')])
                return [b"<script>alert('Sesion iniciada correctamente')</script>" + start_response]
        except Exception as e:
            start_response('500 Internal Server Error', [('Content-type', 'text/plain')])
            return [str(e).encode('utf-8')]
    else:
        return vistas.handle_404(environ, start_response)

def insertarPartido(environ, start_response):
    if environ['REQUEST_METHOD'] == 'POST':
        print("funcion insertarPartido()")
        try:
            size = int(environ.get('CONTENT_LENGTH', 0))
            data = environ['wsgi.input'].read(size).decode()
            paramsPartido = parse_qs(data)      
            
            if paramsPartido['eq1'] == "" or paramsPartido['eq2'] == "" or paramsPartido['dia'] == "" or paramsPartido['password-2'][0] == "":
                return[b"<script>alert('Tienes que rellenar todos los campos')</script>"]
            else:
                sesion = modelos.abrir_sesion()
                modelos.cerrar_sesion(sesion)
                sesion = None
                crearPartido = modelos.evFuturos(
                idNot=idNoticia,
                idUsuario=idUsuario,
                usuario=nombreUsuario,
                comentario=paramsComentario['comentario'][0],
                likes=0
                )
            
                sesion = modelos.abrir_sesion()
                escribeNot.create(sesion)
                modelos.cerrar_sesion(sesion)
                sesion = None
                start_response('303 See Other', [('Location', '/es')])
                return [b'']
        except Exception as e:
            start_response('500 Internal Server Error', [('Content-type', 'text/plain')])
            return [str(e).encode('utf-8')]
    else:
        return vistas.handle_404(environ, start_response)

def app(environ, start_response):
    path = environ.get('PATH_INFO')
    if path == '/':
        return vistas.index(environ, start_response)
    elif path == '/contacto':
        import vistasContacto
        return vistasContacto.contacto(environ, start_response)
    elif path.startswith('/static/'):
        return vistas.serve_static(environ, start_response)
    elif path == '/sign-up':
        return crearUsuario(environ, start_response)
    elif path == '/log-in':
        return iniciarSesion(environ, start_response)
    elif path == '/insert-game':
        return insertarPartido(environ, start_response)
    elif path == '/index':
        return vistas.index(environ, start_response)
    elif path == '/calendario':
        import vistasCalendario
        evFuturos = leerCalendario(environ, start_response)
        return vistasCalendario.paginaEvFuturos(environ, start_response, evFuturos)
    elif path == '/equipos':
        return vistasEquipos.equipos(environ, start_response)
    elif path == '/envivo':
        import vistasEnVivo
        enVivo = leerEnVivo(environ, start_response)
        return vistasEnVivo.paginaEnVivo(environ, start_response, enVivo)
    elif path == '/partidosfinalizados':
        import vistasTerminado
        resTerminados = leerResTerminados(environ, start_response)
        return vistasTerminado.paginaResultados(environ, start_response, resTerminados)
    else:
        return vistas.handle_404(environ, start_response)


if __name__ == "__main__":
    host = 'localhost'
    port = 8000

    httpd = make_server(host, port, app)
    print(f"Servidor en http://{host}:{port}")
    httpd.serve_forever()
'''
Una vez ejecutado el controlador, podemos acceder a través del navegador, 
con las rutas: http://localhost:8000/    (no se usa jinja2)
y   http://localhost:8000/es, esta segunda usa jinja2.
Con la url http://localhost:8000/static/ se mostrará el archivo css.
Si se pone una url diferente, saldrá el mensaje de 'página no encontrada'
'''