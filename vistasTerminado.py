from jinja2 import Environment, FileSystemLoader
import os

env = Environment(loader=FileSystemLoader('templates'))
print(os.path.abspath('templates'))
template = env.get_template('resultados.html')

# Funciones para manejar las rutas específicas

def paginaResultados(environ, start_response, resTerminados):
    # Lógica para la ruta '/templates/partidosfinalizados.html'
    response = template.render(resTerminados = resTerminados).encode('utf-8')
    print("template render")
    print(b"" + response)
    status = '200 OK'
    response_headers = [('Content-type', 'text/html')]
    start_response(status, response_headers)
    return [response]
    

def handle_404(environ, start_response):
    # Lógica para manejar una ruta no reconocida (404)
    status = '404 Not Found'
    response_headers = [('Content-type', 'text/html')]
    start_response(status, response_headers)
    return [b'Page not found']

# Función para servir archivos estáticos
def serve_static(environ, start_response):     
    static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))
    print('static_dir', static_dir)
    #static_dir c:\*\*\DWES\Ej_mvc\static
    path = environ['PATH_INFO']
    print('path is:', path) 
    # path is: /static/style.css    
    css_path = static_dir + '\\style.css'    
    print('css_path:', css_path)
    #css_path: c:\*\*\DWES\Ej_mvc\static\style.css
    
    if not path.startswith('/static/'):
        start_response('404 Not Found', [('Content-type', 'text/plain')])
        return [b'Not Found']
    else:
        # Serve the file
        try:
            with open(css_path, 'rb') as file:
                cssFile = file.read()
                start_response('200 OK', [('Content-type', 'text/css')]) 
                return [cssFile]            
        except Exception as e:
            start_response('500 Internal Server Error', [('Content-type', 'text/plain')])
            return [str(e).encode('utf-8')]