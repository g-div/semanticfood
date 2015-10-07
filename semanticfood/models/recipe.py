import config
from utils import Timer
from .ingredient import Ingredient
from .step import StepSequence
from rdflib import Namespace, RDF, Literal, XSD, RDFS
from requests import Session

FO = Namespace(config.ONTO['BBC'])
NUTRIENT = Namespace(config.ONTO['LIRMM'])
SFO = Namespace(config.ONTO['LOCAL'])


class Recipe():
    LOCAL = Namespace(config.NS['recipes'])

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
        self.steps = StepSequence(steps=self.steps)
        res.extend(self.steps.serialize())
        res.extend([(self.uri, RDF.type, FO.Recipe),
               (self.uri, RDF.type, NUTRIENT.Food),
               (self.uri, RDF.type, SFO.Recipe),
               (self.uri, SFO.steps, self.steps.getURI()),
               (self.uri, RDFS.label, Literal(self.name)),
               (self.uri, RDFS.comment, Literal(self.description, lang='en')),
               (self.uri, SFO.prepTime, Literal(self.prepTime, datatype=XSD.integer)),
               (self.uri, SFO.cookTime, Literal(self.cookTime, datatype=XSD.integer)),
               (self.uri, FO.serves, Literal(self.servings))])


        # TODO: add steps to the graph
        return res

    def deserialize(self, resource):
        self.name = resource.value(RDFS.label)
        self.description = resource.value(RDFS.comment)
        self.prepTime = resource.value(SFO.prepTime)
        self.cookTime = resource.value(SFO.cookTime)
        self.servings = resource.value(FO.serves)
        self.fat = resource.value(NUTRIENT.fatPer100g)
        self.saturatedFat = resource.value(NUTRIENT.saturatedFatPer100g)
        self.unsaturatedFat = resource.value(NUTRIENT.monounsaturatedFatPer100g) + resource.value(NUTRIENT.polyunsaturatedFatPer100g)
        self.monounsaturatedFat = resource.value(NUTRIENT.monounsaturatedFatPer100g)
        self.polyunsaturatedFat = resource.value(NUTRIENT.polyunsaturatedFatPer100g)
        self.transFat = resource.value(NUTRIENT.transFatPer100g)
        self.calories = resource.value(NUTRIENT.energyPer100g)
        self.proteins = resource.value(NUTRIENT.proteinsPer100g)
        self.carbohydrates = resource.value(NUTRIENT.carbohydratesPer100g)
        self.cholesterol = resource.value(NUTRIENT.cholesterolPer100g)
        self.sodium = resource.value(NUTRIENT.sodiumPer100g)
        self.fibers = resource.value(NUTRIENT.fiberPer100g)
        self.sugars = resource.value(NUTRIENT.sugarsPer100g)

        # TODO: add instructions

        self.ingredients = []
        for ingredient in resource.objects(SFO.ingredients):
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
        for label in table:
            if label == 'Energy':
                res.append((self.uri, NUTRIENT.energyPer100g, Literal(table[label]['count'], datatype=XSD.decimal)))
            elif label == 'Carbohydrate, by difference':
                res.append((self.uri, NUTRIENT.carbohydratesPer100g, Literal(table[label]['count'], datatype=XSD.decimal)))
            elif label == 'Cholesterol':
                res.append((self.uri, NUTRIENT.cholesterolPer100g, Literal(float(table[label]['count']) / 100, datatype=XSD.decimal)))
            elif label == 'Total lipid (fat)':
                res.append((self.uri, NUTRIENT.fatPer100g, Literal(table[label]['count'], datatype=XSD.decimal)))
            elif label == 'Fiber, total dietary':
                res.append((self.uri, NUTRIENT.fiberPer100g, Literal(table[label]['count'], datatype=XSD.decimal)))
            elif label == 'Protein':
                res.append((self.uri, NUTRIENT.proteinsPer100g, Literal(table[label]['count'], datatype=XSD.decimal)))
            elif label == 'Fatty acids, total saturated':
                res.append((self.uri, NUTRIENT.saturatedFatPer100g, Literal(table[label]['count'])))
            elif label == 'Fatty acids, total trans':
                res.append((self.uri, NUTRIENT.transFatPer100g, Literal(table[label]['count'])))
            elif label == 'Fatty acids, total monounsaturated':
                res.append((self.uri, NUTRIENT.monounsaturatedFatPer100g, Literal(table[label]['count'])))
            elif label == 'Fatty acids, total polyunsaturated':
                res.append((self.uri, NUTRIENT.polyunsaturatedFatPer100g, Literal(table[label]['count'])))
            elif label == 'Sodium, Na':
                res.append((self.uri, NUTRIENT.sodiumPer100g, Literal(float(table[label]['count']) / 100, datatype=XSD.decimal)))
            elif label == 'Sugars, total':
                res.append((self.uri, NUTRIENT.sugarsPer100g, Literal(table[label]['count'], datatype=XSD.decimal)))
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

            res.append((self.uri, SFO.ingredients, ing.getURI()))
            res.extend(ing.serialize())

            nutritionalInformations = self._calculateNutrients(ingredient=ing, data=nutritionalInformations)

        res.extend(self._parseNutritionTable(nutritionalInformations, res))
        return res
