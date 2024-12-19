from pulp import LpMinimize, LpProblem, lpSum, LpVariable, value

LOW_BND = 0
UP_BND = 1e3


class Optimizer:

    def __init__(self):
        self.disbNVar = dict()
        self.disbPVar = dict()
        self.flowOutRevVar = dict()
        self.flowInRevVar = dict()
        self.flowOutVar = dict()
        self.flowInVar = dict()
        self.model = None
        self.lpModel = LpProblem(name="ftp", sense=LpMinimize)

    def Solve(self, model):
        self.model = model
        self.createVariables()
        self.addConstraints()
        self.addObjectiveFunc()
        res = self.optimize()

        # debug PrintSolution
        self.debugPrintSolution()

    def createVariables(self):
        for e in self.model.edges:
            self.flowInVar[e] = LpVariable(name=f"fin {e.name}", lowBound=LOW_BND, upBound=UP_BND)
            self.flowOutVar[e] = LpVariable(name=f"fout {e.name}", lowBound=LOW_BND, upBound=UP_BND)
            if e.reverse:
                self.flowInRevVar[e] = LpVariable(name=f"finrev {e.name}", lowBound=LOW_BND, upBound=UP_BND)
                self.flowOutRevVar[e] = LpVariable(name=f"foutrev {e.name}", lowBound=LOW_BND, upBound=UP_BND)

        for n in self.model.nodes:
            self.disbPVar[n] = LpVariable(name=f"ndisb_p {n.name}", lowBound=LOW_BND, upBound=UP_BND)
            self.disbNVar[n] = LpVariable(name=f"ndisb_n {n.name}", lowBound=LOW_BND, upBound=UP_BND)

    def addConstraints(self):
        self.addEdgeBalEq()
        self.addNodeBalEq()

    def addEdgeBalEq(self):
        for e in self.model.edges:
            expr = self.flowInVar[e] - self.flowOutVar[e] - e.consumption
            if e.reverse:
                expr += self.flowOutRevVar[e] - self.flowInRevVar[e]
            self.lpModel += (expr == 0, f"edgebal {e.name}")

    def addNodeBalEq(self):
        for n in self.model.nodes:
            expr = lpSum([self.flowOutVar[e] for e in self.model.graph[n].incoming])
            expr -= lpSum([self.flowInVar[e] for e in self.model.graph[n].outcoming])
            expr -= lpSum([self.flowInRevVar[e] for e in self.model.graph[n].incoming if e.reverse])
            expr += lpSum([self.flowOutRevVar[e] for e in self.model.graph[n].outcoming if e.reverse])
            expr += self.disbPVar[n] - self.disbPVar[n]
            expr += n.income - n.outcome
            self.lpModel += (expr == 0, f"nodebal {n.name}")

    def addObjectiveFunc(self):

        expr = 0
        for e in self.model.edges:
            expr += (self.flowInVar[e] + self.flowOutVar[e]) * e.length
            if e.reverse:
                expr += (self.flowOutRevVar[e] + self.flowInRevVar[e]) * e.length

        for n in self.model.nodes:
            expr += 1e6 * (self.disbPVar[n] + self.disbNVar[n])
        self.lpModel += expr

    def optimize(self):
        return self.lpModel.solve()

    def debugPrintSolution(self):
        for e in self.model.edges:
            fin = value(self.flowInVar[e]) - (value(self.flowInRevVar[e]) if e.reverse else 0)
            fout = value(self.flowOutVar[e]) - (value(self.flowOutRevVar[e]) if e.reverse else 0)
            print(f"{e.name} in: {fin} out: {fout}")
