cdef extern from "method.cpp":
    ctypedef struct Node:
        bint leaf
        int n
        vector[Key] keys
        vector[Value] values
        vector[Node*] children

    ctypedef struct SearchResult:
        T result
        bint iserror
        string error_message

    ctypedef class BplusTree:
        cdef Node* root
        cdef int t

        cdef void splitChild(Node* x, int i)
        cdef void insertNonFull(Node* x, Key k, Value v)
        cdef void mergeChildren(Node* x, int i)
        cdef void redistributeKey(Node* x, int i)
        cdef void insert(Key k, Value v)
        cdef void remove(Key k)
        cdef SearchResult search(Key k)

        BplusTree(int t_)
        ~BplusTree()