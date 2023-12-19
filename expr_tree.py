from abc import abstractmethod
from typing import Union, Optional
from tree import Node, Leaf, Visitor, NodeOrLeaf
from constants import PrintExpressionStyle

class ExpressionNode(Node):
    """This class is treating mathematical expressions.
    
    ExpressionNode can be treated as specialized type of Node.
    """
    def __init__(self, name: str, *children: NodeOrLeaf):
        """This method is initializing the object

        Args:
            name (str): Name of the Node (e.g. Mulitply, Negative etc.)
        """
        # Result is set to None, as all children has to be calculated first
        self.result: Optional[Union[int, float]] = None
        super().__init__(name, *children)
 
    @abstractmethod    
    def accept(self, visitor: Visitor) -> None:
        """This method is an abstract method that is an enty point for a visitor

        Args:
            visitor (Visitor): visitor
        """
        pass

class ExpressionLeaf(Leaf):
    """This class is treating mathematical expressions that have leaf structure

    ExpressionLeaf can be treated as specialized type of Leaf
    """
    def __init__(self, name: str, value: Union[int, float]):
        """This method is initializing the object

        Args:
            name (str): Name of the leaf (e.g. Float, Integer etc.)
            value (Union[int, float]): value of the leaf (e.g. 2.0, 4)
        """
        self.result: Union[int, float] = value
        super().__init__(name)

    @abstractmethod    
    def accept(self, visitor: Visitor):
        """This method is an abstract method that is an enty point for a visitor

        Args:
            visitor (Visitor): visitor
        """
        pass
ExpressionNodeOrLeaf = Union[ExpressionNode, ExpressionLeaf]

class Add(ExpressionNode):
    """This class is expressing the Add expressionNode object.
    
    e.g. Add(Float(2.0), Integer(4))
    """
    def __init__(self, *children):
        """This method is initializing the object
        """
        super().__init__('Add',*children)
    def __str__(self):
        return PrintExpressionStyle.SYMBOL_ADD
    def accept(self, visitor: Visitor):
        return visitor.visitAdd(self)

class Multiply(ExpressionNode):
    """This class is expressing the Multiply expressionNode object.
    
    e.g. Multiply(Float(2.0), Integer(4))
    """
    def __init__(self, *children):
        """This method is initializing the object
        """
        super().__init__('Multiply', *children)
    def __str__(self):
        return PrintExpressionStyle.SYMBOL_MULTIPLY
    def accept(self, visitor: Visitor):
        return visitor.visitMultiply(self)

class Divide(ExpressionNode):
    """This class is expressing the Divide expressionNode object.
    
    e.g. Divide(Float(2.0), Integer(4))
    """
    def __init__(self, *children):
        """This method is initializing the object
        """
        if len(children) is not 2:
            raise TypeError("Division can be performed no more nor less than 2 elements")
        super().__init__("Divide", *children)
    def __str__(self):
        return PrintExpressionStyle.SYMBOL_DIVISION
    def accept(self, visitor: Visitor):
        return visitor.visitDivide(self)

class Negative(ExpressionNode):
    """This class is expressing the Negative expressionNode object.
    
    e.g. Negative(Divide(Float(2.0), Integer(4)))
    """
    def __init__(self, *children):
        """This method is initializing the object
        """
        if len(children) > 1:
            raise TypeError("Only one child should be provided for Negative Node")
        super().__init__('Negative', *children)
    def __str__(self):
        return PrintExpressionStyle.SYMBOL_NEGATIVE
    def accept(self, visitor: Visitor):
        return visitor.visitNegative(self)

class Integer(ExpressionLeaf):
    """This class is expressing the Integer expressionLeaf object.
    
    e.g. Integer(2)
    """
    def __init__(self, value):
        """This method is initializing the object
        """
        super().__init__("Integer", int(value))
    def __str__(self):
        return str(self.result)

    def accept(self, visitor: Visitor):
        return visitor.visitInteger(self)

class Float(ExpressionLeaf):
    """This class is expressing the Float expressionLeaf object.
    
    e.g. Float(2.0)
    """
    def __init__(self, value):
        """This method is initializing the object
        """
        super().__init__("Float", float(value))  
    def __str__(self):
        return str(self.result)

    def accept(self, visitor: Visitor):
        return visitor.visitFloat(self)

class EvaluateExpression(Visitor):
    """This class is a visitor to evaluate expressions. eg.:
    expressions = [
            Integer(42),
            Negative(Integer(23)),
            Divide(Integer(5), Integer(2)),
            Divide(Float(5), Integer(2)),
            Add(Integer(2), Divide(Multiply(Float(5.0), Negative(Integer(3))), Float(10.0)))
        ]
        expected = [
            42,
            -23,
            5 // 2,
            5 / 2,
            2 + ((5.0 * -3) / 10.0)
        ]"""

    def traverse(self, tree_element: NodeOrLeaf) -> Union[int, float] :
        """This method is an entry point for EvaluateExpression Visitor.

        Args:
            tree_element (NodeOrLeaf): tree element object

        Raises:
            TypeError: Tree element is empty
            ValueError: tree_element.result did not compute correctly
            TypeError: tree_element is wrong type

        Returns:
            Union[int, float]: result of the expression
        """
        if tree_element is None:
            raise TypeError("Node is provided incorrectly")
        if isinstance(tree_element, (ExpressionNode, ExpressionLeaf)):
            self._evaluate(tree_element)
            if tree_element.result is None:
                raise ValueError("Evaluation did not yield a result") 
            return tree_element.result
        else:
            raise TypeError("In EvaluateExpression, tree_element must be ExpressionNode or ExpressionLeaf")

    def _evaluate(self, tree_element: NodeOrLeaf) -> None:
        """This method recursivley evaluates mathematical expression.
        
        Args:
            tree_element (NodeOrLeaf): tree element object

        Raises:
            TypeError: tree_element is empty

        Returns:
            _type_: None
        """
        # Handle the case of a leaf node
        if isinstance(tree_element, ExpressionLeaf):
            return self._evaluate_leaf(tree_element)
        
        # Handle the case of an internal node
        if isinstance(tree_element, ExpressionNode):
            return self._evaluate_node(tree_element)

        raise TypeError("The tree is empty!")
    
    def _evaluate_leaf(self, tree_element: NodeOrLeaf):
        tree_element.accept(self)
    
    def _evaluate_node(self, tree_element: ExpressionNode):
       # Recursively handle the children
        for child in tree_element.children:
            self._evaluate(child)
        #After children are evaluated, node evaluation can be started:
        tree_element.accept(self)
        
    def visit(self, tree_element: NodeOrLeaf) -> None:
        """This method is a visitor for Leaf and Node classes in EvaluateExpression visitor. 
        
        Not used in this EvaluateExpression visitor class.

        Args:
            tree_element (Node or Leaf): The node object.

        Returns:
            pass: not implemented
        """
        pass

    def visitInteger(self, tree_element: Integer) -> None:
        """This method is a visitor for Integer class in EvaluateExpression visitor. 
        
        As the result in ExpressionLeaf objects is automatically assigned in __init__, this visitor class is empty

        Args:
            tree_element (Integer): The Integer object.

        Returns:
            pass: not implemented
        """
        pass

    def visitFloat(self, tree_element: Float) -> None:
        """This method is a visitor for Float class in EvaluateExpression visitor. 
        
        As the result in ExpressionLeaf objects is automatically assigned in __init__, this visitor class is empty

        Args:
            tree_element (Float): The Float object.

        Returns:
            pass: not implemented
        """
        pass



    def visitNegative(self, tree_element: Negative) -> None:
        """This method assigns the Negative node value to -{value_of_its_child}.
        
        eg. Negative(5) = -5

        Args:
            tree_element (Negative): tree element object

        Raises:
            ValueError: The results of the children needs to be calculated first
            TypeError: Wrong children type
        """
        child = tree_element.children[0]
        if isinstance(child, (ExpressionNode, ExpressionLeaf)):
            if child.result is None: 
                raise ValueError('Internal Error, child not yet calculated!')
            negative = child.result - 2*child.result
            tree_element.result = negative
        else:
            raise TypeError('child of Negative is wrong type (not ExpressionNode nor ExpressionLeaf)')

    def visitAdd(self, tree_element: Add) -> None:
        """This method assigns the Add node value to a value of adding its children.
        
        eg. Add(Float(5.0), Integer(10)) = 15.0 


        Args:
            tree_element (Add): tree element object

        Raises:
            TypeError: The results of the children needs to be calculated first
            ValueError: Wrong children type
        """
        addition: Union[int, float] = 0
        for child in tree_element.children:
            if not isinstance(child, (ExpressionNode, ExpressionLeaf)):
                raise TypeError('AddError: Child is not ExpressionNode or ExpressionLeaf')
            if child.result is None:
                raise ValueError('AddError: Child result has not been calculated')
            addition += child.result           
        tree_element.result = addition

    def visitDivide(self, tree_element: Divide) -> None:
        """This method assigns the Division node value to a value of division of its children.

        Args:
            tree_element (Divide): tree element object

        Raises:
            TypeError: The results of the children needs to be calculated first
            ValueError: Wrong children type
        """
        float_division = False              
        divident = tree_element.children[0]
        divisor = tree_element.children[1]
        if not isinstance(divident, (ExpressionNode, ExpressionLeaf)):
            raise TypeError('DivideError: Child is not ExpressionNode or ExpressionLeaf')
        if not isinstance(divisor, (ExpressionNode, ExpressionLeaf)):
            raise TypeError('DivideError: Child is not ExpressionNode or ExpressionLeaf')
        if divident.result is None or divisor.result is None: 
            raise ValueError('DivideError: child.result has not been calculated')

        if isinstance(divident, Float) or isinstance(divisor, Float):
            float_division = True

        if float_division:
            tree_element.result = divident.result / divisor.result
        else:
            tree_element.result = divident.result // divisor.result

    def visitMultiply(self, tree_element: Multiply) -> None:
        """This method assigns the Multiply node value to a value of multiplication of  its children. 
          eg. Multiply(5.0, 10) = 50.0 

        Args:
            tree_element (Multiply): tree element object

        Raises:
            TypeError: The results of the children needs to be calculated first
            ValueError: Wrong children type
        """
        multiplication: Union[int, float] = 1
        for child in tree_element.children:
            if not isinstance(child, (ExpressionNode, ExpressionLeaf)):
                raise TypeError('MultiplyError: Child is not ExpressionNode or ExpressionLeaf')
            if child.result is None:
                raise ValueError('MultiplyError: Child result has not been calculated')
            multiplication *= child.result
        tree_element.result = multiplication

class PrintExpression(Visitor):
    """This class is a visitor used to print out expressions. 
    
    eg:
    expressions = [
            Integer(42),
            Negative(Integer(23)),
            Divide(Integer(5), Integer(2)),
            Divide(Float(5), Integer(2)),
            Add(Integer(2), Divide(Multiply(Float(5.0), Negative(Integer(3))), Float(10.0)))
        ]
        expected = [
            "* Integer(42)",
            "* Negative\n  * Integer(23)",
            "* Divide\n  * Integer(5)\n  * Integer(2)",
            "* Divide\n  * Float(5.0)\n  * Integer(2)",
            "* Add\n  * Integer(2)\n  * Divide\n    * Multiply\n      * Float(5.0)\n      * Negative\n        * Integer(3)\n    * Float(10.0)"
        ]
        """
    def traverse(self, tree_element: ExpressionNodeOrLeaf) -> str:
        """This method is an entry point for PrintExpression Visitor

        Args:
            tree_element (ExpressionNodeOrLeaf): tree element object

        Raises:
            TypeError: Empty tree

        Returns:
            str: Printed expression
        """
        if tree_element is None:
            raise TypeError("Node is provided incorrectly")
        return self._print_logic(tree_element)

    def _print_logic(self, tree_element,  is_last=False) -> str:
        """This method is representing logic of prining out the expressions in a correct manner.
        
        This method is an entry point for the recursive printing algorithm.

        Args:
            tree_element (_type_): tree element object. The type is checked inside the method.
            is_last (bool, optional): _description_. Defaults to False.

        Raises:
            TypeError: The tree element is empty or wrong type (not ExpressionNode nor ExpressionLeaf)

        Returns:
            str: printed expression
        """

        lines = ""
        if is_last:
            lines +=  tree_element.parent.accept(self)

        # Handle the case of a leaf node
        if isinstance(tree_element, ExpressionLeaf):   
            lines += self._handle_leaf(tree_element)
            return lines

        # Handle the case of an internal node
        if isinstance(tree_element, ExpressionNode):
            lines += self._handle_node(tree_element, is_last)
            return lines      
        raise TypeError("The tree is empty or wrong type (not ExpressionNode nor ExpressionLeaf)")

    def _handle_leaf(self, tree_element: ExpressionLeaf) -> str:
        """This method handles returning leaf expression.

        Args:
            tree_element (ExpressionLeaf): tree element object.

        Returns:
            str: leaf value 
        """
        return tree_element.accept(self)

    def _handle_node(self, tree_element: ExpressionNode, is_last: bool) -> str:
        """This method handles returning node expression.

        Args:
            tree_element (ExpressionNode): tree element object
            is_last (bool): Specifies if current tree_element is a last child of its parent

        Returns:
            str: node expression
        """
        # check if this current node has only one child (e.g. Negative node):
        has_only_one_child = 1 == len(tree_element.children)
        prefix = "" if tree_element.parent is None or (has_only_one_child ) else "("
        # Recursively handle the children
        lines = self._handle_node_children(tree_element, is_last)
        return prefix + lines

    def _handle_node_children(self, tree_element: ExpressionNode, is_last: bool) -> str:
        """This method handles returning an expression from the node's children recursively.

        Args:
            tree_element (ExpressionNode): tree element object, parent of the children that are handled here
            is_last (bool): indicator if the tree_element is last child of its parent

        Returns:
            str: expression of the node's children
        """
        lines = ""
        # check if this current node has only one child (e.g. Negative node):
        has_only_one_child = 1 == len(tree_element.children)
        # Recursively handle the children
        for i, child in enumerate(tree_element.children):
            # check if the i'th child of the current node is last:
            is_last_child = i == len(tree_element.children) - 1
            sufix = ")" if is_last and (is_last_child or has_only_one_child) else ""
            lines += self._print_logic(child, is_last_child) + sufix
        return lines
      
    def visit(self, tree_element: NodeOrLeaf) -> None:
        """This method is for handling leaf and Node visits in PrintExpression visitor. Not used in this visitor.

        Args:
            tree_element (NodeOrLeaf): tree element object
        """
        pass

    def visitInteger(self, tree_element: Integer) -> str:
        """This method is handling Integer visits in PrintExpression visitor.

        Args:
            tree_element (Integer): tree element object

        Returns:
            str: result of Integer
        """
        return str(tree_element)

    def visitFloat(self, tree_element: Float) -> str:
        """This method is handling Float visits in PrintExpression visitor.

        Args:
            tree_element (Float): tree element object

        Returns:
            str: result of Float
        """
        return str(tree_element)

    def visitNegative(self, tree_element: Negative) -> str:
        """This method is handling Negative visits in PrintExpression visitor.

        Args:
            tree_element (Negative): tree element object

        Returns:
            str: result of Negative
        """
        return str(tree_element)

    def visitAdd(self, tree_element: Add) -> str:
        """This method is handling Add visits in PrintExpression visitor.

        Args:
            tree_element (Add): tree element object

        Returns:
            str: result of Add
        """
        return str(tree_element)

    def visitDivide(self, tree_element: Divide) -> str:
        """This method is handling Divide visits in PrintExpression visitor.

        Args:
            tree_element (Divide): tree element object

        Returns:
            str: result of Divide
        """
        return str(tree_element)

    def visitMultiply(self, tree_element: Multiply):
        """This method is handling Multiply visits in PrintExpression visitor.

        Args:
            tree_element (Multiply): tree element object

        Returns:
            str: result of Multiply
        """
        return str(tree_element)
