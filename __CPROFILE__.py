import pstats
from io import StringIO
import cProfile

import cx.SzQlib as lib

for package in dir(lib):
    if package.startswith('__'):
        continue
    for func in dir(getattr(lib, package)):
        if func.startswith("__"):
            continue
        print(f"{package}.{func}")


