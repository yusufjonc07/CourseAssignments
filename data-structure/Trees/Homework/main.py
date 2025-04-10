class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BinaryTree:
    def __init__(self):
        self.root = None

    def add_node(self, value):
        if self.root is None:
            self.root = Node(value)
        else:
            self._insert(self.root, value)

    def _insert(self, current, value):
        if value < current.value:
            if current.left is None:
                current.left = Node(value)
            else:
                self._insert(current.left, value)
        else:
            if current.right is None:
                current.right = Node(value)
            else:
                self._insert(current.right, value)

    def preorder(self, node):
        if node is None:
            return []
        return [node.value] +\
            self.preorder(node.left) +\
            self.preorder(node.right)


tree = BinaryTree()

for num in [23, 45, 98, 34, 12, 43, 90, 21, 87]:
    tree.add_node(num)
    
print("Preorder:", tree.preorder(tree.root))