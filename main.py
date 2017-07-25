from flask import Flask, request
import wikiquote
import random


app = Flask(__name__)


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



if __name__ == '__main__':
    app.run()

