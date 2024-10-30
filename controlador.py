from wsgiref.simple_server import make_server
from urllib.parse import parse_qs
import vistas
import modelos

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
def crearUsuario(environ, start_response):
    if environ['REQUEST_METHOD'] == 'POST':
        print("funcion crearUsuario()")
        try:
            print("funcion crearUsuario()")
            # Leer y parsear los datos del formulario
            # size 0 si la cabecera CONTENT_LENGTH no está definida
            size = int(environ.get('CONTENT_LENGTH', 0))
            # convertir en cadena de texto
            data = environ['wsgi.input'].read(size).decode()
            params = parse_qs(data) # diccionario con clave y valor (lista, aunque sólo haya un valor)            
            # Crear y guardar el nuevo producto
            
            ##if params['nombre'][0] == "" or params['email'][0] == "" or params['password'][0] == "" or params['password-2'][0] == "":
              #  return["hola"]
            #else:
            usuario = modelos.Usuarios(
            nombre=params['nombre'][0],
            email=params['email'][0],
            passwd=params['password'][0]
            )
            print("hola")
        
            sesion = modelos.abrir_sesion()
            usuario.create(sesion)
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
        return vistas.handle_404(environ, start_response)
# Definir la función app que manejará las solicitudes.
def app(environ, start_response):
    path = environ.get('PATH_INFO')
    # print('path: ', path)
    if path == '/':
        return vistas.english_handle_index(environ, start_response)
    elif path == '/es':
        #productos = leerProductos()
        return vistas.spanish_handle_index(environ, start_response)
    elif path.startswith('/static/'):
        return vistas.serve_static(environ, start_response)
    elif path == '/sign-up':
        print("path /sign-up")
        return crearUsuario(environ, start_response)
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