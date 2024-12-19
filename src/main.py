from types import SimpleNamespace

from src.core.BEdge import BEdge
from src.core.BNode import BNode
from src.solver.Solver import Solver


def generate():
    nodes = [BNode(0, 'I1'), BNode(1, 'I2'), BNode(2, 'N1'), BNode(3, 'N2'), BNode(4, 'O1'), BNode(5, 'O2')]
    edges = [BEdge(0, 'I1N2', nodes[0], nodes[3], 10), BEdge(1, 'I2N1', nodes[1], nodes[2], 40),
             BEdge(2, 'I2N2', nodes[1], nodes[3], 10), BEdge(3, 'N1O1', nodes[2], nodes[4], 10),
             BEdge(4, 'N2O2', nodes[3], nodes[5], 10), BEdge(5, 'N1N2', nodes[2], nodes[3], 10, True)]
    income = [(nodes[0], 30), (nodes[1], 70)]
    outcome = [(nodes[4], 30), (nodes[5], 20)]
    cons = [(edges[0], 10), (edges[2], 10), (edges[3], 30)]

    return SimpleNamespace(nodes=nodes, edges=edges, income=income, outcome=outcome, cons=cons)


if __name__ == '__main__':
    bmodel = generate()
    solver = Solver()
    res = solver.Solve(bmodel.nodes, bmodel.edges, bmodel.income, bmodel.outcome, bmodel.cons)
