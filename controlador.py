from wsgiref.simple_server import make_server
from urllib.parse import parse_qs
import vistas
import modelos
from modelos import ResTerminados
from modelos import enVivo
from modelos import evFuturos
from modelos import escribeRes
import os
global usuario
usuario = ""
hayUser = False
idUsuario = None
global sesion
global buscado
global partidoBuscado
partidoBuscado = ""
buscado = False

def leerResTerminados(environ, start_response): # Función para hacer una query de la base de datos a la tabla de resultados terminados
                                                # y plasmar esos datos en el html mediante jinja
    sesion = modelos.abrir_sesion() # Abro la sesión de queries
    juegos = sesion.query(ResTerminados).order_by(ResTerminados.dia.desc(),ResTerminados.matchday.desc()).all() # Esta consulta obtendrá los datos con un orden jerárquico ordenado por matchday > dia > partido 
    datosJerarquizados = {} # Este diccionario guardara los datos en ese orden jerárquico                                                                          
    for juego in juegos:
        if juego.matchday not in datosJerarquizados:
            datosJerarquizados[juego.matchday] = {}
        if juego.dia not in datosJerarquizados[juego.matchday]:
            datosJerarquizados[juego.matchday][juego.dia] = []
        datosJerarquizados[juego.matchday][juego.dia].append(juego)
        print(juego)
    modelos.cerrar_sesion(sesion)
    sesion = None
    return datosJerarquizados # Devolver el diccionario

def leerEnVivo(environ, start_response): # Función para hacer una query de la base de datos a la tabla de partidos en vivo
    sesion = modelos.abrir_sesion()      # y plasmar esos datos en el html mediante jinja
    directos = sesion.query(enVivo).order_by(enVivo.matchday.desc()).all()
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

def leerComIndex(environ, start_response):  # Función para hacer una query de la base de datos a la tabla de escribeRes 
    sesion = modelos.abrir_sesion()         # y plasmar esos datos en la caja de comentarios mediante jinja   
    comentarios = sesion.query(escribeRes).all()
    modelos.cerrar_sesion(sesion)
    sesion = None
    return comentarios

def buscarPartido(environ, start_response):
    
    global usuario
    global buscado
    global partidoBuscado
    if environ['REQUEST_METHOD'] == 'POST':
        try:
            size = int(environ.get('CONTENT_LENGTH', 0))
            data = environ['wsgi.input'].read(size).decode()
            paramsBuscar = parse_qs(data)
            eq1 = paramsBuscar.get('eq1', [None])[0]
            eq2 = paramsBuscar.get('eq2', [None])[0]  
            dia = paramsBuscar.get('fecha_update', [None])[0] 
            
            if not usuario:
                return[b"<script type=text/javascript>alert('No has iniciado sesion')</script>"]
            else:

                resterminados = modelos.ResTerminados()
                consulta = {"eq1":eq1, "eq2":eq2, "dia":dia}
                print("partidoBuscado")
                partidoBuscado = resterminados.readAlgunos(UserSesion, **consulta)
                buscado = True
                
                start_response('303 See Other', [('Location', '/gestion')])
                print("partidoBuscado")
                return [b"Partido encontrado"]
        except Exception as e:
            start_response('500 Internal Server Error', [('Content-type', 'text/plain')])
            return [str(e).encode('utf-8')]
    else:
        return vistas.handle_404(environ, start_response)

def ponerComentarioRes(environ, start_response):
    global usuario
    if environ['REQUEST_METHOD'] == 'POST':
        try:
            size = int(environ.get('CONTENT_LENGTH', 0))
            data = environ['wsgi.input'].read(size).decode()
            paramsComentario = parse_qs(data)
            comentario = paramsComentario.get('comentario', [None])[0] 
            
            if not usuario:
                return[b"<script type=text/javascript>alert('No has iniciado sesion')</script>"]
            else:
                print(f"usuario:{usuario}, idUsuario:{idUsuario}, comentario:{comentario}")
                escribeRes = modelos.escribeRes(
                idusuario=idUsuario,
                usuario=usuario,
                comentario=comentario,
                )
                print("hola")
                escribeRes.create(UserSesion)
                print("hola")
                start_response('303 See Other', [('Location', '/')])
                
                return [b'']
        except Exception as e:
            start_response('500 Internal Server Error', [('Content-type', 'text/plain')])
            return [str(e).encode('utf-8')]
    else:
        return vistas.handle_404(environ, start_response)

def crearUsuario(environ, start_response):
    if environ['REQUEST_METHOD'] == 'POST':
        try:
            size = int(environ.get('CONTENT_LENGTH', 0))
            data = environ['wsgi.input'].read(size).decode()
            paramsUsuario = parse_qs(data)
            usuario = paramsUsuario.get('nombre', [None])[0]
            email = paramsUsuario.get('email', [None])[0]
            contrasena = paramsUsuario.get('password', [None])[0]
            contrasena2 = paramsUsuario.get('password-2', [None])[0]
            
            if usuario == None or email == None or contrasena == None or contrasena2 == None:
                start_response('303 See Other', [('Location', '/contacto')])
                start_response('200 OK', [('Content-type', 'text/html')])
                html_response = """
                <html>
                <head>
                    <title>Error</title>
                </head>
                <body>
                    <h2>Inserta todos los datos necesarios</h2>
                    <p>Seras redirigido al inicio en 3 segundos...</p>
                    <script type="text/javascript">
                        setTimeout(function() {
                            window.location.href = '/';
                        }, 3000);
                    </script>
                </body>
                </html>
                """
                return [html_response.encode('utf-8')]
            else:
                sesion = modelos.abrir_sesion()
                cUsuario = modelos.Usuarios(
                nombre=usuario,
                email=email,
                passwd=contrasena
                )
                
                cUsuario.create(sesion)
                
                modelos.cerrar_sesion(sesion)
                
                sesion = None
                start_response('200 OK', [('Content-type', 'text/html')])
                html_response = f"""
                <html>
                <head>
                    <title>Cuenta creada</title>
                </head>
                <body>
                    <h2>Cuenta creada correctamente</h2>
                    <p>Nombre de usuario: {usuario}</p>
                    <p>Correo: {email}</p> 
                    <button><a href="/">Volver al inicio</a></button>
                </body>
                </html>
                """
                return [html_response.encode('utf-8')]
        except Exception as e:
            start_response('500 Internal Server Error', [('Content-type', 'text/plain')])
            return [str(e).encode('utf-8')]
    else:
        return vistas.handle_404(environ, start_response)

def iniciar_sesion(environ, start_response):
    if environ['REQUEST_METHOD'] == 'POST':
        size = int(environ.get('CONTENT_LENGTH', 0))
        data = environ['wsgi.input'].read(size).decode()
        params = parse_qs(data)
        global usuario, UserSesion, hayUser, idUsuario
        usuario = params.get('usuario', [None])[0]
        contrasena = params.get('password', [None])[0]
        UserSesion = modelos.abrir_sesion()
        consulta = {"nombre": usuario, "passwd": contrasena}
        usuarios = modelos.Usuarios.readAlgunos(UserSesion, **consulta)
        if usuarios:
            hayUser = True
            for usuario1 in usuarios:
                idUsuario = usuario1.id
            
            return usuario, UserSesion, hayUser, idUsuario
        else:
            UserSesion.close()
            UserSesion = None
            return "", None, False, None

def finalizar_sesion():
    global usuario, UserSesion, hayUser, idUsuario
    modelos.cerrar_sesion(UserSesion)
    usuario = ""
    idUsuario = None
    hayUser = False

def insertarPartido(environ, start_response):
    if environ['REQUEST_METHOD'] == 'POST':
        try:
            size = int(environ.get('CONTENT_LENGTH', 0))
            data = environ['wsgi.input'].read(size).decode()
            paramsPartido = parse_qs(data)      
            eq1 = paramsPartido.get('eq1', [None])[0]
            eq2 = paramsPartido.get('eq2', [None])[0]
            dia = paramsPartido.get('fecha', [None])[0]
            hora = paramsPartido.get('horainicio', [None])[0]
            matchday = paramsPartido.get('matchday', [None])[0]
            if eq1 == None or eq2 == None or dia == None or hora == None or matchday == None:
                print(f"eq1:{eq1}; eq2:{eq2}; dia:{dia}; hora:{hora}; matchday:{matchday};")
                start_response('200 OK', [('Content-type', 'text/html')])
                html_response = """
                <html>
                <head>
                    <title>Error</title>
                </head>
                <body>
                    <h2>Inserta todos los datos necesarios</h2>
                    <p>Seras redirigido al inicio en 3 segundos...</p>
                    <script type="text/javascript">
                        setTimeout(function() {
                            window.location.href = '/';
                        }, 3000);
                    </script>
                </body>
                </html>
                """
                return [html_response.encode('utf-8')]
            else:
                sesion = modelos.abrir_sesion()
                crearPartido = modelos.evFuturos(
                eq1=eq1,
                eq2=eq2,
                horainicio=hora,
                dia=dia,
                matchday=matchday,
                mipartido="true"
                )
                sesion.add(crearPartido)
                sesion.commit()
                modelos.cerrar_sesion(sesion)
                sesion = None
                start_response('303 See Other', [('Location', '/gestion')])
                return [b"Partido insertado correctamente"]
        except Exception as e:
            start_response('500 Internal Server Error', [('Content-type', 'text/plain')])
            return [str(e).encode('utf-8')]
    else:
        return vistas.handle_404(environ, start_response)

def actualizarPartido(environ, start_response):
    if environ['REQUEST_METHOD'] == 'POST':
        try:
            size = int(environ.get('CONTENT_LENGTH', 0))
            data = environ['wsgi.input'].read(size).decode()
            paramsUpdate = parse_qs(data)      
            idUpdate = paramsUpdate.get('id', [None])[0]
            eq1 = paramsUpdate.get('eq1_update', [None])[0]
            eq2 = paramsUpdate.get('eq2_update', [None])[0]
            reseq1 = paramsUpdate.get('resultado_eq1', [None])[0]
            reseq2 = paramsUpdate.get('resultado_eq2', [None])[0]
            hora = paramsUpdate.get('hora_update', [None])[0]
            dia = paramsUpdate.get('fecha_update2', [None])[0]
            matchday = paramsUpdate.get('matchday', [None])[0]
            if eq1 == None or eq2 == None or dia == None or hora == None or matchday == None or reseq1 == None or reseq2 == None:
                print(f"eq1:{eq1}; eq2:{eq2}; dia:{dia}; hora:{hora}; matchday:{matchday}; reseq1:{reseq1} reseq2:{reseq2}")
                start_response('200 OK', [('Content-type', 'text/html')])
                html_response = """
                <html>
                <head>
                    <title>Error</title>
                </head>
                <body>
                    <h2>Inserta todos los datos necesarios</h2>
                    <p>Seras redirigido a la pagina de gestión en 3 segundos...</p>
                    <script type="text/javascript">
                        setTimeout(function() {
                            window.location.href = '/';
                        }, 3000);
                    </script>
                </body>
                </html>
                """
                return [html_response.encode('utf-8')]
            else:
                sesion = modelos.abrir_sesion()
                crearPartido = modelos.ResTerminados(
                eq1=eq1,
                eq2=eq2,
                reseq1=reseq1,
                reseq2=reseq2,
                horainicio=hora,
                dia=dia,
                matchday=matchday,
                mipartido="true"
                )
                sesion.commit()
                modelos.cerrar_sesion(sesion)
                sesion = None
                start_response('200 OK', [('Content-type', 'text/html')])
                html_response = """
                <html>
                <head>
                    <title>Error</title>
                </head>
                <body>
                    <h2>Partido actualizado correctamente</h2>
                    <p>Seras redirigido a la pagina de gestión en 3 segundos...</p>
                    <script type="text/javascript">
                        setTimeout(function() {
                            window.location.href = '/gestion';
                        }, 3000);
                    </script>
                </body>
                </html>
                """
                buscado = False
                partidoBuscado = ""
                return [html_response.encode('utf-8')]
        except Exception as e:
            start_response('500 Internal Server Error', [('Content-type', 'text/plain')])
            return [str(e).encode('utf-8')]
    else:
        return vistas.handle_404(environ, start_response)



def app(environ, start_response):
    global usuario, UserSesion, hayUser, idUsuario
    path = environ.get('PATH_INFO')
    if path == '/':
        comentariosres = leerComIndex(environ, start_response)
        return vistas.indice(environ, start_response, usuario, comentariosres)
    elif path == '/contacto':
        return vistas.contacto(environ, start_response, usuario)
    elif path.startswith('/static/'):
        return vistas.serve_static(environ, start_response)
    elif path == '/sign-up':
        return crearUsuario(environ, start_response)
    elif path == '/log-in':
        usuario, UserSesion, hayUser, idUsuario = iniciar_sesion(environ, start_response)
        print(usuario)
        return vistas.sesion_init(start_response, hayUser)
    elif path == '/noUser':
        return vistas.no_user_handle(environ, start_response)    
    elif path == '/log-out':
        finalizar_sesion()
        sesion = None
        return vistas.sesion_finish(environ, start_response)
    elif path == '/insert-game':
        return insertarPartido(environ, start_response)
    elif path == '/search-game':
        return buscarPartido(environ, start_response)
    elif path == '/update-game':
        return actualizarPartido(environ, start_response)
    elif path == '/comentario-index':
        return ponerComentarioRes(environ, start_response)
    elif path == '/calendario':
        evFuturos = leerCalendario(environ, start_response)
        return vistas.paginaEvFuturos(environ, start_response, evFuturos, usuario)
    elif path == '/equipos':
        return vistas.equipos(environ, start_response, usuario)
    elif path == '/envivo':
        enVivo = leerEnVivo(environ, start_response)
        return vistas.paginaEnVivo(environ, start_response, enVivo, usuario)
    elif path == '/partidosfinalizados':
        resTerminados = leerResTerminados(environ, start_response)
        for res in resTerminados.items():
            print(res)
        print("aloasdasdadasUIHFUIHQUIFHQIEUF")
        return vistas.paginaResultados(environ, start_response, resTerminados, usuario)
    elif path == '/noticias':
        return vistas.noticias(environ, start_response, usuario)
    elif path == '/gestion':
        if buscado == False:
            partidoBuscado == ""
        return vistas.gestion(environ, start_response, usuario, partidoBuscado, buscado)
    elif path == '/robots':
        return vistas.robots(environ, start_response)
    elif path == '/sitemap':
        return vistas.robots(environ, start_response)
    else:
        return vistas.handle_404(environ, start_response)


if __name__ == "__main__":
    host = 'localhost'
    port = 5555

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