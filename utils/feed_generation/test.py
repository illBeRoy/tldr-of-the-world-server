import utils.quotes
import utils.feed_generation

feed_client = utils.feed_generation.Feed()
feed_id = feed_client.get_feed_id(['Amy Winehouse', 'Prince (musician)', 'David Ben-Gurion'])
feed = feed_client.get_quotes(feed_id, 0, 8)

print(feed)
