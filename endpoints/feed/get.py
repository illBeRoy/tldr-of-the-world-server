import server


class Endpoint(server.Endpoint):

    url = '/feeds/<feed_id>'

    def get(self, feed_id):
        parser = server.QuerystringParser()
        parser.add_argument('page', help='which page of the feed to get')
        args = parser.parse_args()

        try:
            page = int(args.page)
        except:
            page = 0

        if page < 0:
            page = 0

        page_size = 30

        try:
            feed = self.context.feed.get_quotes(feed_id, page * page_size, (page + 1) * page_size)
        except:
            raise server.RestfulException(404, 'Feed was not found')

        return {'page': page, 'quotes': feed}
