from types import SimpleNamespace

from src.interfaces.IEdge import IEdge
from src.interfaces.INode import INode


class FlowNode(INode):
    def __init__(self, id: int, name: str, income: int = 0,
                 outcome: int = 0):
        super().__init__(id, name)
        self.income = income
        self.outcome = outcome


class FlowEdge(IEdge):
    def __init__(self, id: int, name: str, nodeFrom: FlowNode, nodeTo: FlowNode, length: int = 0, reverse: bool = False,
                 consumption: int = 0):
        super().__init__(id, name, nodeFrom, nodeTo, length, reverse)
        self.consumption = consumption


class Graph:

    def __init__(self):
        self.g = dict()

    def __getitem__(self, item):
        return self.g[item]

    @property
    def nodes(self):
        return self.g.keys()

    @property
    def edges(self):
        return set(
            [e for el in self.g.values() for e in el.incoming] + [e for el in self.g.values() for e in el.outcoming])

    def add_node(self, node: FlowNode):
        self.g[node] = SimpleNamespace(outcoming=set(), incoming=set())

    def add_edge(self, edge: FlowEdge):
        self.g[edge.nodeFrom].outcoming.add(edge)
        self.g[edge.nodeTo].incoming.add(edge)
