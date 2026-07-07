# id1: 218821718
# name1: Uri Aviram
# username1: uriaviram
# id2: 334758984
# name2: Bar Nahari
# username2: barnahari


"""A class representing a node in an AVL tree"""

#bar do you see that
#no

class AVLNode(object):
    """Constructor, you are allowed to add more fields.

    @type key: int
    @param key: key of your node
    @type value: string
    @param value: data of your node
    """

    def __init__(self, key, value, is_real = True):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.height = 0 if is_real else -1
        self.bf = 0
        self.is_real = is_real

    """returns whether self is not a virtual node 

    @rtype: bool
    @returns: False if self is a virtual node, True otherwise.
    """

    def is_real_node(self):
        return self.is_real


"""
A class implementing an AVL tree.
"""


class AVLTree(object):
    """
    Constructor, you are allowed to add more fields.

    @type is_avl: boolean
    @param is_avl: If True then tree is AVL, otherwise it is just a "regular" binary search tree, without rotations.
    """

    def __init__(self, is_avl= True):
        self.fakeNode = AVLNode(None, None, False)
        self.root = self.fakeNode
        self.root.parent = self.fakeNode
        self.Size = 0
        self.is_avl = is_avl

    """searches for a node in the dictionary corresponding to the key (starting at the root)

    @type key: int
    @param key: a key to be searched
    @rtype: (AVLNode,int)
    @returns: a tuple (x, search_time) where x is the node corresponding to key (or None if not found)
    and search_time is the search time, as defined and explained in the assignment.
    """

    def search(self, key):
        search_time = 1
        if not self.root.is_real:
            return None, 1
        node = self.root
        while node.is_real:
            if node.key == key:
                return node, search_time
            if key < node.key:
                node = node.left
            else:
                node = node.right
            search_time += 1
        return None, search_time

    """inserts a new node into the dictionary with corresponding key and value (starting at the root)

    @type key: int
    @pre: key currently does not appear in the dictionary
    @param key: key of item that is to be inserted to self
    @type val: string
    @param val: the value of the item
    @rtype: (AVLNode,int,int,int)
    @returns: a 4-tuple (x, search_time, rotations, height_changes), where x is the new node
    and the other 3 return values are as defined and explained in the assignment.
    """

    def insert(self, key, val):
        search_time = 2
        rotations = 0
        height_changes = 0
        new_node = None
        if not self.root.is_real:
            self.root = AVLNode(key, val)
            self.root.left = self.fakeNode
            self.root.right = self.fakeNode
            self.root.parent = self.fakeNode
            self.Size += 1
            return self.root, search_time, rotations, height_changes


        node = self.root
        while True:
            if key < node.key:
                if not node.left.is_real:
                    new_node = AVLNode(key, val)
                    node.left = new_node
                    break
                else:
                    node = node.left
            else:
                if not node.right.is_real:
                    new_node = AVLNode(key, val)
                    node.right = new_node
                    break
                else:
                    node = node.right
            search_time += 1

        new_node.left = self.fakeNode
        new_node.right = self.fakeNode
        new_node.parent = node
        self.Size += 1

        node = new_node

        if self.is_avl:
            while node is not self.root:
                node = node.parent
                old_height = node.height
                node.height = 1 + max(node.left.height, node.right.height)
                node.bf = node.left.height - node.right.height
                if abs(node.bf) < 2:
                    if node.height != old_height:
                        height_changes += 1
                    else:
                        break
                else:
                    if node.bf == 2:
                        if node.left.bf == -1:
                            self.rotate_left(node.left)
                            rotations += 1
                        self.rotate_right(node)
                        rotations += 1
                    else:
                        if node.right.bf == 1:
                            self.rotate_right(node.right)
                            rotations += 1
                        self.rotate_left(node)
                        rotations += 1

        return new_node, search_time, rotations, height_changes












    """deletes node from the dictionary

    @type node: AVLNode
    @pre: node is a real pointer to a node in self
    """

    def delete(self, node):
        if not node.is_real:
            return

        if not node.left.is_real and not node.right.is_real: #leaf
            if node == self.root:
                self.root = self.fakeNode
                self.Size -= 1
                node.parent = None
                return
            elif node == node.parent.left:
                node.parent.left = self.fakeNode
            else:
                node.parent.right = self.fakeNode
            self.Size -= 1

        elif not node.left.is_real or not node.right.is_real:
            child = node.left if node.left.is_real else node.right
            if node == self.root:
                self.root = child
                child.parent = self.fakeNode
                self.Size -= 1
                return
            elif node == node.parent.left:
                node.parent.left = child
                child.parent = node.parent
            else:
                node.parent.right = child
                child.parent = node.parent
            self.Size -= 1
        else:
            successor = node.right
            while successor.left.is_real:
                successor = successor.left

            node.key, successor.key = successor.key, node.key
            node.value, successor.value = successor.value, node.value

            self.delete(successor)


        while node is not self.root:
            if node.parent.left is None or node.parent.right is None:
                pass
            node = node.parent

            node.height = 1 + max(node.left.height, node.right.height)
            old_bf = node.bf
            node.bf = node.left.height - node.right.height
            if node.bf == old_bf:
                break
            if self.is_avl and abs(node.bf) > 1:
                if node.bf == 2:
                    if node.left.bf == -1:
                        self.rotate_left(node.left)
                    self.rotate_right(node)
                else:
                    if node.right.bf == 1:
                        self.rotate_right(node.right)
                    self.rotate_left(node)









    """returns a list representing dictionary 

    @rtype: list
    @returns: a list of (key, value) tuples sorted by key, representing the data structure
    """

    def avl_to_list(self):
        def avl_to_list_rec(node):
            if not node.is_real:
                return []
            return avl_to_list_rec(node.left) + [(node.key, node.value)] + avl_to_list_rec(node.right)
        return avl_to_list_rec(self.root)


    """returns the number of items in dictionary 

    @rtype: int
    @returns: the number of items in dictionary 
    """

    def size(self):
        return self.Size

    """returns the root of the tree representing the dictionary

    @rtype: AVLNode
    @returns: the root, None if the dictionary is empty
    """

    def get_root(self):
        return self.root

    """returns the height of the tree

        @rtype: int
        @returns: the height of the tree 
        """

    def get_height(self):
        if self.is_avl:
            return self.root.height if self.root.is_real else -1

        if not self.root.is_real:
            return -1

        max_depth = -1
        stack = [(self.root, 0)]  # (node, depth)

        while stack:
            node, depth = stack.pop()
            if not node.is_real:
                max_depth = max(max_depth, depth - 1)
                continue

            stack.append((node.left, depth + 1))
            stack.append((node.right, depth + 1))

        return max_depth



    def rotate_right(self, node):
        new_root = node.left
        node.left = new_root.right
        new_root.right.parent = node
        new_root.parent = node.parent
        if not node.parent.is_real:
            self.root = new_root
        elif node == node.parent.right:
            node.parent.right = new_root
        else:
            node.parent.left = new_root
        new_root.right = node
        node.parent = new_root

        # Update heights and balance factors
        node.height = 1 + max(node.left.height, node.right.height)
        new_root.height = 1 + max(new_root.left.height, new_root.right.height)
        node.bf = node.left.height - node.right.height
        new_root.bf = new_root.left.height - new_root.right.height


    def rotate_left(self, node):
        new_root = node.right
        node.right = new_root.left
        new_root.left.parent = node
        new_root.parent = node.parent
        if not node.parent.is_real:
            self.root = new_root
        elif node == node.parent.left:
            node.parent.left = new_root
        else:
            node.parent.right = new_root
        new_root.left = node
        node.parent = new_root

        # Update heights and balance factors
        node.height = 1 + max(node.left.height, node.right.height)
        new_root.height = 1 + max(new_root.left.height, new_root.right.height)
        node.bf = node.left.height - node.right.height
        new_root.bf = new_root.left.height - new_root.right.height
