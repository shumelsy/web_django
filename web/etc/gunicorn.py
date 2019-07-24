CONFIG = {                                                                      
    'mode': 'wsgi',                                                           
    'working_dir': '/home/box/etc/',                                           
    # 'python': '/usr/bin/python',                                              
    'args': (                                                                   
        'gunicorn:wsgi_application',
	'--bind=0.0.0.0:8000',                                              
        '--workers=16',                                                         
        '--timeout=60',                                                         
        'app.module',                                                           
    ),                                                                          
}

def wsgi_application(environ, start_response):
        status = '200 OK'
        headers = [
                ('Content-Type', 'text/plain')
        ]
        body = [bites(i + '\n', 'ascii') for i in environ['QUERY_STRING'].split('&')]
        start_response(status, headers)
        return [body]


