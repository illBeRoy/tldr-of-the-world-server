import server


class Endpoint(server.Endpoint):

    url = '/feeds/<feed_id>'

    def get(self, feed_id):
        try:
            following, people = self.context.feed.get_seed_from_feed_id(feed_id)
        except:
            raise server.RestfulException(404, 'Feed not found')

        return {'feed_id': feed_id, 'following': following, 'people': people}
