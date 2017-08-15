# TL;DR of the World Server
Part of the [TL;DR of the World](https://tlderofthe.world) academic project.  

Client repository can be found [here](https://github.com/illBeRoy/famous-quote-feed-client).

Whenever "graph" is mentioned in this readme it refers to [another part of the project](https://github.com/illBeRoy/famous-quote-feed-data-explorer).

## Server structure

### Framework
The site sits on a framework built by [Roy](https://github.com/illBeRoy) that warps [flask](http://flask.pocoo.org/), you can explore the framework code in the server directory.

### Endpoints
The endpoints, which sits under the endpoints directory define the api of the server:

#### Feed
- create: expects a list of people (`core`) which will be enriched with more people to create a `seed` and then a feed created for this `seed` (and a unique `feed_id`).
- get: expects a `feed_id` and returns the `core` and the `seed` matching the `feed_id`.
- page: expects a number and `feed_id`. The number represents a page number within the feed. Each page is made out of 30 quotes and the server returns the matching page for the given `feed_id`.

#### People
- biography: expects a name (side note: everytime we refer to name in endpoints it is the page name in wikiquote website). The server returns all the details we know about this person.
- pictures: expects a list of names, returns the images of each person.
- random: return 50 random names from our database.
- search: expects a string, return up to 10 names from our database that starts with this string (used to implement auto-complete).
- suggest: expects a name, return 20 names of people in our database that have similarity to the person, sorted high to low. See more about the similarity in [this repository](https://github.com/illBeRoy/famous-quote-feed-data-explorer).

### Modules
The server module can be found under utils directory:

#### biography
Responsible for:
- Getting all the details  we know on people from the pentheon dataset.
- Fecthing  wikipedia summery and images of peoples.  
Uses [python wikipedia package](https://pypi.python.org/pypi/wikipedia).

You can also find a script that convert the csv that appers in assets direcotry (more on it later) to sqlite db.  

#### feed_generation
Responsible for generating a feed out of `core` and `seed`.  
The module makes sure to provide a feed that gives more emphasis to the `core` people over the people we added to it.  
This is done by building blocks of 10 quotes consisting of 6 `core` quotes and 4 `non-core` quotes.  
The module is also responsible for creating `feed_id` and saving the mapping of them to the `core` and `seed`.

#### graph
Read on it in the linked repository.

#### group_enrichment
Responsible for taking a `core` and enriching it with people using our similarity graph to create a `seed`.

#### names
Responsible for:
- Getting random names.
- Finding names that start with a given string (to support auto-complete).

#### quotes
Responsible for getting quotes and caching them in our db.  
First time we need quotes of a certain  person we fetch them from wikiquote website.  
On every consecutive request, we fetch the quotes from our db.

This uses [python wikiqoute package](https://pypi.python.org/pypi/wikiquote).

### assets 
The assets directory contains:
- A Pickled version of our graph.
- A file with all the names we support.
- A csv that contains all the pentheon details for the names we support + mapping to wikiquote and wikipedia names.
- An sqlite db that was created with the csv fields.
