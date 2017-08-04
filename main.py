from flask import Flask, request
import wikiquote
import random
from graph import Graph

app = Flask(__name__)
DEFAULT_SIZE = 20
graph = Graph().load("graph.pickle")


@app.route('/')
def api_root():
    return 'main page for main people'


@app.route('/random_quote')
def random_quote():
    if 'name' in request.args:
        person = request.args['name']
    else:
        person = "Donald Trump"
    return get_quote(person)


def get_quote(person_name):
    quotes = wikiquote.quotes(person_name)
    quote = random.choice(quotes)
    return quote

@app.route('/enrich_list/')
def get_enrich_list():
    """
    GET request
    given a list of persons, returns an enriched list
    """
    people = request.args.get('people', ["Roy Sommer", "Aviv Ben-Haim"])
    return enrich_list(people)


def enrich_list(people_list, up_to=DEFAULT_SIZE):
    result = set(people_list)
    for person in people_list:
        if len(result) >= up_to:
            break
        neighbors = graph.get_sorted_neighbours(person)
        result.add(neighbors[0])
    return result

if __name__ == '__main__':
    app.run()

