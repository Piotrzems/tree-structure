from enum import Enum


class NodeStyle(Enum):
    """Class representing different types of displaying the tree in PrintTree()
    """
    INDENT = 1
    BULLET = 2
    TREE = 3