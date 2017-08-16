# TL;DR of the World Server
Part of the [TL;DR of the World](https://tldrofthe.world) academic project.  

Client repository can be found [here](https://github.com/illBeRoy/tldr-of-the-world-client).

Whenever "graph" is mentioned in this readme it refers to [another part of the project](https://github.com/illBeRoy/tldr-of-the-world-data).

## Server structure

### Framework
The server uses a customly written framework (created by [Roy Sommer](https://github.com/illberoy)) that is built around [flask](http://flask.pocoo.org/), and allows for creating declarative api specification by defining a collection of Endpoint classes. It is not essential to understand the framework in order to study the server's BL, as it is the technical driver that creates an abstraction to run the logic upon.

### Endpoints
The endpoints are the de-facto api sepcification of the server:

#### Feed

- `[POST] /feed`: expects a list of people (`core`) which will be enriched with more people to create an enriched `seed` group using our proximity graph (see [graphy](https://github.com/illBeRoy/tldr-of-the-world-data)) and then a persistant feed is created for this `seed`, with a unique `feed_id`.

- `[GET] /feed/<feed_id>`: for a given `feed_id`, returns information about said feed: seed, core group, and id for validation.

- `[GET] /feed/<feed_id>/<page>`: expects `feed_id` and `page` number. Returns a corresponding page of the given feed, consisting of 30 quotes.

#### People

- `[GET] /people/<person>`: expects a name that matches a record in our names database. The server returns all the details we know about this person, including their picture and a summary from wikipedia.

- `[GET] /people/pictures?names=<str>`: expects a list of names, returns the images for specified people.

- `[GET] /people/random`: returns 50 random names from our database.

- `[GET] /people/search/<query>`: expects a string, returns up to 10 names from our database which begin with given string (used to implement auto-complete).

- `[GET] /people/<person>/suggest`: for a given person in our database, returns 20 names of people in our database that have similarity to the person. One again, uses our proximity graph which can be found in [this repository](https://github.com/illBeRoy/famous-quote-feed-data-explorer).

### Modules
The server module are logical units, each having their own well defined domain:

#### Biography

Responsible for:

- Getting all the details  we know on people from the pentheon dataset.

- Fecthing  wikipedia summary and images of peoples.  
Uses [python wikipedia package](https://pypi.python.org/pypi/wikipedia).

You can also find a script that convert the pantheon csv into sqlite db.  

#### Group Enrichment
Responsible for taking a `core` and enriching it with people using our proxmity graph. This is used to create a `seed` - a group of people sharing similar background which can be used to create the feed.

#### Feed Generation

Responsible for generating a feed out of `core group` and `seed`.  
The module makes sure to provide a feed that gives more emphasis to the `core` people over the people we added to it using the `enrichment` module.

This is done by building blocks of 10 quotes consisting of 6 `core` quotes and 4 `non-core` quotes.

The module is also responsible for creating `feed_id` and saving the mapping of them to the `core` and `seed`.

#### Names

Responsible for managing our name listings, which allows for searching our names database.

#### Quotes

Responsible for getting quotes and caching them in a local db.

First time we need quotes of a certain  person we fetch them from wikiquote website.  
On every consecutive request, we fetch the quotes from our cache.

This uses [python wikiqoute package](https://pypi.python.org/pypi/wikiquote).

### Assets

The assets directory contains:

- A Pickled version of our graph.

- A file with all the names we support.

- A csv that contains all the pentheon details for the names we support + mapping to wikiquote and wikipedia names.

- An sqlite db that was created with the csv fields.
