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

