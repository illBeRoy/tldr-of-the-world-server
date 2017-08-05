from collections import defaultdict


class GroupEnrichment(object):
    def __init__(self, people_graph):
        self._people_graph = people_graph

    def enrich_group(self, group, wanted_size):
        """
        Get a group of people and enrich (enlarge) them to the wanting size
        """

        # find out how many neighbors to get from each person in the group
        number_of_people_needed = len(wanted_size) - len(group)
        number_of_neighbors_to_get = defaultdict(lambda: int)
        i = 0
        while number_of_people_needed != 0:
            if len(group) > i:
                i = 0
            number_of_neighbors_to_get[group[i]] += 1
            number_of_people_needed -= 1
            i += 1

        # get the neighbors of the group
        for person, number_of_neighbors in number_of_neighbors_to_get.items():
            new_people = self._people_graph.get_sorted_neighbours(person)[:number_of_neighbors - 1]
            for new_person in new_people:
                group.append(new_person)

        return group
