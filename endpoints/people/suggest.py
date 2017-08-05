import server


class Endpoint(server.Endpoint):

    url = '/people/<name>/suggest'

    def get(self, name):
        try:
            return self.context.proximity_graph.get_sorted_neighbours(name)[:20]
        except:
            raise server.RestfulException(404, 'Cannot find person')
