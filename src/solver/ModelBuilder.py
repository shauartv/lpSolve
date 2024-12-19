from src.interfaces.IEdge import IEdge
from src.interfaces.INode import INode
from src.solver.Graph import FlowNode, FlowEdge
from src.solver.Model import Model


class ModelBuilder:

    def __init__(self):
        self.graphEdges = dict()
        self.graphNodes = dict()
        self.model = Model()

    def BuildModel(self, nodes: list[INode], edges: list[IEdge], income: list[tuple[INode, int]],
                   outcome: list[tuple[INode, int]], cons: list[tuple[IEdge, int]]):
        self.prepare(edges, nodes)
        self.createGraph()
        self.fillModelNodes(income, outcome)
        self.fillModelEdges(cons)
        return self.model

    def prepare(self, edges, nodes):
        self.graphNodes = dict((n.id, FlowNode(n.id, n.name)) for n in nodes)
        for e in edges:
            nfrom = self.graphNodes[e.nodeFrom.id]
            nto = self.graphNodes[e.nodeTo.id]
            self.graphEdges[e.id] = FlowEdge(e.id, e.name, nfrom, nto, e.length, e.reverse)

    def createGraph(self):
        for n in self.graphNodes.values():
            self.model.graph.add_node(n)
        for e in self.graphEdges.values():
            self.model.graph.add_edge(e)

        # map(lambda n: self.model.graph.add_node(n), self.graphNodes)
        # map(lambda e: self.model.graph.add_edge(e), self.graphEdges)

    def fillModelNodes(self, income: list[tuple[INode, int]], outcome: list[tuple[INode, int]]):
        for n, val in income:
            self.graphNodes[n.id].income = val
        for n, val in outcome:
            self.graphNodes[n.id].outcome = val

    def fillModelEdges(self, cons: list[tuple[IEdge, int]]):
        for e, val in cons:
            self.graphEdges[e.id].consumption = val
