class TreeStyle():
    """Tree style. In this example should look like this:
   ╿ Scene
   ├─┮ Robot
   │ ├─┮ Flange
   │ │ └─┮ Gripper
   │ │   └─╼ Object
   │ └─╼ Camera
   └─┮ Table
     └─╼ Box
    """
    PREFIX_ROOT_LONLEY = '─╼ ' #single leaf without the root
    PREFIX_ROOT = ' ╿ ' # root

    PREFIX_LAST_SIBILING_W_CHILD = ' └─┮ ' # last sibling of a node that has 1 child
    PREFIX_LAST_SIBLING_NO_CHILDREN = ' └─╼ ' # Last sibling which is a leaf (without children)
    PREFIX_MIDDLE_SIBLING_NO_CHILDREN = ' ├─╼ '# MIDDLE sibling leaf (without children)
    
    PREFIX_MIDDLE_SIBLING_W_CHILD = ' ├─┮ '  # middle child that is a node with at least 1 child 
    PREFIX_VERTICAL_CONTINUATION = ' │' # last leaf 
    

class PrintExpressionStyle():
    """Class representing contant symbols used for printing the tree in PrintExpression()
    """
    SYMBOL_DIVISION = " / "
    SYMBOL_MULTIPLY = " * "
    SYMBOL_NEGATIVE = "-"
    SYMBOL_ADD = " + "