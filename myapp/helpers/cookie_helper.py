def set_cookie(response, key, value, http_only=True):
    response.set_cookie(key, value, httponly=http_only)

def get_cookie(request, name):
    return request.COOKIES.get(name, 'Cookie not found')
