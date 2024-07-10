from typing import Any, Iterable

import numpy as np


class MutableTuple:
    def __init__(self, *args):
        # append
        # clear
        # copy
        # count
        # extend
        # index
        # insert
        # pop
        # remove
        # reverse
        # sort
        self.np_data = np.array(args)

    def append(self, value):
        self.np_data = np.append(self.np_data, value)

    def clear(self):
        self.np_data = np.array([])

    def copy(self):
        return MutableTuple(*self.np_data)

    def count(self, value):
        return np.sum(self.np_data == value)

    def extend(self, iterable: Iterable):
        self.np_data = np.append(self.np_data, np.array(iterable))



class Node:
    def __init__(self, is_init=False):
        self.leaf = True
        self.n = 0
        self.keys = np.full([10], Node)
        self.values = np.full([10], Node)
        self.children = np.full([10], Node)
        self.is_init = is_init

    def init(self):
        self.is_init = True


class SeatchResult:
    result = None
    iserror: bool = False

    def __init__(self, result, is_error):
        self.result = result
        self.iserror = is_error


class BplusTree:

    def __init__(self, t):
        self.root = np.full([10], Node)
        self.t = t

    def split_child(self, x: Node, i: int):
        y = x.children[i]  # type: Node
        z = Node(True)
        z.leaf = y.leaf
        z.n = self.t - 1

        for j in range(self.t - 1):
            z.keys[j] = y.keys[j + self.t]

        if not y.leaf:
            for j in range(self.t):
                z.children[j] = y.children[j + self.t]

        y.n = self.t - 1

        j = x.n
        while j > i:
            x.children[j] = x.children[j - 1]
            j -= 1

        x.children[i + 1] = z

        x.keys[i] = y.keys[self.t - 1]

        x.n += 1

        y.n = self.t - 1

    def insert_non_full(self, x: Node, key, value):
        i = x.n - 1

        if x.leaf:
            while i >= 0 and key < x.keys[i]:
                x.keys[i + 1] = x.keys[i]
                x.values[i + 1] = x.values[i]
                i -= 1
            x.keys[i + 1] = key
            x.values[i + 1] = value
            x.n += 1

        else:
            while i >= 0 and key < x.keys[i]:
                i -= 1
            i += 1

            if x.children[i].n == 2 * self.t - 1:
                self.split_child(x, i)
                if key > x.keys[i]:
                    i += 1
            self.insert_non_full(x.children[i], key, value)

    def merge_children(self, x: Node, i: int):
        y = x.children[i]  # type: Node
        z = x.children[i + 1]  # type: Node

        y.keys[self.t - 1] = x.keys[i]

        for j in range(self.t):
            y.children[j + self.t] = z.children[j]

        if not y.leaf:
            for j in range(self.t + 1):
                y.children[j + self.t] = z.children[j]

        y.n += self.t + 1

        for j in range(i, x.n - 1):
            x.keys[j] = x.keys[j + 1]

        for j in range(i + 1, x.n):
            x.children[j] = x.children[j + 1]

        x.n -= 1

        del z

        for j in range(y.n + 1):
            if y.children[j] is not None:
                y.children[j].parent = y

    def redistribute_key(self, x: Node, i):
        pass

    def insert(self, key, value):
        pass

    def remove(self, key):
        pass

    def search(self, key) -> SeatchResult:
        pass
