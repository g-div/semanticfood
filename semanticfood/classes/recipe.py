import config
from utils import Timer, USDA
from uritools import uricompose
from rdflib import Namespace, RDF, URIRef, Literal
from classes.ingredient import Ingredient


FOOD = Namespace(config.ONTO['BBC'])
SCHEMA = Namespace(config.ONTO['SCHEMA'])


class Recipe(object):

    """docstring for Recipe"""

    def __init__(self, data={'name': '',
                             'description': '',
                             'prepTime': {},
                             'cookTime': {},
                             'servings': 0,
                             'ingredient': []}):

        self.name = data.get('name')
        self.description = data.get('description')
        self.prepTime = Timer(data.get('prepTime')).isoformat()
        self.cookTime = Timer(data.get('cookTime')).isoformat()
        self.servings = data.get('servings')
        self.ingredients = []
        for response in USDA(data.get('ingredient')).getData():
            self.ingredients.append(Ingredient(name=response.get('report').get('food').get('name')))

    def serialize(self):
        entry = URIRef(uricompose(scheme='http',
                                  host=config.HOST,
                                  port=config.PORT,
                                  path='/{}/{}'.format('recipes', self.name)))

        # TODO: add other fields to the graph
        return [(entry, RDF.type, FOOD.Recipe),
                (entry, SCHEMA.description, Literal(self.description))]
                #(entry, SCHEMA.prepTime, self.prepTime),
                #(entry, SCHEMA.cookTime, self.cookTime),
                #(entry, FOOD.serves, self.servings)]
