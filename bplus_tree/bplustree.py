class Node:
    def __init__(self, leaf=True):
        self.leaf = leaf
        self.n = 0
        self.keys = []
        self.values = []
        self.children = []

    def __del__(self):
        for child in self.children:
            del child

    def __str__(self):
        if self.leaf:
            return f"Leaf Node({dict(zip(self.keys, self.values))})"
        else:
            return f"Internal Node({dict(zip(self.keys, [child.__str__() for child in self.children]))})"


class SearchResult:
    def __init__(self, result=None, iserror=False, error_message=""):
        self.result = result
        self.iserror = iserror
        self.error_message = error_message


class BplusTree:
    def __init__(self, t):
        self.root = Node()
        self.t = t

    def split_child(self, x, i):
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

    def insert_non_full(self, x, k, v):
        i = x.n - 1

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

    def merge_children(self, x, i):
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

    def redistribute_key(self, x, i):
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

    def insert(self, k, v):
        if self.root.n == 2 * self.t - 1:
            s = Node(leaf=False)
            s.children.append(self.root)
            self.split_child(s, 0)
            self.insert_non_full(s, k, v)
            self.root = s
        else:
            self.insert_non_full(self.root, k, v)

    def remove(self, k):
        x = self.root
        found = False

        while x is not None:
            i = 0
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
            sibling_index = -1
            sibling = None
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

    def search(self, k):
        x = self.root
        while not x.leaf:
            i = 0
            while i < x.n and k > x.keys[i]:
                i += 1
            x = x.children[i]  # Continue down the tree until reaching a leaf node

        # Now x is a leaf node, perform the search on this node
        i = 0
        while i < x.n and k > x.keys[i]:
            i += 1
        if i < x.n and k == x.keys[i]:
            return SearchResult(result=x.values[i])
        else:
            return SearchResult(result=None)  # Key not found
