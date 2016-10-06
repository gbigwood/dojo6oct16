import sys
import os.path
from importlib.util import find_spec, cache_from_source


class InfectImporter():

    def __init__(self):
        self.inside = False

    def find_spec(self, name, path=None, target=None):
        if not self.inside:
            self.inside = True
            spec = find_spec(name, path)
            self.infect(spec.origin)
            self.inside = False
        return None

    def infect(self, filename):
        if filename:
            pyc_filename = cache_from_source(filename)
            if os.path.exists(pyc_filename):
                print("infecting", filename)


sys.meta_path = [InfectImporter()] + sys.meta_path

import requests