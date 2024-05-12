#include <pybind11/pybind11.h>

PYBIND11_MODULE(database, m) {
    m.doc() = "pybind11 example plugin";
    
}
