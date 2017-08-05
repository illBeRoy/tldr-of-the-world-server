import os
import os.path
import sqlite3
import wikiquote


class Quotes(object):

    def __init__(self, cache_file='cache.sqlite'):
        self._conn = self._initialize_cache(cache_file)

    def quotes(self, name, max_quotes=250):
        '''
        Gets quotes for a given name. Must precisely match the record found on wikiquotes.

        Will try to get the records from local cache. In case they do not exist there, will fetch them from
        wikiquotes and later on cache them.

        :param name: name of person
        :param max_quotes: maximal amount of quotes to fetch. optional
        :return: quotes for given name, as a list of strings
        :raises: if person was not found
        '''
        try:
            return self._quotes_from_cache(name, max_quotes=max_quotes)

        except:
            try:
                quotes = self._quotes_from_api(name, max_quotes=max_quotes)
            except:
                raise Exception('No quotes found for input "{0}"'.format(name))

            self._save_quotes_to_cache(name, quotes)

            return quotes

    def quotes_len(self, name):
        '''
        Returns how many quotes the given individual has.

        Tries to get that information from the local cache, and if fails invokes a caching process for the
        quotes themselves.

        :param name: name of person
        :return: how many quotes this person has
        '''
        try:
            return self._len_from_db(name)
        except:
            return len(self.quotes(name))

    def _quotes_from_cache(self, name, max_quotes=100):
        '''
        Gets quotes from local cache.

        :param name: name of person
        :param max_quotes: maximal amount of quotes to fetch. optional
        :return: quotes for given name, as a list of strings
        :raises: if person does not exist in local cache
        '''
        cur = self._conn.cursor()

        quote_records = cur.execute('SELECT * FROM quotes WHERE person = ? ORDER BY i ASC LIMIT ?',
                                    (name, max_quotes)).fetchall()
        if (len(quote_records)) == 0:
            raise Exception('No records found in cache')

        return [quote for person, index, quote in quote_records]

    def _quotes_from_api(self, name, max_quotes):
        '''
        Gets quotes from remote api.

        :param name: name of person
        :param max_quotes: maximal amount of quotes to fetch. optional
        :return: quotes for given name, as a list of strings
        :raises: if person was not found on api
        '''
        quotes = wikiquote.quotes(name, max_quotes=max_quotes)

        if len(quotes) == 0:
            raise Exception('No records found in api')

        return quotes

    def _len_from_db(self, name):
        '''
        Gets the amount of quotes a person has from the database, without querying the quotes themselves.

        This is an optimization.

        :param name: name of person
        :return: amount of quotes they have
        :raises: if person does not exist in db
        '''
        cur = self._conn.cursor()

        try:
            person, quotes_len = cur.execute('SELECT * FROM people WHERE name = ?', (name, )).fetchone()
        except:
            raise Exception('No quotes length in cache')

        print('len from db')
        return quotes_len

    def _save_quotes_to_cache(self, name, quotes):
        '''
        Saves a list of quotes into the cache.

        :param name: name of person
        :param quotes: their quotes
        '''
        cur = self._conn.cursor()

        for index, quote in enumerate(quotes):
            cur.execute('INSERT INTO quotes (person, i, content) VALUES (?, ?, ?)', (name, index, quote))

        cur.execute('INSERT INTO people (name, quotes_len) VALUES (?, ?)', (name, len(quotes)))

        self._conn.commit()

    def _initialize_cache(self, cache_file):
        '''
        Initializes cache file.

        :param cache_file: path to said file
        :return: connection object which is pysqlite3 compliant
        '''
        if os.path.exists(cache_file):
            conn = sqlite3.connect(cache_file)
        else:
            conn = sqlite3.connect(cache_file)
            conn.execute('CREATE TABLE people (name TEXT PRIMARY KEY, quotes_len INT)')
            conn.execute('CREATE TABLE quotes (person TEXT, i INT, content TEXT, PRIMARY KEY (person, i))')
            conn.commit()

        return conn
