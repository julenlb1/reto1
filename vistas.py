# Este codigo se encarga de dos tareas, la mas importante siendo la gestión de templates y renderización de contenido en el navegador
# además de servir a los archivos estaticos (Solamente imagenes)

# Todos los imports necesarios para el buen funcionamiento del programa
from jinja2 import Environment, FileSystemLoader
import os
import urllib.parse


env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('index.html')
templateContacto = env.get_template('contacto.html')
templateFuturo = env.get_template('calendario.html')
templateVivo = env.get_template('endirecto.html')
templateEquipos = env.get_template('equipos.html')
templateNoticias = env.get_template('noticias.html')
templateResultados = env.get_template('partidosfinalizados.html')
templateGestion = env.get_template('gestion.html')
templateRobots = env.get_template('robots.txt')

# Funciones para manejar las rutas específicas
def indice(environ, start_response, usuario, comentarioRes):
    # Lógica para la ruta '/contacto'
    response = template.render(usuario=usuario, comentarioRes=comentarioRes).encode('utf-8')
    status = '200 OK'
    response_headers = [('Content-type', 'text/html;charset=utf-8')]
    start_response(status, response_headers)
    return [response]

def paginaEvFuturos(environ, start_response, evFuturos, usuario):
    # Lógica para la ruta '/calendario'
    response = templateFuturo.render(evFuturos = evFuturos, usuario=usuario).encode('utf-8')
    status = '200 OK'
    response_headers = [('Content-type', 'text/html;charset=utf-8')]
    start_response(status, response_headers)
    return [response]

def contacto(environ, start_response, usuario):
    # Lógica para la ruta '/contacto'
    response = templateContacto.render(usuario=usuario).encode('utf-8')
    status = '200 OK'
    response_headers = [('Content-type', 'text/html;charset=utf-8')]
    start_response(status, response_headers)
    return [response]

def paginaEnVivo(environ, start_response, envivo, usuario):
    # Lógica para la ruta '/envivo'
    response = templateVivo.render(envivo = envivo, usuario=usuario).encode('utf-8')
    status = '200 OK'
    response_headers = [('Content-type', 'text/html;charset=utf-8')]
    start_response(status, response_headers)
    return [response]

def equipos(environ, start_response, usuario):
    # Lógica para la ruta '/equipos'
    response = templateEquipos.render(usuario=usuario).encode('utf-8')
    status = '200 OK'
    response_headers = [('Content-type', 'text/html;charset=utf-8')]
    start_response(status, response_headers)
    return [response]

def noticias(environ, start_response, usuario):
    # Lógica para la ruta '/noticias'
    response = templateNoticias.render(usuario=usuario).encode('utf-8')
    status = '200 OK'
    response_headers = [('Content-type', 'text/html;charset=utf-8')]
    start_response(status, response_headers)
    return [response]

def paginaResultados(environ, start_response, resTerminados, usuario):
    # Lógica para la ruta '/partidosfinalizados'
    response = templateResultados.render(resTerminados = resTerminados, usuario=usuario).encode('utf-8')
    status = '200 OK'
    response_headers = [('Content-type', 'text/html;charset=utf-8')]
    start_response(status, response_headers)
    return [response]

def gestion(environ, start_response, usuario, partidos, buscado):
    # Lógica para la ruta '/partidosfinalizados'
    response = templateGestion.render(usuario=usuario, partidos=partidos, buscado=buscado).encode('utf-8')
    status = '200 OK'
    response_headers = [('Content-type', 'text/html;charset=utf-8')]
    start_response(status, response_headers)
    return [response]

def sesion_init(start_response, hayUser):
    # Lógica para la ruta '/log-in'
    if hayUser:
        start_response('303 See Other', [('Location', '/')])
        return [b'Seras redirigido al indice']
    else:
        start_response('303 See Other', [('Location', '/noUser')])
        return [b'']

def sesion_finish(environ, start_response):
    # Lógica para la ruta '/log-out'
    start_response('303 See Other', [('Location', '/')])
    return [b'']

def no_user_handle(environ, start_response):
    # Lógica para la ruta '/noUser'
    start_response('303 See Other', [('Location', '/')])
    return [b'Usuario no encontrado, redireccionando...']

def robots(environ, start_response):
    # Lógica para la ruta '/robots'
    response = templateRobots.render().encode('utf-8')
    status = '200 OK'
    response_headers = [('Content-type', 'text')]
    start_response(status, response_headers)
    return [response]

def handle_404(environ, start_response):
    # Lógica para manejar una ruta no reconocida (404)
    status = '404 Not Found'
    response_headers = [('Content-type', 'text/html;charset=utf-8')]
    start_response(status, response_headers)
    return [b'Page not found']

# Función para servir archivos estáticos

def serve_static(environ, start_response):     
    static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static')) #  Aqui conseguimos la ruta a static
    path = environ['PATH_INFO']
    path = urllib.parse.unquote(path, encoding="utf-8")
    print(f"hola: {path}")
    if not path.startswith('/static/'):
        start_response('404 Not Found', [('Content-type', 'text/plain')])
        return [b'Not Found']
    file_path = os.path.join(static_dir, path[len('/static/'):]) # Aqui conseguimos la ruta completa al archivo


    if os.path.isfile(file_path): # Con esta condicion deducimos el tipo de archivo por su extension
        try:
            if file_path.endswith('.png'):
                content_type = 'image/png'
            elif file_path.endswith('.jpg') or file_path.endswith('.jpeg'):
                content_type = 'image/jpeg'
            elif file_path.endswith('.webp'):
                content_type = 'image/webp'
            else:
                content_type = 'application/octet-stream'

            # Servir el archivo (Imagenes)
            with open(file_path, 'rb') as file:
                file_content = file.read()
                start_response('200 OK', [('Content-type', content_type)]) 
                return [file_content]
                
        except Exception as e:
            start_response('500 Internal Server Error', [('Content-type', 'text/plain')])
            return [str(e).encode('utf-8')]
    else:
        # Si el archivo no se encuentra
        start_response('404 Not Found', [('Content-type', 'text/plain')])
        return [b'Not Found']