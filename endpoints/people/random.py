import server


class Endpoint(server.Endpoint):

    url = '/people/random'

    def get(self):
        parser = server.QuerystringParser()
        parser.add_argument('count', help='how many random names to generate', default=10)
        args = parser.parse_args()

        try:
            count = int(args.count)
        except:
            count = 10

        if count > 50:
            count = 50

        return self.context.names.random(count)
