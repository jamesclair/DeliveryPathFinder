from Location import Location

class DistanceGraph:
    def __init__(self):
        self.adjacency_list = {}
        self.edge_weights = {}
        self.hub_vertex = Location(None)

    def add_vertex(self, new_vertex):
        self.adjacency_list[new_vertex] = []

    def add_directed_edge(self, from_vertex, to_vertex, weight=1.0):
        self.edge_weights[(from_vertex, to_vertex)] = weight
        self.adjacency_list[from_vertex].append(to_vertex)

    def remove_directed_edge(self, from_vertex, to_vertex):
        self.edge_weights.pop([from_vertex, to_vertex])
        self.adjacency_list[from_vertex].pop(to_vertex)

    def add_undirected_edge(self, vertex_a, vertex_b, weight=1.0):
        self.add_directed_edge(vertex_a, vertex_b, weight)
        self.add_directed_edge(vertex_b, vertex_a, weight)

    def remove_undirected_edge(self, vertex_a, vertex_b):
        self.remove_directed_edge(vertex_a, vertex_b)
        self.remove_directed_edge(vertex_b, vertex_a)
