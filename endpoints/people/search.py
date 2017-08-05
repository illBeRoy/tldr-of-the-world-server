import server


class Endpoint(server.Endpoint):

    url = '/people/search/<name>'

    def get(self, name):
        name = name.lower()
        return self.context.names.find(name, 10)
