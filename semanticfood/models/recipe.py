import config
from utils import Timer, USDA
from rdflib import Namespace, RDF, Literal, XSD
from urllib.parse import quote
from models.ingredient import Ingredient


FOOD = Namespace(config.ONTO['BBC'])
SCHEMA = Namespace(config.ONTO['SCHEMA'])
LOCAL = Namespace(config.GRAPH_NAME)


class Recipe():

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
            self.ingredients.append(Ingredient(name=response.get('report').get('food').get('name'), 
                                               nutrients=response.get('report').get('food').get('nutrients')))

        self.uri = LOCAL[quote(self.name)]

    def serialize(self):

        res = [(self.uri, RDF.type, FOOD.Recipe),
                (self.uri, RDF.type, SCHEMA.Recipe),
                (self.uri, SCHEMA.description, Literal(self.description, lang='en')),
                (self.uri, SCHEMA.prepTime, Literal(self.prepTime, datatype=SCHEMA.Duration)),
                (self.uri, SCHEMA.cookTime, Literal(self.cookTime, datatype=SCHEMA.Duration)),
                (self.uri, FOOD.serves, Literal(self.servings, datatype=XSD.String))]

        nutrients = {}
        for ingredient in self.ingredients:
            for nutrient in ingredient.nutrients:
              if not nutrients.get(nutrient.get('name')):
                nutrients[nutrient.get('name')] = 0
              nutrients[nutrient.get('name')] += float(nutrient.get('value'))

            res.append((self.uri, FOOD.ingredient, ingredient.uri))
        print(nutrients)
        # TODO: add other fields to the graph
        return res
