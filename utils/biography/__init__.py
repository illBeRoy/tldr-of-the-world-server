import wikipedia
import sqlite3
import requests


class Biography(object):

    def __init__(self, people_db):
        self._db_connection = self._get_db_connection(people_db)
        self._picture_size = 200

        # In {NAMES} we can enter more then one title name separated by |
        self._wikipedia_api = 'https://en.wikipedia.org/w/api.php'

    def get_biography(self, name):
        """
        :param name: name of person (wikiquote title page)
        :return: a dict with the fields name, summery, image_url, wikipedia_url
        """
        wikipedia_name = self._wikiquote_name_to_wikipedia_name(name)
        page = wikipedia.page(title=wikipedia_name)
        image_url = self.get_wikipedia_images(name)[name]
        result = self._get_bio_from_db(name)
        result['summery'] = page.summary
        result['image_url'] = image_url
        result['wikipedia_url'] = page.url
        return result

    def _get_bio_from_db(self, name):
        cur = self._db_connection.cursor()

        results = cur.execute('SELECT * FROM people WHERE wikiquote_name = ?', (name,)).fetchall()
        person = results[0]
        bio = {'name': name,
               'occupation': person[2],
               'industry': person[3],
               'domain': person[4],
               'gender': person[5],
               'birth_year': person[6],
               'lat': person[7],
               'lon': person[8],
               'country_name': person[9],
               'birth_city': person[10]}
        return bio

    def get_wikipedia_images(self, wikiquote_names):
        """
        Returns a dict: {name: image_url, name2: image_url...}
        :param wikiquote_names: list of wikiquotes pages or just one
        """
        wikiquote_names = self._as_list(wikiquote_names)
        wikiquote_name_to_wikipedia_name = {wikiquote_name: self._wikiquote_name_to_wikipedia_name(wikiquote_name)
                                            for wikiquote_name in wikiquote_names}

        wikipedia_name_to_wikiquote_name = {v: k for k, v in wikiquote_name_to_wikipedia_name.items()}

        names = ''
        for wikipedia_name in wikiquote_name_to_wikipedia_name.values():
            if names == '':
                names = wikipedia_name
            else:
                names = '{0}|{1}'.format(names, wikipedia_name)

        params = {'action': 'query',
                  'titles': names,
                  'prop': 'pageimages',
                  'format': 'json',
                  'pithumbsize': self._picture_size
                  }

        result = requests.get(self._wikipedia_api, params=params)

        pages = result.json()['query']['pages']
        images = {}
        for page in pages.values():
            wikiquote_name = wikipedia_name_to_wikiquote_name[page['title']]
            images[wikiquote_name] = page['thumbnail']['source']

        return images

    def _wikiquote_name_to_wikipedia_name(self, wikiquote_name):
        cur = self._db_connection.cursor()

        results = cur.execute('SELECT wikipedia_name FROM people WHERE wikiquote_name = ?',
                                   (wikiquote_name,)).fetchall()
        if (len(results)) == 0:
            raise Exception('Wikiquote name not found in db')

        return results[0][0]

    def _get_db_connection(self, people_db):
        return sqlite3.connect(people_db)

    def _as_list(self, obj):
        if isinstance(obj, (list, tuple)):
            return obj

        return [obj]