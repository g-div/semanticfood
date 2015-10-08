import config
from wtforms import Form, FieldList, TextField, TextAreaField, IntegerField, FormField, SubmitField, validators
from rdflib import Graph, URIRef
from rdflib.plugins.stores.sparqlstore import SPARQLUpdateStore


def getSingle(graph, ns, id):
    """
    This function is used by the most endpoints (e.g.: GenericBlueprint)
    to get all predicates and objects related to the given id.

    :param graph: the graph with data
    :ns ns: the namespace of the resource
    :id id: the id of the resource
    """
    tmpGraph = Graph()

    entry = URIRef(ns[id])
    for predicate, obj in graph.predicate_objects(entry):
        tmpGraph.add((entry, predicate, obj))

    return tmpGraph


class GraphWrapper():
    """
    A small utility class to wrap the connection of the
    RDFlib Graph
    """

    def __init__(self):
        store = SPARQLUpdateStore(
            config.SPARQL_ENDPOINT, config.SPARQL_ENDPOINT)
        self.graph = Graph(store, config.GRAPH_NAME)
        self.graph.bind('fo', config.ONTO['BBC'])
        self.graph.bind('food', config.ONTO['LIRMM'])
        self.graph.bind('sfo', config.ONTO['LOCAL'])

    def getConnection(self):
        return self.graph


class Timer():
    """
    A small utility class to convert minutes in ISO 8601
    and to an human readable string
    """

    def __init__(self, minutes):
        self.minutes, self.hours = divmod(int(minutes), 60)

    def getString(self):
        if self.hours:
            return '{0} hours and {1} minutes'.format(self.minutes, self.hours)
        else:
            return '{1} minutes'.format(self.minutes)

    def isoformat(self):
        time = 'P'
        if self.hours or self.minutes:
            time += 'T'
        if self.hours:
            time += '{}H'.format(self.hours)
        if self.minutes:
            time += '{}M'.format(self.minutes)

        return time


class IngredientForm(Form):
    food = TextAreaField()
    quantity = IntegerField(validators=[validators.NumberRange(min=1)])


class RecipeForms(Form):
    name = TextField(description='Recipe Name',
                     validators=[validators.Length(min=2, max=35)])

    description = TextAreaField(description='Description')

    prepTime = IntegerField(label='Preparation Time',
                            description='Preparation Time (Minutes)', validators=[validators.NumberRange(min=0), validators.Optional()])

    cookTime = IntegerField(label='Cooking Time',
                            description='Cooking Time (Minutes)', validators=[validators.NumberRange(min=0), validators.Optional()])

    servings = IntegerField(description='Servings',
                            validators=[validators.NumberRange(min=1)])

    ingredient = FieldList(
        FormField(IngredientForm), description='Ingredients')

    instructionStep = FieldList(TextAreaField(description='Describe the first step'),
                                min_entries=1)

    submit = SubmitField(description='Save')


class Filter(Form):
    operator = TextField()
    value = TextField()
    type = IntegerField()
    unit = TextField()


class SearchForm(Form):
    fulltextsearch = TextField()
    filter = FieldList(FormField(Filter))
