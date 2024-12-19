import enum


class SolvingResult(enum.Enum):
    optimal = 1
    disbalance = 2
    infeasible = 3
    unknownError = 4
