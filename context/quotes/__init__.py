import os
import os.path

import utils.quotes


quotes = utils.quotes.Quotes(cache_file=os.path.join('cache', 'quotes.cache.sqlite'))
