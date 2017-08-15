import os
import os.path
import sqlite3
import pickle
import time
import random
import hashlib

import utils.quotes


class Feed(object):

    def __init__(self, cache_dir='cache'):
        self._quotes_client = utils.quotes.Quotes(cache_file=os.path.join(cache_dir, 'quotes.cache.sqlite'))
        self._conn = self._initialize_feeds_file(os.path.join(cache_dir, 'feeds.cache.sqlite'))

    def get_feed_id(self, seed_core, seed):
        """
        :param seed_core: The people that are the "core" of the seed
        :param seed: The entire list of people
        :return:
        """
        return self._create_feed_id(seed_core, seed)

    def build_feed(self, feed_id):
        self._get_or_create_feed(feed_id)

    def get_seed_from_feed_id(self, feed_id):
        cur = self._conn.cursor()

        results = cur.execute('SELECT seed FROM feed_id_to_seed WHERE feed_id = ?',
                                   (feed_id,)).fetchall()
        if (len(results)) == 0:
            raise Exception('Seed id not found in db')

        return pickle.loads(results[0][0])

    def get_quotes(self, feed_id, start, stop):
        feed = self._get_or_create_feed(feed_id)
        return feed[start:stop]

    def _get_or_create_feed(self, feed_id):
        """
        returns a list of quotes from feed_id, starting at start, ending at stop (includes)
        """
        try:
            feed = self._get_feed_from_db(feed_id)

        except:
            # Feed not in db, need to create it
            seed_core, seed = self.get_seed_from_feed_id(feed_id)
            self._create_feed(seed_core, seed)

            # get feed that was created
            feed = self._get_feed_from_db(feed_id)

        return feed

    def _get_feed_from_db(self, feed_id):
        cur = self._conn.cursor()

        pickled_feed = cur.execute('SELECT feed FROM feeds WHERE feed_id = ?',
                                   (feed_id,)).fetchall()
        if (len(pickled_feed)) == 0:
            raise Exception('Feed id not found in db')

        return pickle.loads(pickled_feed[0][0])

    def _create_feed_id(self, seed_core, seed):
        """
        Create a unique feed id that is based on the seed
        """
        seed_core = sorted(seed_core)
        seed = sorted(seed)
        feed_id = pickle.dumps((seed_core, seed))
        feed_id = hashlib.md5(feed_id).hexdigest()
        self._save_feed_id_mapping(feed_id, (seed_core, seed))
        return feed_id

    def _create_feed(self, seed_core, seed):
        """
        Create a feed according to a given seed
        :param seed: list of people
        """
        seed = sorted(seed)
        seed_core = sorted(seed_core)
        feed_id = self._create_feed_id(seed_core, seed)
        feed = {}

        for person in seed:
            feed[person] = self._quotes_client.quotes(person)

        feed = self._feed_builder(feed, seed_core, seed)

        pickled_feed = pickle.dumps(feed)
        self._save_feed_id_mapping(feed_id, seed)
        self._save_feed_to_db(feed_id, pickled_feed)

    def _save_feed_id_mapping(self, feed_id, seed):
        cur = self._conn.cursor()

        # Check if feed mapping is already in and then save if needed:
        try:
            self.get_seed_from_feed_id(feed_id)
        except:
            seed = pickle.dumps(seed)
            cur.execute('INSERT INTO feed_id_to_seed (feed_id, seed) VALUES (?, ?)', (feed_id, seed))

        self._conn.commit()

    def _feed_builder(self, feed, seed_core, seed):
        non_core = set(seed)
        non_core = non_core.difference(seed_core)
        non_core = list(non_core)

        final_feed = []
        first_ten = True

        # Every 10 quotes will be 6 core, 4 non-core. until no more of one kind is left.
        while len(non_core) + len(seed_core) != 0:
            chosen_core = []
            chosen_non_core = []

            partial_quotes = []
            for i in range(0, 10, 1):
                if i <= 5 and len(seed_core):
                    chosen_core.append(random.choice(seed_core))
                elif len(non_core):
                    chosen_non_core.append(random.choice(non_core))

            for person in chosen_core:

                # get quote from each chosen_core person
                if len(feed[person]) != 0:
                    quote = random.choice(feed[person])
                    feed[person].remove(quote)
                    partial_quotes.append((quote, person))
                else:

                    # if not more quotes left for this person, delete him from the seed_core list
                    try:
                        seed_core.remove(person)
                    except:
                        pass

            # same for non_core:
            for person in chosen_non_core:
                if len(feed[person]) != 0:
                    quote = random.choice(feed[person])
                    feed[person].remove(quote)
                    partial_quotes.append((quote, person))
                else:
                    try:
                        non_core.remove(person)
                    except:
                        pass

            # don't shuffle first ten quotes
            if first_ten:
                first_ten = False
            else:
                random.shuffle(partial_quotes)

            for quote in partial_quotes:
                final_feed.append(quote)

        return final_feed

    def _save_feed_to_db(self, feed_id, feed):
        '''
        Saves the feed to db
        '''
        cur = self._conn.cursor()

        creation_time = int(time.time())
        cur.execute('INSERT INTO feeds (feed_id, feed, creation_epoc_time) VALUES (?, ?, ?)', (feed_id, feed, creation_time))

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
            conn.execute('CREATE TABLE feeds (feed_id TEXT PRIMARY KEY, feed TEXT, creation_epoc_time INT)')
            conn.execute('CREATE TABLE feed_id_to_seed (feed_id TEXT PRIMARY KEY, seed TEXT)')

            conn.commit()

        return conn
