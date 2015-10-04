import config
from rdflib import Namespace
from urllib.parse import quote

LOCAL = Namespace(config.INGREDIENT_NS)


class Ingredient(object):

    """docstring for Ingredient"""

    def __init__(self, name, nutrients):
        self.name = name

        self.uri = LOCAL[quote(self.name)]

        self.nutrients = nutrients
