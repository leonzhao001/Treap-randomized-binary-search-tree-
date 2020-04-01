import random

class Node:
    def __init__(self, key: int):
        self.key = key
        self.size = 1
        self.left = None
        self.right = None

class RandomizedBST:
    def __init__(self):
        self.root = None

    # Is the given tree empty   
    def empty(self):
        return self.root is None

    # Returns whether the given number is in the tree.
    def _member(self, t, k):
        if t is None: return False
        elif k < t.key : return self._member(t.left, k)
        elif k > t.key : return self._member(t.right, k)
        else: return True

    def member(self, k):
        return self._member(self.root, k)

    # Gets the size of a (possibly empty) tree.
    def _size(self, t):
        return t.size if t is not None else 0

    # Creates a new singleton tree with the given value.
    def _new_node(self, k):
        return Node(k)

    # Sets the size of a node from the sizes of the immediate subtrees.
    def _fix_size(self, t):
        t.size = 1 + self._size(t.left) + self._size(t.right)

    # Inserts a key as a leaf, returning the modified tree.
    # (This insertion operation will produce a severely imbalanced
    # tree if the keys are inserted in sorted order.)
    def leaf_insert(self, t, k):
        if t is None: return self._new_node(k)
        elif k < t.key:
            t.left = self.leaf_insert(t.left, k)
            self._fix_size(t)
            return t
        elif k > t.key:
            t.right = self.leaf_insert(t.right, k)
            self._fix_size(t)
            return t
        else: return t

    # Performs a right rotation.
    # PRECONDITION: `d` and `d.left` are nodes
    def _rotate_right(self, d):
        b = d.left
        d.left = b.right
        b.right = d
        self._fix_size(d)
        self._fix_size(b)
        return b

    # Performs a left rotation.
    # PRECONDITION: `b` and `b.right` are nodes
    def _rotate_left(self, b):
        d = b.right
        b.right = d.left
        d.left = b
        self._fix_size(b)
        self._fix_size(d)
        return d

    # Inserts an element at the root, returning the modified tree.
    # (This insertion operation will produce a severely imbalanced
    # tree if the keys are inserted in sorted order.)
    def _root_insert(self, t, k):
        if t is None: return self._new_node(k)
        elif k < t.key:
            t.left = self._root_insert(t.left, k)
            return self._rotate_right(t)
        elif k > t.key:
            t.right = self._root_insert(t.right, k)
            return self._rotate_left(t)
        else: return t

    # Inserts an element, maintaining randomness and returning the modified tree.
    def _insert(self, t, k):
        if t is None: return self._new_node(k)
        elif random.randint(0, self._size(t) + 1) == 0:
            return self._root_insert(t, k)
        elif k < t.key:
            t.left = self._insert(t.left, k)
            self._fix_size(t)
            return t
        elif k > t.key:
            t.right = self._insert(t.right, k)
            self._fix_size(t)
            return t
        else: return t

    def insert(self, k):
        self.root = self._insert(self.root, k)

    # Joins two trees, assuming all the keys of the first are less than
    # all the keys of the second.
    def _join(self, t1, t2):
        if t1 is None: return t2
        elif t2 is None: return t1
        elif random.randint(0, self._size(t1) + self._size(t2)) < self._size(t1):
            t1.right = self._join(t1.right, t2)
            self._fix_size(t1)
            return t1
        else:
            t2.left = self._join(t1, t2.left)
            self._fix_size(t2)
            return t2

    # Deletes an element from a tree, returning the modified tree.
    def _delete(self, t, k):
        if t is None: return t
        elif k < t.key:
            t.left = self._delete(t.left, k)
            self._fix_size(t)
            return t
        elif k > t.key:
            t.right = self._delete(t.right, k)
            self._fix_size(t)
            return t
        else:
            return self._join(t.left, t.right)

    def delete(self, k):
        self.root = self._delete(self.root, k)

    # Returns the height (max depth) of a tree.
    def _tree_height(self, t):
        if t is None: return 0
        else: return 1 + max(self._tree_height(t.left), self._tree_height(t.right))

    def height(self):
        return self._tree_height(self.root)

    # Pretty-prints a tree. 
    def print_tree(self):
        def rec(t, n_spaces):
            if t is None: return
            print(' '*n_spaces, 'key:', t.key , 'size:', t.size , 'height:', self._tree_height(t))
            rec(t.left, n_spaces + 2)
            rec(t.right, n_spaces + 2)
        rec(self.root, 0)

if __name__ == '__main__':
    # Builds a random tree of `n` elements, using `f` to produce each element
    def sample(n,f):
        result = RandomizedBST()
        for i in range(n):
            result.insert(f(i))
        result.print_tree()
        print ('Height:',result.height())

    sample(100, lambda x: x)


