import server


class Endpoint(server.Endpoint):

    url = '/people/pictures'

    def get(self):
        parser = server.QuerystringParser()
        parser.add_argument('names', help='names of the people to get pictures for')
        args = parser.parse_args()

        if not isinstance(args.names, str):
            return {}

        people = args.names.split(',')
        people = [name.replace('#/COMMA/', ',') for name in people]

        try:
            return self.context.biography.get_wikipedia_images(people)
        except Exception as err:
            raise server.RestfulException(404, 'Could not find people specified in the request ({0})')
