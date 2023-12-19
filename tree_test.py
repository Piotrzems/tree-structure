import unittest
import inspect

from tree import Leaf, Node, Visitor
from print_tree import PrintTree, NodeStyle
from expr_tree import EvaluateExpression, PrintExpression, Add, Integer, Divide, Multiply, Float, Negative

functionality_tests_off = False

class TestTree(unittest.TestCase):

    def test_tree_data_structure(self):
        with self.subTest(i=1):
            leaf = Leaf("TestLeaf")
            self.assertEqual(leaf.name, "TestLeaf")
            self.assertEqual(leaf.parent, None)

        with self.subTest(i=2):
            node = Node("TestNode", Leaf("1"), Leaf("2"))
            self.assertEqual(node.name, "TestNode")
            self.assertEqual(node.parent, None)
            self.assertEqual(len(node.children), 2)
            for c in node.children:
                self.assertEqual(c.parent, node)

        with self.subTest(i=3):
            with self.assertRaises(TypeError):
                node = Node("ErrorNode")

    def test_visitor_data_structure(self):
        with self.subTest(i=1):
            self.assertTrue(inspect.isfunction(Visitor.traverse))  # entry point
            self.assertTrue(inspect.isfunction(Visitor.visit))
            self.assertTrue(inspect.isfunction(Leaf.accept))
            self.assertTrue(inspect.isfunction(Node.accept))

        with self.subTest(i=2):
            self.assertTrue(issubclass(PrintTree, Visitor))
            self.assertTrue(issubclass(PrintExpression, Visitor))
            self.assertTrue(issubclass(EvaluateExpression, Visitor))

    @unittest.skipIf(functionality_tests_off, "toggled off by user")
    def test_print_visitor_indent(self):
        
        trees = [
            Leaf("Scene"),
            Node("Scene", Leaf("Table"), Leaf("Object")),
            Node("Scene", Node("Robot", Node("Flange", Node("Gripper", Leaf("Object"))), Leaf("Camera")), Node("Table", Leaf("Box")))
        ]
        expected = [
            "Scene",
            "Scene\n  Table\n  Object",
            "Scene\n  Robot\n    Flange\n      Gripper\n        Object\n    Camera\n  Table\n    Box"
        ]
        visitor = PrintTree(NodeStyle.INDENT)

        for i, c in enumerate(zip(trees, expected)):
            with self.subTest(i=i):
                self.assertEqual(visitor.traverse(c[0]), c[1])

    @unittest.skipIf(functionality_tests_off, "toggled off by user")
    def test_print_visitor_bullet(self):
        trees = [
            Leaf("Scene"),
            Node("Scene", Leaf("Table"), Leaf("Object")),
            Node("Scene", Node("Robot", Node("Flange", Node("Gripper", Leaf("Object"))), Leaf("Camera")), Node("Table", Leaf("Box")))
        ]
        expected = [
            "* Scene",
            "* Scene\n  * Table\n  * Object",
            "* Scene\n  * Robot\n    * Flange\n      * Gripper\n        * Object\n    * Camera\n  * Table\n    * Box"
        ]
        visitor = PrintTree(NodeStyle.BULLET)

        for i, c in enumerate(zip(trees, expected)):
            with self.subTest(i=i):
                self.assertEqual(visitor.traverse(c[0]), c[1])

    @unittest.skipIf(functionality_tests_off, "toggled off by user")
    def test_print_visitor_tree(self):
        trees = [
            Leaf("Scene"),
            Node("Scene", Leaf("Table"), Leaf("Object")),
            Node("Scene", Node("Robot", Node("Flange", Node("Gripper", Leaf("Object"))), Leaf("Camera")), Node("Table", Leaf("Box")))
        ]
        expected = [
            "─╼ Scene",
            " ╿ Scene\n ├─╼ Table\n └─╼ Object",
            " ╿ Scene\n ├─┮ Robot\n │ ├─┮ Flange\n │ │ └─┮ Gripper\n │ │   └─╼ Object\n │ └─╼ Camera\n └─┮ Table\n   └─╼ Box"
        ]
        visitor = PrintTree(NodeStyle.TREE)

        for i, c in enumerate(zip(trees, expected)):
            with self.subTest(i=i):
                self.assertEqual(visitor.traverse(c[0]), c[1])
                

    @unittest.skipIf(functionality_tests_off, "toggled off by user")
    def test_print_expression_tree(self):
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
        visitor = PrintTree(NodeStyle.BULLET)

        for i, c in enumerate(zip(expressions, expected)):
        
            with self.subTest(i=i):
                self.assertEqual(visitor.traverse(c[0]), c[1])

        expected = [
            "42",
            "-23",
            "5 / 2",
            "5.0 / 2",
            "2 + ((5.0 * -3) / 10.0)"
        ]

        visitor = PrintExpression()
        for i, c in enumerate(zip(expressions, expected)):     
            with self.subTest(i=i + len(expressions)):
                self.assertEqual(visitor.traverse(c[0]), c[1])

                

    @unittest.skipIf(functionality_tests_off, "toggled off by user")
    def test_evaluate_expression_tree(self):
        expressions = [
            Integer(42),
            Negative(Integer(23)),
            Divide(Integer(5), Integer(2)),
            Divide(Float(5), Integer(2)),
            Add(Integer(2), Divide(Multiply(Float(5.0), Negative(Integer(3))), Float(10.0))),
            Negative( Add(Integer(2),Integer(3)) ),  # ----- MY TESTS -----
            Add(Integer(2),Integer(3)),
        ]
        expected = [
            42,
            -23,
            5 // 2,
            5 / 2,
            2 + ((5.0 * -3) / 10.0),
            -(2 + 3),
            2 + 3,
        ]
        visitor = EvaluateExpression()

        for i, c in enumerate(zip(expressions, expected)):
            with self.subTest(i=i):
                self.assertEqual(visitor.traverse(c[0]), c[1])
                

        expected = [
            "42 = 42",
            "-23 = -23",
            "5 / 2 = 2",
            "5.0 / 2 = 2.5",
            "2 + ((5.0 * -3) / 10.0) = 0.5",
            "-(2 + 3) = -5",
            "2 + 3 = 5"
        ]

        visitor1 = PrintExpression()
        visitor2 = EvaluateExpression()
        for i, c in enumerate(zip(expressions, expected)):
            with self.subTest(i=i + len(expressions)):
                self.assertEqual(f"{visitor1.traverse(c[0])} = {visitor2.traverse(c[0])}", c[1])
