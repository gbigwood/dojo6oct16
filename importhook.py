import sys
from importlib.util import find_spec

class InfectImporter():

    def __init__(self):
        self.inside = False

    def find_spec(self, name, path=None, target=None):
        if not self.inside:
            self.inside = True
            spec = find_spec(name, path)
            print("infect ", spec.origin)
            self.inside = False
        return None

sys.meta_path = [InfectImporter()] + sys.meta_path

import http.client
