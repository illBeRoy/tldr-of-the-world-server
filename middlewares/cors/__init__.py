import flask


def middleware(app):

    def handler(response):
        response.headers['Access-Control-Allow-Origin'] = '*'

        if flask.request.method == 'OPTIONS':
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type'

        return response

    app.after_request(handler)

    return handler
