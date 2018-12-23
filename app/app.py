from pprint import pformat

def hello(env, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    yield b"Hello world!"
    
def application(env, start_response):
    status = "200 OK"   

    body = pformat(env).encode('utf-8')
    headers = [('Content-Type', 'text/plain'),
                ('Content-Lenght',str(len(body)))
        ]
    start_response(status, headers)
    yield body

def parametrs(env, start_response):
    status = "200 OK"
    body = None
    if env['REQUEST_METHOD'] == "GET":
        body = 'Metod GET \nParametrs : {}'.format(env['QUERY_STRING'].split('&')).encode()
    elif env['REQUEST_METHOD'] == "POST":
        try:
            request_body_size = int(env.get('CONTENT_LENGTH', 0))
        except (ValueError):
            request_body_size = 0
        body = 'Metod POST \nParametrs : {}'.format(env['wsgi.input'].read(request_body_size)).encode()
    headers = [('Content-Type', 'text/plain'),
               ('Content-Lenght', str(len(body)))
               ]
    start_response(status, headers)
    yield body
