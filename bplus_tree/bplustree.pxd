# bplustree.pxd

ctypedef struct Node:
    bool leaf
    int n
    vector[object] keys
    vector[object] values
    vector[Node*] children

ctypedef struct SearchResult:
    object result
    bool iserror
    string error_message

ctypedef struct BplusTree:
    pass  # 假设BplusTree没有公开的成员变量

cdef extern from "method.cpp" namespace "std":
    ctypedef struct Node:
        Node()
        ~Node()

    ctypedef struct SearchResult:
        SearchResult(object value)
        SearchResult(bool error, string error_message)

    ctypedef struct BplusTree:
        BplusTree(int t)
        ~BplusTree()
        void insert(object k, object v)
        void remove(object k)
        SearchResult search(object k)
