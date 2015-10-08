import config
from uuid import uuid4
from rdflib import Namespace, RDF, Literal, XSD, RDFS

FO = Namespace(config.ONTO['BBC'])

class IngredientList():
    """
    This class is used for the object-serialization of the class ingredientList_
    .. _ingredientList: http://www.bbc.co.uk/ontologies/fo#terms_IngredientList
    """
    LOCAL = Namespace(config.NS['ingredientList'])
    SFO = Namespace(config.ONTO['LOCAL'])

    def __init__(self, ingredients):
        self.ingredients = ingredients

        self.uri = self.LOCAL[str(uuid4())]

    def serialize(self):
        res = [(self.uri, RDF.type, FO.IngredientList)]
        for ingredient in self.ingredients:
            res.append((self.uri, FO.ingredients, ingredient.getURI()))
            res.extend(ingredient.serialize())

        return res

    def getURI(self):
        return self.uri


class Ingredient():
    """
    This class is used for the object-serialization of the class Ingredient_
    .. _Ingredient: http://www.bbc.co.uk/ontologies/fo#terms_Ingredient
    """
    LOCAL = Namespace(config.NS['ingredients'])

    def __init__(self, name, quantity, nutrients):
        self.name = name
        self.quantity = quantity
        self.nutrients = nutrients
        self.uri = self.LOCAL["{}g_{}".format(self.quantity, self.name.strip().replace(' ', '_'))]
        self.foodURI = self.LOCAL[name.strip().replace(' ', '_')]


    def serialize(self):
        return [(self.uri, RDF.type, FO.Ingredient),
                (self.uri, FO.metric_quantity, Literal('{} g'.format(self.quantity))),
                (self.uri, FO.quantity, Literal(self.quantity, datatype=XSD.nonNegativeInteger)),
                (self.uri, FO.food, self.foodURI),
                (self.foodURI, RDF.type, FO.Food),
                (self.foodURI, RDFS.label, Literal(self.name))]

    def getURI(self):
        return self.uri

    def getNutrients(self):
        return self.nutrients
