import os.path


class Names(object):

    def __init__(self, assets_dir):
        self._names = {}

        with open(os.path.join(assets_dir, 'names_wikiquote.txt'), 'r', encoding='utf-16') as f:
            self._names['wikiquote'] = list(enumerate(f.read().splitlines()))

        self._names['official'] = self._names['wikiquote']

        self._names['suggestions'] = [(index, name.lower()) for index, name in self._names['official']]

    def find(self, name, limit=10):
        name = name.lower()
        suggestions = []

        for index, _ in filter(lambda x: x[1].startswith(name), self._names['suggestions']):
            suggestions.append(self._names['official'][index][1])

            limit -= 1
            if limit == 0:
                break

        return suggestions

names = Names(os.path.join(os.path.dirname(__file__), '..', '..', 'assets'))
