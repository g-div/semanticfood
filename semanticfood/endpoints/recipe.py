import config
from rdflib import Graph, Namespace, RDF, URIRef
from flask import Blueprint, render_template, request, redirect, url_for
from flask_negotiate import produces
from utils import SPARQLStore, RecipeForms
from models.recipe import Recipe


recipe = Blueprint('recipe', __name__)

FOOD = Namespace(config.ONTO['BBC'])
LOCAL = Namespace(config.GRAPH_NAME)

store = SPARQLStore(config.SPARQL_ENDPOINT).getConnection()
graph = Graph(store, config.GRAPH_NAME)
graph.bind('fo', 'http://www.bbc.co.uk/ontologies/fo/')
graph.bind('schema', 'http://schema.org/Recipe')


@recipe.route('/')
@produces('text/html')
def get():
    """ GET / List all recipes"""
    recipes = []
    for subject in graph.subjects(RDF.type, FOOD.Recipe):
        recipes.append({'uri': subject, 'name': subject.split('/')[-1:][0]})
    return render_template('recipe/recipes.html', recipes=recipes)


@recipe.route('/<id>')
def negotiate(id):
    if 'text/html' in request.headers.get('Accept'):
        return redirect(url_for('recipe.getHTMLRecipe', id=id))
    elif 'application/json+ld' in request.headers.get('Accept'):
        return redirect(url_for('recipe.getJSONLDRecipe', id=id))
    elif 'application/rdf+xml' in request.headers.get('Accept'):
        return redirect(url_for('recipe.getRDFRecipe', id=id))


@recipe.route('/<id>.html')
@produces('text/html')
def getHTMLRecipe(id):
    result = {}

    entry = URIRef(LOCAL[id])
    for predicate, obj in graph.predicate_objects(entry):
        result[predicate] = obj
        # TODO: adapt object to templates
    return render_template('recipe/recipe.html', recipe=result)


@recipe.route('/<id>.jsonld')
@produces('application/json+ld')
def getJSONLDRecipe(id):
    return getSingle(id).serialize(format='json-ld')


@recipe.route('/<id>.rdf')
@produces('application/rdf+xml')
def getRDFRecipe(id):
    return getSingle(id).serialize()


def getSingle(id):
    tmpGraph = Graph()

    entry = URIRef(LOCAL[id])
    for predicate, obj in graph.predicate_objects(entry):
        tmpGraph.add((entry, predicate, obj))

    return tmpGraph

@recipe.route('/create', methods=['GET', 'POST'])
@produces('text/html')
def create():
    # TODO: add tooltips based on schema.org description
    form = RecipeForms(request.form)

    if request.method == 'POST' and form.validate():

        for triple in Recipe(form.data).serialize():
            graph.add(triple)

        graph.commit()

        return redirect(url_for('recipe.get'))
    elif request.method == 'POST' and not form.validate():
        print(form.errors)
    return render_template('recipe/create.html', form=form)
