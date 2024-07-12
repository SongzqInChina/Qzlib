cdef class Node:
    cdef bool leaf
    cdef int n
    cdef list keys
    cdef list values
    cdef list children

    cdef void __cinit__(self, leaf=True):
        self.leaf = leaf
        self.n = 0
        self.keys = []
        self.values = []
        self.children = []

    cdef void __del__(self):
        for child in self.children:
            del child

    cdef str __str__(self):
        if self.leaf:
            return f"Leaf Node({dict(zip(self.keys, self.values))})"
        else:
            return f"Internal Node({dict(zip(self.keys, [child.__str__() for child in self.children]))})"


cdef class SearchResult:
    cdef object result
    cdef bool iserror 
    cdef str error_message

    cdef void __cinit__(self, result=None, iserror=False, str error_message=""):
        self.result = result
        self.iserror = iserror
        self.error_message = error_message


class BplusTree:
    cdef Node root
    cdef int t

    cdef void __cinit__(self, int t):
        self.root: Node = Node()
        self.t: int = t

    cdef void split_child(self, Node x, int i):
        y = x.children[i]
        z = Node(leaf=y.leaf)

        # Initialize the new node z
        z.n = self.t - 1
        z.keys = y.keys[self.t:]
        z.values = y.values[self.t:]

        y.keys = y.keys[:self.t]
        y.values = y.values[:self.t]

        if not y.leaf:
            z.children = y.children[self.t:]
            y.children = y.children[:self.t]

        # Insert the new node z into x's children list at position i+1
        x.children.insert(i + 1, z)

        # Move the middle key up to the parent node x
        x.keys.insert(i, y.keys[-1])

        # Increment the number of keys in x
        x.n += 1

    cdef void insert_non_full(self, Node x, k, v):
        cdef i = x.n - 1

        if x.leaf:
            while i >= 0 and k < x.keys[i]:
                x.keys.insert(i + 1, x.keys[i])
                x.values.insert(i + 1, x.values[i])
                i -= 1
            x.keys.insert(i + 1, k)
            x.values.insert(i + 1, v)
            x.n += 1
        else:
            while i >= 0 and k < x.keys[i]:
                i -= 1
            i += 1

            if x.children[i].n == 2 * self.t - 1:
                self.split_child(x, i)
                if k > x.keys[i]:
                    i += 1

            self.insert_non_full(x.children[i], k, v)

    cdef void merge_children(self, Node x, int i):
        y = x.children[i]
        z = x.children[i + 1]

        # Transfer the middle key from x to y
        y.keys.append(x.keys[i])

        # Transfer all keys and children from z to y
        y.keys.extend(z.keys)
        if not y.leaf:
            y.children.extend(z.children)

        # Update the number of keys in y
        y.n += z.n + 1

        # Remove the middle key from x
        x.keys.pop(i)

        # Remove z from x's children list
        x.children.pop(i + 1)

        # Update the number of keys in x
        x.n -= 1

        # Delete the merged node z
        del z

    cdef void redistribute_key(self, Node x, int i):
        y = x.children[i]
        z = x.children[i + 1]

        if y.n < self.t:
            # Move a key from z to y
            y.keys.append(x.keys[i])
            y.n += 1

            # Move a key from z to x
            x.keys[i] = z.keys.pop(0)

            # Move a child from z to y, if applicable
            if not y.leaf:
                y.children.append(z.children.pop(0))

            z.n -= 1
        else:
            # Move a key from y to x
            x.keys[i] = y.keys.pop()

            # Move a key from y to z
            z.keys = y.keys[self.t:] + z.keys
            if not z.leaf:
                z.children = y.children[self.t + 1:] + z.children

            # Update y
            y.keys = y.keys[:self.t]
            y.children = y.children[:self.t + 1]
            y.n = self.t

            # Update z
            z.n = self.t

    cdef void insert(self, object k, object v):
        if self.root.n == 2 * self.t - 1:
            s = Node(leaf=False)
            s.children.append(self.root)
            self.split_child(s, 0)
            self.insert_non_full(s, k, v)
            self.root = s
        else:
            self.insert_non_full(self.root, k, v)

    cdef void remove(self, object k):
        cdef Node x = self.root
        cdef bool found = False

        while x is not None:
            cdef int i = 0
            while i < x.n and k > x.keys[i]:
                i += 1

            if i < x.n and k == x.keys[i]:
                found = True
                break

            if not x.leaf:
                x = x.children[i]
            else:
                break

        if not found:
            return

        i = 0
        while i < x.n and k > x.keys[i]:
            i += 1
        x.keys.pop(i)
        x.values.pop(i)
        x.n -= 1

        if x.n < self.t and x.parent is not None:
            cdef int sibling_index = -1
            cdef sibling = None
            if i != 0:
                sibling_index = i - 1
                sibling = x.parent.children[sibling_index]
            elif i < x.n:
                sibling_index = i
                sibling = x.parent.children[sibling_index]

            if sibling is not None and sibling.n >= self.t:
                self.redistribute_key(x.parent, sibling_index)
            else:
                if sibling_index != -1:
                    self.merge_children(x.parent, sibling_index)
                else:
                    self.merge_children(x.parent, i)

                if x.parent.n == 0:
                    self.root = x
                    del x.parent

    cdef SearchResult search(self, object k):
        cdef Node x = self.root
        while not x.leaf:
            cdef int i = 0
            while i < x.n and k > x.keys[i]:
                i += 1
            x = x.children[i]  # Continue down the tree until reaching a leaf node

        # Now x is a leaf node, perform the search on this node
        cdef int i = 0
        while i < x.n and k > x.keys[i]:
            i += 1
        if i < x.n and k == x.keys[i]:
            return SearchResult(result=x.values[i])
        else:
            return SearchResult(result=None)  # Key not found
