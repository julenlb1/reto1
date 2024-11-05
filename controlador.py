from wsgiref.simple_server import make_server
from urllib.parse import parse_qs
import vistas

#import vistasEnVivo
#import vistasEquipos
#import vistasNoticias
#import vistasPlantilla
import modelos
from modelos import ResTerminados
from modelos import enVivo
from modelos import evFuturos
# Definir función para leer productos.
"""def leerProductos():
    sesion = modelos.abrir_sesion()
    consulta = {"id": 1}
    productos = modelos.Producto.read(sesion, **consulta)
    # print(productos)
    modelos.cerrar_sesion(sesion)
    sesion = None
    return productos"""

# Definir función para añadir productos.
"""def add_product(environ, start_response):
    if environ['REQUEST_METHOD'] == 'POST':
        try:
            # Leer y parsear los datos del formulario
            # size 0 si la cabecera CONTENT_LENGTH no está definida
            size = int(environ.get('CONTENT_LENGTH', 0))
            # convertir en cadena de texto
            data = environ['wsgi.input'].read(size).decode()
            params = parse_qs(data) # diccionario con clave y valor (lista, aunque sólo haya un valor)            
            # Crear y guardar el nuevo producto
            producto = modelos.Producto(
                producto=params['producto'][0],
                modelo=params['modelo'][0],
                precio=float(params['precio'][0])
            )
            sesion = modelos.abrir_sesion()
            producto.create(sesion)
            modelos.cerrar_sesion(sesion)
            sesion = None
            # Redirigir a la página principal
            # '303 See Other' indica que se debe realizar una solicitud GET a la 
            # URL especificada en Location, en este caso -> '/es'
            start_response('303 See Other', [('Location', '/es')])
            # hay que devolver cadena de bytes
            return [b''] # cuerpo de la respuesta vacío porque no necesitamos enviar contenido adicional
            # finaliza la respuesta, permitiendo que el navegador procese la redirección hacia '/es'
        except Exception as e:
            start_response('500 Internal Server Error', [('Content-type', 'text/plain')])
            return [str(e).encode('utf-8')]
    else:
        return vistas.handle_404(environ, start_response)"""

def leerResTerminados(environ, start_response):
    
    sesion = modelos.abrir_sesion()
    juegos = sesion.query(ResTerminados).order_by(ResTerminados.matchday.asc(), ResTerminados.dia.asc()).all()
    datosJerarquizados = {}
    for juego in juegos:
        if juego.matchday not in datosJerarquizados:
            datosJerarquizados[juego.matchday] = {}
        if juego.dia not in datosJerarquizados[juego.matchday]:
            datosJerarquizados[juego.matchday][juego.dia] = []
        datosJerarquizados[juego.matchday][juego.dia].append(juego)
    modelos.cerrar_sesion(sesion)
    sesion = None
    return datosJerarquizados
def leerEnVivo(environ, start_response):
    sesion = modelos.abrir_sesion()
    consulta = {envivo.c.matchday, envivo.c.dia}
    modelos.envivo.readJornadas(sesion, consulta)
    modelos.cerrar_sesion(sesion)
    sesion = None
    return envivo

def leerCalendario(environ, start_response):
    sesion = modelos.abrir_sesion()
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
            
            if params['nombre'][0] == "" or params['email'][0] == "" or params['password'][0] == "" or params['password-2'][0] == "":
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
                comentario=paramsComentario['comentario'][0],
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
            size = int(environ.get('CONTENT_LENGTH', 0))
            data = environ['wsgi.input'].read(size).decode()
            paramsUsuario = parse_qs(data)      
            if paramsUsuario['nombre'] == "" or paramsUsuario['email'] == "" or paramsUsuario['password'] == "" or paramsUsuario['password-2'] == "":
                return[b"<script>alert('Todos los campos deben de estar completos')</script>"]
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
                consulta = {"nombre" = paramsUsuario['nombre'], "email" = paramsUsuario['email'], "passwd" = paramsUsuario['password']}
                inicioSesion = modelos.Usuarios.readAlgunos(sesion, **consulta)                   
                modelos.cerrar_sesion(sesion)
                sesion = None
                

                start_response('303 See Other', [('Location', '/contacto')])
                return [b"<script>alert('Sesion iniciada correctamente')</script>" + start_response]
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
        return vistas.contacto(environ, start_response)
    elif path.startswith('/static/'):
        return vistas.serve_static(environ, start_response)
    elif path == '/sign-up':
        return crearUsuario(environ, start_response)
    elif path == '/log-in':
        return iniciarSesion(environ, start_response)
    elif path == '/index':
        envivo = leerEnVivo()
        return vistasEnVivo.index(environ, start_response, envivo)
    elif path == '/calendario':
        import vistasCalendario
        evFuturos = leerCalendario(environ, start_response)
        return vistasCalendario.paginaEvFuturos(environ, start_response, evFuturos)
    elif path == '/equipos':
        return vistasEquipos.equipos(environ, start_response)
    
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