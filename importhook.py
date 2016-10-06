import imp
import sys


class InfectImporter():

    def find_spec(self, name, path=None, target=None):
        print("find spec", name, path, target)
        return None

sys.meta_path = [InfectImporter()] + sys.meta_path

import http.client
