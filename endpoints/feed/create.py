import server


class Endpoint(server.Endpoint):

    url = '/feeds'

    def post(self):
        parser = server.BodyParser()
        parser.add_argument('people', help='people to generate feed from', type=list, required=True)
        args = parser.parse_args()

        if not 5 <= len(args.people) <= 30:
            raise server.RestfulException(400, 'List of people should contain between 5 and 30 names')

        for name in args.people:
            if not isinstance(name, str):
                raise server.RestfulException(400, 'Invalid name: {0}'.format(name))

            if not self.context.names.has(name):
                raise server.RestfulException(400, 'Person "{0}" does not exist in our database'.format(name))

        # this part was added to ensure robustness - as some people in our database actually DON'T have quotes
        people_without_quotes = set()

        while True:

            # create seed
            seed = self.context.group_enrich.enrich_group(args.people, 30, exclude=people_without_quotes)

            # iterate all people in seed to ensure its safety
            seed_is_safe = True
            for person in seed:
                try:
                    self.context.quotes.quotes_len(person)
                except Exception as err:
                    if person in args.people:
                        raise server.RestfulException(500, 'Cannot use {0}. Our bad.'.format(person))

                    print('omitting {0} from feed'.format(person))

                    people_without_quotes.add(person)
                    seed_is_safe = False
                    break

            if seed_is_safe:
                break

        feed_id = self.context.feed.get_feed_id(args.people, seed)

        self.context.feed.build_feed(feed_id)

        return {'feed_id': feed_id, 'people': seed, 'following': args.people}
