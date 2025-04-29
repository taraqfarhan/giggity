# Miscellaneous helper functions (used in the implementations of porcelain and plumbing commands)

# python standard modules
import zlib
import os


def read_file(path, compressed=False):
    if (os.path.exists(path) and os.path.isfile(path)):
        if not compressed: 
            with open(path, "rb") as file: return file.read()
        else:
            with open(path, "rb") as file: return zlib.decompress(file.read()) # returns utf-8 encoded data
    else: print(f"fatal: could not open '{path}' for reading: No such file")