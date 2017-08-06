import math

import server


class Endpoint(server.Endpoint):

    url = '/feeds'

    def post(self):
        parser = server.BodyParser()
        parser.add_argument('people', help='people to generate feed from', type=list, required=True)
        args = parser.parse_args()

        if not 5 <= len(args.people) <= 30:
            raise server.RestfulException(400, 'List of people should contain between 5 and 50 names')

        for name in args.people:
            if not isinstance(name, str):
                raise server.RestfulException(400, 'Invalid name: {0}'.format(name))

            if not self.context.names.has(name):
                raise server.RestfulException(400, 'Person "{0}" does not exist in our database'.format(name))

        seed = self.context.group_enrich.enrich_group(args.people, 30)

        feed_id = self.context.feed.get_feed_id(seed)

        return feed_id
