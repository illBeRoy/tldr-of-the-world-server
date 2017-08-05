import server


class Endpoint(server.Endpoint):

    url = '/people/search/<query>'

    def get(self, query):
        return self.context.names.find(query, 10)
