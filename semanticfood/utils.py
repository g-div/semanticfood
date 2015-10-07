import config
from wtforms import Form, FieldList, TextField, TextAreaField, IntegerField, FormField, SubmitField, validators
from rdflib import Graph, URIRef
from rdflib.plugins.stores.sparqlstore import SPARQLUpdateStore


def getSingle(graph, ns, id):
    tmpGraph = Graph()

    entry = URIRef(ns[id])
    for predicate, obj in graph.predicate_objects(entry):
        tmpGraph.add((entry, predicate, obj))

    return tmpGraph


class GraphWrapper():

    def __init__(self):
        store = SPARQLUpdateStore(config.SPARQL_ENDPOINT, config.SPARQL_ENDPOINT)
        self.graph = Graph(store, config.GRAPH_NAME)
        self.graph.bind('fo', 'http://www.bbc.co.uk/ontologies/fo/')
        self.graph.bind('schema', 'http://schema.org/')
        self.graph.bind('food', 'http://data.lirmm.fr/ontologies/food/#')

    def getConnection(self):
        return self.graph


class Timer():

    """docstring for Timer"""

    def __init__(self, data):
        self.days = data['days']
        self.hours = data['hours']
        self.minutes = data['minutes']

    def isoformat(self):
        prepTime = 'P'
        if self.days:
            prepTime += '{}D'.format(self.days)
        if self.hours or self.minutes:
            prepTime += 'T'
        if self.hours:
            prepTime += '{}H'.format(self.hours)
        if self.minutes:
            prepTime += '{}M'.format(self.minutes)

        return prepTime


class TimeForm(Form):
    days = IntegerField(description='Days',
                        validators=[validators.NumberRange(min=0),
                                    validators.Optional()])
    hours = IntegerField(description='Hours',
                         validators=[validators.NumberRange(min=0),
                                     validators.Optional()])
    minutes = IntegerField(description='Minutes',
                           validators=[validators.NumberRange(min=0),
                                       validators.Optional()])


class IngredientForm(Form):
    food = TextAreaField()
    quantity = IntegerField(validators=[validators.NumberRange(min=1)])


class RecipeForms(Form):
    name = TextField(description='Recipe Name',
                     validators=[validators.Length(min=2, max=35)])

    description = TextAreaField(description='Description')

    prepTime = FormField(TimeForm,
                         label='Preparation Time (in Minutes)',
                         description='Preparation Time (in Minutes)')

    cookTime = FormField(TimeForm,
                         label='Cooking Time Time (in Minutes)',
                         description='Cooking Time Time (in Minutes)')

    servings = IntegerField(description='Servings',
                            validators=[validators.NumberRange(min=1)])

    ingredient = FieldList(FormField(IngredientForm), description='Ingredients')

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

