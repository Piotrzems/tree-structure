from abc import ABC, abstractmethod
from typing import Union, Optional

class Node:
    """Represent a node in a tree structure.

    A Node object is a fundamental part of a tree, representing elements with children.

    Attributes:
        name (str): The name of the node.
        parent (Node, optional): The parent of this node. Defaults to None.
        children (tuple of NodeOrLeaf): The children of this node.

    Args:
        name (str): The name of the node.
        *children (NodeOrLeaf): Variable length list of children nodes.
    
    Raises:
        TypeError: If no children are provided.
    """
    def __init__(self, name: str, *children: 'NodeOrLeaf'):
        """This method is initializing an object

        Args:
            name (str): name of the node
            children (NodeOrLeaf): variable-length list of all children
        Raises:
            TypeError: No child provided
        """
        if not children:
            raise TypeError("At least one child should be provided for Node")
        self.name = str(name)
        self.parent: Optional[Node] = None
        self.children = children
        for child in children:
            child.parent = self

    def accept(self, visitor: 'Visitor') -> Optional[str]:
        """Accept a visitor for the visitor pattern.

        This method allows a Visitor object to visit the node, enabling operations
        defined in the Visitor to be performed on the node.

        Args:
            visitor (Visitor): The visitor that is visiting this node.

        Returns:
            str: The result of the visitor's visit method.
        """
        return visitor.visit(self)
    
class Leaf:
    """Represent a leaf in a tree structure.

    A Leaf is an element of a tree that does not have any children.
    """
    def __init__(self,name: str):
        """_summary_

        Args:
            name (str): _description_
        """
        self.name = name
        self.parent: Optional[NodeOrLeaf] = None
    def accept(self, visitor: 'Visitor') -> Optional[str]:
        """Accept a visitor for the visitor pattern.

        This method allows a Visitor object to visit the leaf, enabling operations
        defined in the Visitor to be performed on the leaf.

        Args:
            visitor (Visitor): The visitor that is visiting this leaf.

        Returns:
            str: The result of the visitor's visit method.
        """
        return visitor.visit(self)
    
NodeOrLeaf = Union[Node, Leaf]

class Visitor(ABC):
    """Abstract base class for visitors in the visitor pattern.
    
    The Visitor class defines the interface for operations that can be performed on
    elements of a tree-like structure (nodes and leaves).
    """
    @abstractmethod
    def traverse(self, tree_element):
        """Traverse and visit each element in a tree-like structure.

        This method should be implemented to define how to traverse and visit each element.

        Args:
            tree_element (_type_): The element of the tree from which to traverse. 
            Can be Leaf, Node or anything that inherits from them.

        Returns:
            None
        """
        pass
    @abstractmethod
    def visit(self, tree_element):
        """An abstract method to visit a single element in a tree-like structure.

        This method should be implemented to define the operation to perform on a single element.

        Args:
            tree_element (_type_): tree element that can be Leaf, Node or anything that inherits from them.
        """
        pass
    
    @abstractmethod
    def visitFloat(self, tree_element):
        """An abstract method to visit a Float class object in a tree-like structure.

        This method should be implemented to define the operation to perform on a single element.

        Args:
            tree_element (_type_): tree element that is Float.
        """
        pass
    @abstractmethod
    def visitInteger(self, tree_element):
        """An abstract method to visit a Integer class object in a tree-like structure.

        This method should be implemented to define the operation to perform on a single element.

        Args:
            tree_element (_type_): tree element that is Integer.
        """
        pass
    @abstractmethod
    def visitMultiply(self, tree_element):
        """An abstract method to visit a Multiply class object in a tree-like structure.

        This method should be implemented to define the operation to perform on a single element.

        Args:
            tree_element (_type_): tree element that is Multiply.
        """
        pass
    @abstractmethod
    def visitDivide(self, tree_element):
        """An abstract method to visit a Divide class objectin a tree-like structure.

        This method should be implemented to define the operation to perform on a single element.

        Args:
            tree_element (_type_): tree element that is Divide.
        """
        pass
    @abstractmethod
    def visitAdd(self, tree_element):
        """An abstract method to visit a Add class object in a tree-like structure.

        This method should be implemented to define the operation to perform on a single element.

        Args:
            tree_element (_type_): tree element that is Add.
        """
        pass
    @abstractmethod
    def visitNegative(self, tree_element):
        """An abstract method to visit a Negative class object in a tree-like structure.

        This method should be implemented to define the operation to perform on a single element.

        Args:
            tree_element (_type_): tree element that is Negative.
        """
        pass