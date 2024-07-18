# bplustree.pyx
from libcpp.vector cimport vector
from libcpp.string cimport string

cdef extern from "method.cpp":
    pass  # 不需要在这里重复类型定义，因为已经在.pxd中定义了

# Python bindings for BplusTree
cdef class BPlusTree:
    cdef BplusTree* thisptr

    def __cinit__(self, int t):
        self.thisptr = new BplusTree(t)

    def __dealloc__(self):
        del self.thisptr

    def insert(self, object k, object v):
        self.thisptr.insert(k, v)

    def remove(self, object k):
        self.thisptr.remove(k)

    def search(self, object k):
        cdef SearchResult res = self.thisptr.search(k)
        if res.iserror:
            raise ValueError(res.error_message)
        else:
            return res.result
