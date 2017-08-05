import server


class Endpoint(server.Endpoint):

    url = '/people/<name>/suggest'

    def get(self, name):
        return self.context.proximity_graph.get_sorted_neighbours(name)[:20]
