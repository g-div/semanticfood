import config
from rdflib import Namespace, RDF, Literal, XSD, RDFS

FO = Namespace(config.ONTO['BBC'])

class Ingredient(object):
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
