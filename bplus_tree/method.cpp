#include <vector>
#include <iostream>

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

template<typename Key, typename Value>
struct Node {
    bool leaf = true;
    int n = 0;
    std::vector<Key> keys;
    std::vector<Value> values;
    std::vector<Node<Key, Value>*> children;

    Node() {}
    ~Node() {
        for (auto& child : children) delete child;
    }
};

template<typename T>
struct SearchResult{
    T result;
    bool iserror = false;
    string error_message;
    SearchResult(T value): result(value){}
    SearchResult(bool error, string error_message):
        iserror(error), error_message(error_message) {}
};

template<typename Key, typename Value>
class BplusTree {
private:
    Node<Key, Value>* root;
    int t;

    void splitChild(Node<Key, Value>* x, int i);
    void insertNonFull(Node<Key, Value>* x, const Key& k, const Value& v);
    void mergeChildren(Node<Key, Value>* x, int i);
    void redistributeKey(Node<Key, Value>* x, int i);

public:
    BplusTree(int t_) : t(t_), root(new Node<Key, Value>()) {}
    ~BplusTree() { delete root; }

    void insert(const Key& k, const Value& v);
    void remove(const Key& k);
    SearchResult<Value> search(const Key& k);
};

template<typename Key, typename Value>
void BplusTree<Key, Value>::splitChild(Node<Key, Value>* x, int i) {
    Node<Key, Value>* y = x->children[i];
    Node<Key, Value>* z = new Node<Key, Value>;
    
    // Initialize the new node z
    z->leaf = y->leaf;
    z->n = t - 1;

    // Copy the last t-1 keys from y to z
    for (int j = 0; j < t - 1; ++j) {
        z->keys[j] = y->keys[j + t];
    }

    // Copy the last t children from y to z, if y is not a leaf
    if (!y->leaf) {
        for (int j = 0; j < t; ++j) {
            z->children[j] = y->children[j + t];
        }
    }

    // Update the number of keys in y
    y->n = t - 1;

    // Insert the new node z into x's children list at position i+1
    for (int j = x->n; j > i; --j) {
        x->children[j] = x->children[j - 1];
    }
    x->children[i + 1] = z;

    // Move the middle key up to the parent node x
    x->keys[i] = y->keys[t - 1];

    // Increment the number of keys in x
    x->n++;

    // Adjust the number of keys in y
    y->n = t - 1;
}

template<typename Key, typename Value>
void BplusTree<Key, Value>::insertNonFull(Node<Key, Value>* x, const Key& k, const Value& v) {
    int i = x->n - 1;
    
    if (x->leaf) {
        while (i >= 0 && k < x->keys[i]) {
            x->keys[i + 1] = x->keys[i];
            x->values[i + 1] = x->values[i];
            i--;
        }
        x->keys[i + 1] = k;
        x->values[i + 1] = v;
        x->n++;
    } else {
        while (i >= 0 && k < x->keys[i]) {
            i--;
        }
        i++;
        
        if (x->children[i]->n == 2 * t - 1) {
            splitChild(x, i);
            if (k > x->keys[i]) {
                i++;
            }
        }
        
        insertNonFull(x->children[i], k, v);
    }
}
template<typename Key, typename Value>
void BplusTree<Key, Value>::mergeChildren(Node<Key, Value>* x, int i) {
    Node<Key, Value>* y = x->children[i];
    Node<Key, Value>* z = x->children[i + 1];
    
    // Transfer the middle key from x to y
    y->keys[t - 1] = x->keys[i];
    
    // Transfer all keys and children from z to y
    for (int j = 0; j < t; ++j) {
        y->keys[j + t] = z->keys[j];
    }
    
    if (!y->leaf) {
        for (int j = 0; j <= t; ++j) {
            y->children[j + t] = z->children[j];
        }
    }
    
    // Update the number of keys in y
    y->n += t + 1;
    
    // Remove the middle key from x
    for (int j = i; j < x->n - 1; ++j) {
        x->keys[j] = x->keys[j + 1];
    }
    
    // Remove z from x's children list
    for (int j = i + 1; j < x->n; ++j) {
        x->children[j] = x->children[j + 1];
    }
    
    // Update the number of keys in x
    x->n--;
    
    // Delete the merged node z
    delete z;
    
    // Update parent pointers of y's children
    for (int j = 0; j <= y->n; ++j) {
        if (y->children[j] != nullptr) {
            y->children[j]->parent = y;
        }
    }
}
template<typename Key, typename Value>
void BplusTree<Key, Value>::redistributeKey(Node<Key, Value>* x, int i) {
    Node<Key, Value>* y = x->children[i];
    Node<Key, Value>* z = x->children[i + 1];
    
    if (y->n < t) {
        // Move a key from z to y
        y->keys[y->n] = x->keys[i];
        y->n++;
        
        // Move a key from z to x
        x->keys[i] = z->keys[0];
        
        // Move a child from z to y, if applicable
        if (!y->leaf) {
            y->children[y->n] = z->children[0];
        }
        
        // Update z
        z->keys.erase(z->keys.begin());
        if (!z->leaf) {
            z->children.erase(z->children.begin());
        }
        z->n--;
    } else {
        // Move a key from y to x
        x->keys[i] = y->keys[t - 1];
        
        // Move a key from y to z
        for (int j = 0; j < t; ++j) {
            z->keys[j] = y->keys[j + t];
        }
        
        // Move a child from y to z, if applicable
        if (!z->leaf) {
            for (int j = 0; j <= t; ++j) {
                z->children[j] = y->children[j + t];
            }
        }
        
        // Update y
        y->keys.resize(t);
        if (!y->leaf) {
            y->children.resize(t + 1);
        }
        y->n = t;
        
        // Update z
        z->n = t;
    }
    
    // Update parent pointers of y's and z's children
    for (int j = 0; j <= y->n; ++j) {
        if (y->children[j] != nullptr) {
            y->children[j]->parent = y;
        }
    }
    for (int j = 0; j <= z->n; ++j) {
        if (z->children[j] != nullptr) {
            z->children[j]->parent = z;
        }
    }
}

template<typename Key, typename Value>
void BplusTree<Key, Value>::insert(const Key& k, const Value& v) {
    if (root->n == 2 * t - 1) {
        Node<Key, Value>* s = new Node<Key, Value>;
        root->leaf = false;
        s->children.push_back(root);
        splitChild(s, 0);
        insertNonFull(s, k, v);
        root = s;
    } else {
        insertNonFull(root, k, v);
    }
}

template<typename Key, typename Value>
void BplusTree<Key, Value>::remove(const Key& k) {
    // Find the node containing the key
    Node<Key, Value>* x = root;
    bool found = false;

    while (x != nullptr) {
        int i = 0;
        while (i < x->n && k > x->keys[i]) {
            i++;
        }
        
        // Check if the key is found in the current node
        if (i < x->n && k == x->keys[i]) {
            found = true;
            break;
        }

        // If the current node is not a leaf, move to the appropriate child
        if (!x->leaf) {
            x = x->children[i];
        } else {
            // Reached a leaf node without finding the key, exit early
            break;
        }
    }

    // If the key is not found, return
    if (!found) return;

    // Remove the key from the leaf node
    int i = 0;
    while (i < x->n && k > x->keys[i]) {
        i++;
    }
    for (int j = i; j < x->n - 1; j++) {
        x->keys[j] = x->keys[j + 1];
        if (!x->leaf) {
            x->children[j] = x->children[j + 1];
        }
    }
    x->n--;

    // Handle underflow condition
    if (x->n < t) {
        // Attempt to borrow from siblings or merge
        if (x->parent != nullptr) {
            int siblingIndex = -1;
            Node<Key, Value>* sibling = nullptr;
            if (i != 0) {
                siblingIndex = i - 1;
                sibling = x->parent->children[siblingIndex];
            } else if (i < x->n) {
                siblingIndex = i;
                sibling = x->parent->children[siblingIndex];
            }

            // Try to redistribute with a sibling
            if (sibling != nullptr && sibling->n >= t) {
                redistributeKey(x->parent, siblingIndex);
            } else {
                // Merge with a sibling
                if (siblingIndex != -1) {
                    mergeChildren(x->parent, siblingIndex);
                } else {
                    mergeChildren(x->parent, i);
                }
                
                // After merging, the node may become the new root
                if (x->parent->n == 0) {
                    root = x;
                    delete x->parent;
                }
            }
        }
    }
}


template<typename Key, typename Value>
SearchResult<Value> BplusTree<Key, Value>::search(const Key& k) {
    // Start from the root and traverse down to find the key
    Node<Key, Value>* x = root;
    int i = 0;
    while(!x->leaf){
        while (i < x->n && k > x->keys[i]) {
            i++;
        }
        x = x->children[i];
    }
    i = 0;
    while(i < x->n && k > x->keys[i]){
        i++;
    }
    if (i < x->n && k == x->keys[i]) {
        return SearchResult<Value>(true, x->values[i]);
    } else {
        return SearchResult<Value>(false, Value());
    }
}

namespace py = pybind11;

template<typename K, typename V>
PYBIND11_MODULE_TPL(bplustree, m, K, V) {
    py::class_<BplusTree<K, V>>(m, "BPlusTree")
        .def(py::init<int>())
        .def("insert", &BplusTree<K, V>::insert, py::arg("key"), py::arg("value"))
        .def("remove", &BplusTree<K, V>::remove, py::arg("key"))
        .def("search", [](BplusTree<K, V>& tree, K key) -> py::object {
            auto result = tree.search(key);
            if(result.iserror) {
                throw std::runtime_error(result.error_message);
            }
            return result.result;
        }, py::arg("key"));
}

// To use this template module, you would call it like this in your main C++ file:
// #include "bplustree.h"
// PYBIND11_PLUGIN(bplustree) {
//     return bplustree<py::object, py::object>();
// }