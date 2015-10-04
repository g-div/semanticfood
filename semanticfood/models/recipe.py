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
            res.append((self.uri, FOOD.ingredient, ingredient.uri))

            for nutrient in ingredient.nutrients:
                if nutrient.get('nutrient_id') is not 268:
                    if not nutrients.get(nutrient.get('name')):
                        nutrients[nutrient.get('name')] = {'count': 0, 'unit': nutrient.get('unit')}
                    nutrients[nutrient.get('name')]['count'] += float(nutrient.get('value'))

        # TODO: transFatContent and unsaturatedFatContent are unknow
        for nutritionalInformation in nutrients:
            if nutritionalInformation == 'Energy':
                res.append((self.uri, SCHEMA.calories, Literal('{} {}'.format(nutrients[nutritionalInformation]['count'], nutrients[nutritionalInformation]['unit']), datatype=SCHEMA.Energy)))
            if nutritionalInformation == 'Carbohydrate, by difference':
                res.append((self.uri, SCHEMA.carbohydrateContent, Literal('{} {}'.format(nutrients[nutritionalInformation]['count'], nutrients[nutritionalInformation]['unit']), datatype=SCHEMA.Mass)))
            if nutritionalInformation == 'Cholesterol':
                res.append((self.uri, SCHEMA.cholesterolContent, Literal('{} {}'.format(nutrients[nutritionalInformation]['count'], nutrients[nutritionalInformation]['unit']), datatype=SCHEMA.Mass)))
            if nutritionalInformation == 'Total lipid (fat)':
                res.append((self.uri, SCHEMA.fatContent, Literal('{} {}'.format(nutrients[nutritionalInformation]['count'], nutrients[nutritionalInformation]['unit']), datatype=SCHEMA.Mass)))
            if nutritionalInformation == 'Fiber, total dietary':
                res.append((self.uri, SCHEMA.fiberContent, Literal('{} {}'.format(nutrients[nutritionalInformation]['count'], nutrients[nutritionalInformation]['unit']), datatype=SCHEMA.Mass)))
            if nutritionalInformation == 'Protein':
                res.append((self.uri, SCHEMA.proteinContent, Literal('{} {}'.format(nutrients[nutritionalInformation]['count'], nutrients[nutritionalInformation]['unit']), datatype=SCHEMA.Mass)))
            if nutritionalInformation == 'Fatty acids, total saturated':
                res.append((self.uri, SCHEMA.saturatedFatContent, Literal('{} {}'.format(nutrients[nutritionalInformation]['count'], nutrients[nutritionalInformation]['unit']), datatype=SCHEMA.Mass)))
            if nutritionalInformation == 'Sodium, Na':
                res.append((self.uri, SCHEMA.sodiumContent, Literal('{} {}'.format(nutrients[nutritionalInformation]['count'], nutrients[nutritionalInformation]['unit']), datatype=SCHEMA.Mass)))
            if nutritionalInformation == 'Sugars, total':
                res.append((self.uri, SCHEMA.sugarContent, Literal('{} {}'.format(nutrients[nutritionalInformation]['count'], nutrients[nutritionalInformation]['unit']), datatype=SCHEMA.Mass)))

        # TODO: add steps to the graph
        return res
