import server


class Endpoint(server.Endpoint):

    url = '/suggest/<name>'

    def get(self, name):
        return 'ok, {0}'.format(name)
