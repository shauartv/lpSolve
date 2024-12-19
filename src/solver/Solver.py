from src.interfaces.IEdge import IEdge
from src.interfaces.INode import INode
from src.solver.ModelBuilder import ModelBuilder
from src.solver.Optimizer import Optimizer
from src.solver.SolutionReader import SolutionReader
from src.solver.SolvingResult import SolvingResult


class Solver:

    def __init__(self):
        self.builder = ModelBuilder()
        self.optimizer = Optimizer()
        self.reader = SolutionReader()

    def Solve(self, nodes: list[INode], edges: list[IEdge], income: list[tuple[INode, int]],
              outcome: list[tuple[INode, int]], cons: list[tuple[IEdge, int]]):
        solution = None
        model = self.builder.BuildModel(nodes, edges, income, outcome, cons)
        result = self.optimizer.Solve(model)

        if result in (SolvingResult.optimal, SolvingResult.disbalance):
            solution = self.reader.ReadSolution()

        return result, solution
