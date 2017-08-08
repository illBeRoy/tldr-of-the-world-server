import os

import utils.biography

biography = utils.biography.Biography(os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'people.sqlite'))
