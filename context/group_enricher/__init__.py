import os.path

import utils.graph
import utils.group_enrichment
from context.proximity_graph import proximity_graph

group_enricher = utils.group_enrichment.GroupEnrichment(proximity_graph)