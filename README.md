# tree-structure
Tree structure using Visitor Pattern

To run the unit tests: 
```python
python -m unittest tree_test.py  
```
## Functionality
### Printing the tree in folder-like structure
In:
```python
Node("Scene", Node("Robot", Node("Flange", Node("Gripper", Leaf("Object"))), Leaf("Camera")), Node("Table", Leaf("Box")))
```
Out:
```python
 ╿ Scene
 ├─┮ Robot
 │ ├─┮ Flange
 │ │ └─┮ Gripper
 │ │   └─╼ Object
 │ └─╼ Camera
 └─┮ Table
   └─╼ Box
 ```

See 
 <a href="https://github.com/Piotrzems/tree-structure/blob/c071b90970a3c57d87e8b60bb5760aafcb97ec3e/tree_test.py#L80">test_print_visitor_tree</a> function from tree_test.py for more details.

### Printing mathematical expressions
In:
```python
Add(Integer(2), Divide(Multiply(Float(5.0), Negative(Integer(3))), Float(10.0)))
```
Out:
```python
2 + ((5.0 * -3) / 10.0)
```

See 
 <a href="https://github.com/Piotrzems/tree-structure/blob/c071b90970a3c57d87e8b60bb5760aafcb97ec3e/tree_test.py#L99">test_print_expression_tree</a> function from tree_test.py for more details.
### Evaluating mathematical expressions
In:
```python
Add(Integer(2), Divide(Multiply(Float(5.0), Negative(Integer(3))), Float(10.0)))
```
Out:
```python
2 + ((5.0 * -3) / 10.0) = 0.5
```
See 
 <a href="https://github.com/Piotrzems/tree-structure/blob/c071b90970a3c57d87e8b60bb5760aafcb97ec3e/tree_test.py#L137">test_evaluate_expression_tree</a> function from tree_test.py for more details.

