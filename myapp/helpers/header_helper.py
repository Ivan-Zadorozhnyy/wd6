def set_header(response, name, value):
    response[name] = value

def get_header(request, name):
    return request.headers.get(name, 'Header not found')
