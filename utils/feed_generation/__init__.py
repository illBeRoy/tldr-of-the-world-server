import os
import os.path
import sqlite3
import pickle
import time
import random

import utils.quotes


class Feed(object):
    def __init__(self, cache_dir='cache'):
        self._quotes_client = utils.quotes.Quotes(cache_file=os.path.join(cache_dir, 'quotes.cache.sqlite'))
        self._conn = self._initialize_feeds_file(os.path.join(cache_dir, 'feeds.cache.sqlite'))

    def get_feed_id(self, seed):
        return self._create_feed_id(seed)

    def get_seed_from_feed_id(self, feed_id):
        return pickle.loads(feed_id)

    def get_quotes(self, feed_id, start, stop):
        """
        returns a list of quotes from feed_id, starting at start, ending at stop (includes)
        """

        try:
            feed = self._get_feed_from_db(feed_id)
            if len(feed) < stop:
                return feed[start:]
            else:
                return feed[start:stop]
        except:

            # Feed not in db, need to create it
            seed = pickle.loads(feed_id)
            self._create_feed(seed)
            feed = self._get_feed_from_db(feed_id)
            if len(feed) < stop:
                return feed[start:]
            else:
                return feed[start:stop]

    def _get_feed_from_db(self, feed_id):
        cur = self._conn.cursor()

        pickled_feed = cur.execute('SELECT feed FROM feeds WHERE id = ?',
                                   (feed_id,)).fetchall()
        if (len(pickled_feed)) == 0:
            raise Exception('Feed id not found in db')

        return pickle.loads(pickled_feed[0][0])

    def _create_feed_id(self, seed):
        """
        Create a unique feed id that is based on the seed
        """
        feed_id = pickle.dumps(sorted(seed))
        return feed_id

    def _create_feed(self, seed):
        """
        Create a feed according to a given seed
        :param seed: list of people
        """
        seed = sorted(seed)
        feed_id = self._create_feed_id(seed)
        feed = []

        for person in seed:
            quotes = self._quotes_client.quotes(person)
            for quote in quotes:
                feed.append((quote, person))

        feed = self._shuffle_feed(feed)

        pickled_feed = pickle.dumps(feed)
        self._save_feed_to_db(feed_id, pickled_feed)

    def _shuffle_feed(self, feed):
        random.shuffle(feed)
        return feed

    def _save_feed_to_db(self, feed_id, feed):
        '''
        Saves the feed to db
        '''
        cur = self._conn.cursor()

        creation_time = int(time.time())
        cur.execute('INSERT INTO feeds (id, feed, creation_epoc_time) VALUES (?, ?, ?)', (feed_id, feed, creation_time))

        self._conn.commit()


    def _initialize_feeds_file(self, seed_file):
        '''
        Initializes seed file.

        :param seed: path to said file
        :return: connection object which is pysqlite3 compliant
        '''
        if os.path.exists(seed_file):
            conn = sqlite3.connect(seed_file)
        else:
            conn = sqlite3.connect(seed_file)
            conn.execute('CREATE TABLE feeds (id TEXT PRIMARY KEY, feed TEXT, creation_epoc_time INT)')

            conn.commit()

        return conn
