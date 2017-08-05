import os.path

import utils.graph


proximity_graph = utils.graph.Graph()
proximity_graph.load(os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'graph.pickle'))
