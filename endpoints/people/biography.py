import server


class Endpoint(server.Endpoint):

    url = '/people/<name>'

    def get(self, name):
        try:
            return self.context.biography.get_biography(name)
        except:
            raise server.RestfulException(404, 'Could not find person')
