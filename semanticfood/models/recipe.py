import config
from utils import Timer
from rdflib import Namespace, RDF, Literal, RDFS
from rdflib.collection import Collection
from urllib import parse
from requests import Session



FO = Namespace(config.ONTO['BBC'])
SCHEMA = Namespace(config.ONTO['SCHEMA'])
LOCAL = Namespace(config.GRAPH_NAME)
INGREDIENT = Namespace(config.INGREDIENT_NS)


class Recipe():

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

        self.uri = LOCAL[self.name.strip().replace(' ', '_')]

    def serialize(self):

        res = self._calculateNutrition()
        res.extend([(self.uri, RDF.type, FO.Recipe),
               (self.uri, RDF.type, SCHEMA.Recipe),
               (self.uri, RDFS.label, Literal(self.name)),
               (self.uri, SCHEMA.description, Literal(self.description, lang='en')),
               (self.uri, SCHEMA.prepTime, Literal(Timer(self.prepTime).isoformat(), datatype=SCHEMA.Duration)),
               (self.uri, SCHEMA.cookTime, Literal(Timer(self.cookTime).isoformat(), datatype=SCHEMA.Duration)),
               (self.uri, SCHEMA.recipeYield, Literal(self.servings))])


        # TODO: add steps to the graph
        return res

    def deserialize(self, resource):
        self.name = resource.value(RDFS.label)
        self.description = resource.value(SCHEMA.description)
        self.prepTime = resource.value(SCHEMA.prepTime)
        self.cookTime = resource.value(SCHEMA.cookTime)
        self.servings = resource.value(SCHEMA.recipeYield)
        self.fat = resource.value(SCHEMA.fatContent)
        self.cal = resource.value(SCHEMA.calories)

        # TODO: add instructions

        self.ingredients = []
        for ingredient in resource.objects(FO.ingredients):
            name = ingredient.value(FO.food).value(RDFS.label)
            quantity = ingredient.value(FO.metric_quantity)
            self.ingredients.append('{} {}'.format(quantity, name))

        return self

    def _calculateNutrition(self):
        res = []

        session = Session()
        nutritionalInformations = {}
        for ingredient in self.ingredients:

            response = session.get(config.USDA_API.format(config.USDA_API_KEY, ingredient['food'])).json()
            name = response.get('report').get('food').get('name')
            nutrients = response.get('report').get('food').get('nutrients')
            quantity = ingredient['quantity']

            ingredientURI = INGREDIENT["{}g_{}".format(quantity, name.strip().replace(' ', '_'))]
            foodURI = INGREDIENT[name.strip().replace(' ', '_')]
            res.extend([(self.uri, FO.ingredients, ingredientURI),
                        (ingredientURI, RDF.type, FO.Ingredient),
                        (ingredientURI, FO.metric_quantity, Literal('{} g'.format(quantity))),
                        (ingredientURI, FO.food, foodURI),
                        (foodURI, RDF.type, FO.Food),
                        (foodURI, RDFS.label, Literal(name))])


            for nutrient in nutrients:
                if nutrient.get('nutrient_id') is not 268:
                    if not nutritionalInformations.get(nutrient.get('name')):
                        nutritionalInformations[nutrient.get('name')] = {'count': 0, 'unit': nutrient.get('unit')}
                    nutritionalInformations[nutrient.get('name')]['count'] += float(nutrient.get('value')) * quantity

        # TODO: transFatContent and unsaturatedFatContent are unknow
        for nutritionalInformation in nutritionalInformations:
            if nutritionalInformation == 'Energy':
                res.append((self.uri, SCHEMA.calories, Literal('{} {}'.format(nutritionalInformations[nutritionalInformation]['count'], nutritionalInformations[nutritionalInformation]['unit']), datatype=SCHEMA.Energy)))
            elif nutritionalInformation == 'Carbohydrate, by difference':
                res.append((self.uri, SCHEMA.carbohydrateContent, Literal('{} {}'.format(nutritionalInformations[nutritionalInformation]['count'], nutritionalInformations[nutritionalInformation]['unit']), datatype=SCHEMA.Mass)))
            elif nutritionalInformation == 'Cholesterol':
                res.append((self.uri, SCHEMA.cholesterolContent, Literal('{} {}'.format(nutritionalInformations[nutritionalInformation]['count'], nutritionalInformations[nutritionalInformation]['unit']), datatype=SCHEMA.Mass)))
            elif nutritionalInformation == 'Total lipid (fat)':
                res.append((self.uri, SCHEMA.fatContent, Literal('{} {}'.format(nutritionalInformations[nutritionalInformation]['count'], nutritionalInformations[nutritionalInformation]['unit']), datatype=SCHEMA.Mass)))
            elif nutritionalInformation == 'Fiber, total dietary':
                res.append((self.uri, SCHEMA.fiberContent, Literal('{} {}'.format(nutritionalInformations[nutritionalInformation]['count'], nutritionalInformations[nutritionalInformation]['unit']), datatype=SCHEMA.Mass)))
            elif nutritionalInformation == 'Protein':
                res.append((self.uri, SCHEMA.proteinContent, Literal('{} {}'.format(nutritionalInformations[nutritionalInformation]['count'], nutritionalInformations[nutritionalInformation]['unit']), datatype=SCHEMA.Mass)))
            elif nutritionalInformation == 'Fatty acids, total saturated':
                res.append((self.uri, SCHEMA.saturatedFatContent, Literal('{} {}'.format(nutritionalInformations[nutritionalInformation]['count'], nutritionalInformations[nutritionalInformation]['unit']), datatype=SCHEMA.Mass)))
            elif nutritionalInformation == 'Sodium, Na':
                res.append((self.uri, SCHEMA.sodiumContent, Literal('{} {}'.format(nutritionalInformations[nutritionalInformation]['count'], nutritionalInformations[nutritionalInformation]['unit']), datatype=SCHEMA.Mass)))
            elif nutritionalInformation == 'Sugars, total':
                res.append((self.uri, SCHEMA.sugarContent, Literal('{} {}'.format(nutritionalInformations[nutritionalInformation]['count'], nutritionalInformations[nutritionalInformation]['unit']), datatype=SCHEMA.Mass)))

        return res
