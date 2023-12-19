from tokenize import String
from xmlrpc.client import Boolean, boolean
from tree import Node, Leaf, Visitor, NodeOrLeaf
from enums import NodeStyle
from constants import TreeStyle


class PrintTree(Visitor):
    """This class is a visitor for printing the tree in one of the NodeStyle styles.
    """
    def __init__(self, style: NodeStyle):
        self.style = style
        
    def traverse(self, tree_element: NodeOrLeaf) -> str:
        """This method is an entry point for this PrintTree visitor, chooses the correct style of tree structure.

        Args:
            tree_element (NodeOrLeaf): tree element object

        Raises:
            TypeError: empty element

        Returns:
            str: printed structure
        """
        if tree_element is None:
            raise TypeError("Node is provided incorrectly (empty)")
        if self.style == NodeStyle.TREE:
            return self._print_logic_tree(tree_element)
        if self.style == NodeStyle.INDENT:
            return self._print_logic_prefix(tree_element, prefix='')
        if self.style == NodeStyle.BULLET:
            return self._print_logic_prefix(tree_element, prefix='* ')

    def _print_logic_tree(self, tree_element: NodeOrLeaf, prefix:str="", is_last:bool=True) -> str:
        """This method is handling generation of the tree-like structure from tree_element.
        
        e.g.
        In:  Node("Scene", Node("Robot", Node("Flange", Node("Gripper", Leaf("Object"))), Leaf("Camera")), Node("Table", Leaf("Box")))
        Out:
       "╿ Scene
        ├─┮ Robot
        │ ├─┮ Flange
        │ │ └─┮ Gripper
        │ │   └─╼ Object
        │ └─╼ Camera
        └─┮ Table
          └─╼ Box"
        " ╿ Scene\n ├─┮ Robot\n │ ├─┮ Flange\n │ │ └─┮ Gripper\n │ │   └─╼ Object\n │ └─╼ Camera\n └─┮ Table\n   └─╼ Box"
         "Scene\n  Robot\n    Flange\n      Gripper\n        Object\n    Camera\n  Table\n    Box"

        Args:
            tree_element (NodeOrLeaf): tree element object
            prefix (str, optional): defines what should be printed before new element. Defaults to "".
            is_last (bool, optional): Indicates if current element is last child to its parent. Defaults to True.

        Raises:
            TypeError: wrong tree element object type

        Returns:
            str: tree structure
        """
        # Handle the case of a leaf node
        if isinstance(tree_element, Leaf):
            return self._handle_leaf_logic_tree(tree_element,prefix,is_last)
        # Handle the case of an internal node
        if isinstance(tree_element, Node):
            return self._handle_node_logic_tree(tree_element, prefix, is_last)

        raise TypeError("Unsupported tree element type")

    def _handle_leaf_logic_tree(self, tree_element: Leaf, prefix: str, is_last: bool) -> str:
        """This method handles leaf in printing the tree-like structure.

        Args:
            tree_element (Leaf): tree element Leaf object
            prefix (str): defines what should be printed before new element
            is_last (bool):  Indicates if current element is last child to its parent

        Raises:
            TypeError: Leaf name is None

        Returns:
            str: leaf name in correct tree-like structure
        """
        leaf_name = tree_element.accept(self)
        if leaf_name is None:
            raise TypeError("Leaf accept returned None instead of name")
        if is_last:
            connector = TreeStyle.PREFIX_LAST_SIBLING_NO_CHILDREN 
        else:
            connector = TreeStyle.PREFIX_MIDDLE_SIBLING_NO_CHILDREN
        if tree_element.parent is None:
            connector = TreeStyle.PREFIX_ROOT_LONLEY
        return prefix + connector + leaf_name
    def _handle_node_logic_tree(self, tree_element: Node, prefix:str, is_last:bool) -> str:
        """This method handles the generation of node names in a tree-like structure.

        Args:
            tree_element (Node): tree element Node object
            prefix (str): defines what should be printed before new element
            is_last (bool):  Indicates if current element is last child to its parent

        Raises:
            TypeError: Node name is None

        Returns:
            str: node name in correct tree-like structure
        """
        
        lines = self._handle_parent_node(tree_element, prefix, is_last)
        lines += self._handle_node_children(tree_element, prefix, is_last)
        return lines
    
    def _handle_parent_node(self, tree_element: Node, prefix:str, is_last:bool) -> str:
        """This method handles the generation of parent node name in a tree-like structure

        Args:
            tree_element (Node): tree element Node object
            prefix (str): defines what should be printed before new element
            is_last (bool):  Indicates if current element is last child to its parent

        Raises:
            TypeError: Node name is None

        Returns:
            str: node name in correct tree-like structure
        """
        leaf_name = tree_element.accept(self)
        if leaf_name is None:
            raise TypeError("Leaf accept returned None instead of name")
        if is_last:
            connector = TreeStyle.PREFIX_LAST_SIBILING_W_CHILD 
        else: connector = TreeStyle.PREFIX_MIDDLE_SIBLING_W_CHILD
        if tree_element.parent is None:
            connector = TreeStyle.PREFIX_ROOT
        return prefix + connector + leaf_name 
    
    def _handle_node_children(self, tree_element: Node, prefix:str, is_last:bool) -> str:
        """This method handles the generation of children node names in a tree like structure

        Args:
            tree_element (Node): tree element Node object
            prefix (str): defines what should be printed before new element
            is_last (bool):  Indicates if current element is last child to its parent

        Returns:
            str: children node name in correct tree-like structure
        """
        # Recursively handle the children
        lines = ""
        for i, child in enumerate(tree_element.children):
            is_last_child = i == len(tree_element.children) - 1
            extension = "  " if is_last else TreeStyle.PREFIX_VERTICAL_CONTINUATION
            if tree_element.parent is None:
                extension =""
            lines += "\n" + (self._print_logic_tree(child, prefix + extension, is_last_child))
        return lines

    def _print_logic_prefix(self, tree_element: NodeOrLeaf, level:int=0, prefix:str='') -> str:
        """This method handles generation of node and children names in the prefix-like structure
        
        e.g.
        In:  Node("Scene", Node("Robot", Node("Flange", Node("Gripper", Leaf("Object"))), Leaf("Camera")), Node("Table", Leaf("Box")))
        with prefix = " ":
        Out: "Scene\n  Robot\n    Flange\n      Gripper\n        Object\n    Camera\n  Table\n    Box"
         
        with prefix = "* ":
        Out: "* Add\n  * Integer(2)\n  * Divide\n    * Multiply\n      * Float(5.0)\n      * Negative\n        * Integer(3)\n    * Float(10.0)"

        Args:
            tree_element (NodeOrLeaf): tree element object
            level (int, optional): current level of the structure. Defaults to 0.
            prefix (str, optional): previous lines to be printed before nem tree element. Defaults to ''.

        Raises:
            TypeError: no return value

        Returns:
            str: complete prefix-like structure
        """
        name = tree_element.accept(self)
        if name is None:
            raise TypeError("Leaf or Node accept returned None instead of name")
        
        result =  '  '*level + prefix + name
        if isinstance(tree_element, Node):
            for child in tree_element.children:
                result += '\n' + self._print_logic_prefix(child, level+1, prefix)
        return result

    def visit(self, tree_element: NodeOrLeaf) -> str:
        """This method visits the Node or Leaf objects and return its name for PrintTree visitor.

        Args:
            tree_element (NodeOrLeaf): tree element object

        Returns:
            str: name of the tree eleemnt
        """
        return tree_element.name
    
    def visitInteger(self, tree_element: NodeOrLeaf) -> str:
        """This method visits the Integer objects and return its name for PrintTree visitor.

        Args:
            tree_element (NodeOrLeaf): tree element object

        Returns:
            str: name of the tree eleemnt
        """
        return str(tree_element.name) + "(" + str(tree_element) + ")"
    
    def visitNegative(self, tree_element: NodeOrLeaf) -> str:
        """This method visits the Negative objects and return its name for PrintTree visitor.

        Args:
            tree_element (NodeOrLeaf): tree element object

        Returns:
            str: name of the tree eleemnt
        """
        return str(tree_element.name)
    
    def visitDivide(self, tree_element: NodeOrLeaf) -> str:
        """This method visits the Divide objects and return its name for PrintTree visitor.

        Args:
            tree_element (NodeOrLeaf): tree element object

        Returns:
            str: name of the tree eleemnt
        """
        return tree_element.name
    
    def visitFloat(self, tree_element: NodeOrLeaf) -> str:
        """This method visits the Float objects and return its name for PrintTree visitor.

        Args:
            tree_element (NodeOrLeaf): tree element object

        Returns:
            str: name of the tree eleemnt
        """
        return str(tree_element.name) + "(" + str(tree_element) + ")"

    def visitAdd(self, tree_element: NodeOrLeaf) -> str:
        """This method visits the Add objects and return its name for PrintTree visitor.

        Args:
            tree_element (NodeOrLeaf): tree element object

        Returns:
            str: name of the tree eleemnt
        """
        return tree_element.name
    
    def visitMultiply(self, tree_element: NodeOrLeaf) -> str:
        """This method visits the Multiply objects and return its name for PrintTree visitor.

        Args:
            tree_element (NodeOrLeaf): tree element object

        Returns:
            str: name of the tree eleemnt
        """
        return tree_element.name


