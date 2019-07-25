def wsgi_application(environ, start_response):
        status = '200 OK'
        headers = [
                ('Content-Type', 'text/plain')
        ]
        body = [bites(i + '\n', 'ascii') for i in environ['QUERY_STRING'].split('&')]
        start_response(status, headers)
        return [body]

