import config
from utils import Timer
from .ingredient import Ingredient
from rdflib import Namespace, RDF, Literal, XSD, RDFS
from requests import Session

FO = Namespace(config.ONTO['BBC'])
SCHEMA = Namespace(config.ONTO['SCHEMA'])
NUTRIENT = Namespace(config.ONTO['LIRMM'])


class Recipe():
    LOCAL = Namespace(config.RECIPE_PREFIX)

    """docstring for Recipe"""

    def __init__(self, data={'name': '',
                             'description': '',
                             'prepTime': {},
                             'cookTime': {},
                             'servings': 0,
                             'ingredient': []}):

        self.name = data.get('name').strip()
        self.description = data.get('description')
        self.prepTime = data.get('prepTime')
        self.cookTime = data.get('cookTime')
        self.servings = data.get('servings')
        self.ingredients = data.get('ingredient')
        self.steps = data.get('instructionStep')

        self.uri = self.LOCAL[self.name.strip().replace(' ', '_')]

    def serialize(self):

        res = self._serializeIngredients()
        res.extend([(self.uri, RDF.type, FO.Recipe),
               (self.uri, RDF.type, NUTRIENT.FOOD),
               (self.uri, RDFS.label, Literal(self.name)),
               (self.uri, RDFS.comment, Literal(self.description, lang='en')),
               (self.uri, SCHEMA.prepTime, Literal(Timer(self.prepTime).isoformat(), datatype=SCHEMA.Duration)),
               (self.uri, SCHEMA.cookTime, Literal(Timer(self.cookTime).isoformat(), datatype=SCHEMA.Duration)),
               (self.uri, FO.serves, Literal(self.servings))])


        # TODO: add steps to the graph
        return res

    def deserialize(self, resource):
        self.name = resource.value(RDFS.label)
        self.description = resource.value(RDFS.comment)
        self.prepTime = resource.value(SCHEMA.prepTime)
        self.cookTime = resource.value(SCHEMA.cookTime)
        self.servings = resource.value(FO.serves)
        self.fat = resource.value(NUTRIENT.fatPer100g)
        self.cal = resource.value(NUTRIENT.energyPer100g)

        # TODO: add instructions

        self.ingredients = []
        for ingredient in resource.objects(FO.ingredients):
            name = ingredient.value(FO.food).value(RDFS.label)
            quantity = ingredient.value(FO.metric_quantity)
            self.ingredients.append('{} {}'.format(quantity, name))

        return self


    def _calculateNutrients(self, ingredient, data):
        for nutrient in ingredient.getNutrients():
            if nutrient.get('nutrient_id') is not 268:
                if not data.get(nutrient.get('name')):
                    data[nutrient.get('name')] = {'count': 0, 'unit': nutrient.get('unit')}
                data[nutrient.get('name')]['count'] += float(nutrient.get('value'))
        return data

    def _parseNutritionTable(self, table, res):
        # TODO: transFatContent and unsaturatedFatContent are unknown
        for label in table:
            if label == 'Energy':
                res.append((self.uri, NUTRIENT.energyPer100g, Literal(table[label]['count'])))
            elif label == 'Carbohydrate, by difference':
                res.append((self.uri, NUTRIENT.carbohydratesPer100g, Literal(table[label]['count'], datatype=XSD.decimal)))
            elif label == 'Cholesterol':
                res.append((self.uri, NUTRIENT.cholesterolPer100g, Literal(table[label]['count'], datatype=XSD.decimal)))
            elif label == 'Total lipid (fat)':
                res.append((self.uri, NUTRIENT.fatPer100g, Literal(table[label]['count'], datatype=XSD.decimal)))
            elif label == 'Fiber, total dietary':
                res.append((self.uri, NUTRIENT.fiberPer100g, Literal(table[label]['count'])))
            elif label == 'Protein':
                res.append((self.uri, NUTRIENT.proteinsPer100g, Literal(table[label]['count'], datatype=XSD.decimal)))
            elif label == 'Fatty acids, total saturated':
                res.append((self.uri, NUTRIENT.saturatedFatPer100g, Literal(table[label]['count'])))
            elif label == 'Sodium, Na':
                res.append((self.uri, NUTRIENT.sodiumPer100g, Literal(table[label]['count'])))
            elif label == 'Sugars, total':
                res.append((self.uri, NUTRIENT.sugarsPer100g, Literal(table[label]['count'])))
        return res

    def _serializeIngredients(self):
        res = []

        session = Session()
        nutritionalInformations = {}
        for ingredient in self.ingredients:

            response = session.get(config.USDA_API.format(config.USDA_API_KEY, ingredient['food'])).json()

            ing = Ingredient(name=response.get('report').get('food').get('name'),
                             quantity=ingredient['quantity'],
                             nutrients=response.get('report').get('food').get('nutrients'))

            res.append((self.uri, FO.ingredients, ing.getURI()))
            res.extend(ing.serialize())

            nutritionalInformations = self._calculateNutrients(ingredient=ing, data=nutritionalInformations)

        res.extend(self._parseNutritionTable(nutritionalInformations, res))
        return res
