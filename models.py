

class PersonData(object):
    def __init__(self, name, url=None):
        self.name = name
        self.url = url


class QuoteData(object):
    def __init__(self, person, quote, date=None):
        self.person = person
        self.quote = quote
        self.date = date

