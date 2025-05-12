import time
from tree_visual import TreeVisual
class Node:
    def __init__(self, value):
        self.value = value
        self.left: Node = None
        self.right: Node = None
        self.height = 1  # New nodes start with height 1

class AVLTree(TreeVisual):
    def __init__(self):
        self.root = None

    def insert(self, root, key):
        # 1. Normal BST insert
        if not root:
            return Node(key)
        elif key < root.value:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)

        # 2. Update height
        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))

        # 3. Check balance
        balance = self.get_balance(root)

        # 4. Balance tree with rotations
        # Left Left Case
        if balance > 1 and key < root.left.value:
            return self.rotate_right(root)

        # Right Right Case
        if balance < -1 and key > root.right.value:
            return self.rotate_left(root)

        # Left Right Case
        if balance > 1 and key > root.left.value:
            root.left = self.rotate_left(root.left)
            return self.rotate_right(root)

        # Right Left Case
        if balance < -1 and key < root.right.value:
            root.right = self.rotate_right(root.right)
            return self.rotate_left(root)

        return root

    def get_height(self, node):
        return node.height if node else 0

    def get_balance(self, node):
        return self.get_height(node.left) - self.get_height(node.right) if node else 0

    def rotate_left(self, z):
        y = z.right
        T2 = y.left

        # Perform rotation
        y.left = z
        z.right = T2

        # Update heights
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def rotate_right(self, z):
        y = z.left
        T3 = y.right

        # Perform rotation
        y.right = z
        z.left = T3

        # Update heights
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def build_tree(self, values):
        for val in values:
            self.root = self.insert(self.root, val)
            self.print_tree()
            time.sleep(1)

