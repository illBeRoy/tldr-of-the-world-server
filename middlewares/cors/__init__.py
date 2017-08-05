def middleware(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
