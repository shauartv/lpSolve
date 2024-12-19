from src.solver.Graph import Graph


class Model:

    def __init__(self):
        self.graph = Graph()

    @property
    def nodes(self):
        return self.graph.nodes

    @property
    def edges(self):
        return self.graph.edges
