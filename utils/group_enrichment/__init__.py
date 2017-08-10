import copy
import itertools


class GroupEnrichment(object):

    def __init__(self, people_graph):
        self._people_graph = people_graph

    def enrich_group(self, group, wanted_size, exclude=None):
        """
        Get a group of people and enrich (enlarge) them to the wanting size
        """
        enriched_group = copy.copy(group)
        seed = itertools.cycle(group)
        neighbours = {}

        while len(enriched_group) < wanted_size:
            person = next(seed)
            neighbours[person] = neighbours.get(person, iter([n for n, s in self._people_graph.get_sorted_neighbours(person)]))

            try:
                name = next(neighbours[person])

                while name in enriched_group or name in exclude:
                    name = next(neighbours[person])

                enriched_group.append(name)
            except:
                pass

        return enriched_group
