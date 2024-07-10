from libc.stdio cimport FILE
from libcpp.vector cimport vector
from libcpp.string cimport string

cdef extern from "method.cpp":
    pass # Include the declarations from the .pxd file here

cdef class PyBplusTree:
    cdef BplusTree* thisptr

    def __cinit__(self, int t):
        self.thisptr = new BplusTree(t)

    def __dealloc__(self):
        del self.thisptr

    def insert(self, Key k, Value v):
        self.thisptr.insert(k, v)

    def remove(self, Key k):
        self.thisptr.remove(k)

    def search(self, Key k):
        cdef SearchResult res = self.thisptr.search(k)
        if res.iserror:
            raise ValueError(res.error_message)
        return res.result