from src.interfaces.INode import INode


class IEdge:

    def __init__(self, id: int, name: str, nodeFrom: INode, nodeTo: INode, length: int = 0, reverse: bool = False):
        self.reverse = reverse
        self.length = length
        self.nodeTo = nodeTo
        self.nodeFrom = nodeFrom
        self.name = name
        self.id = id
