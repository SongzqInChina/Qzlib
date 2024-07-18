from setuptools import setup
from Cython.Build import cythonize
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [
   Extension("bplustree",
             ["bplustree.pyx"],
             language="c++",      # Specify that we're using C++
             extra_compile_args=["-std=c++11"], # Specify the C++ standard
             include_dirs=['.']   # Include directory for headers
   )
]

setup(
   name='BPlusTree',
   cmdclass={'build_ext': build_ext},
   ext_modules=cythonize(ext_modules),
)
