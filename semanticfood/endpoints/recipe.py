import config
from rdflib import Graph, Namespace, RDF, URIRef
from flask import Blueprint, render_template, request, redirect, url_for
from flask_negotiate import produces
from utils import SPARQLStore, RecipeForms
from classes.recipe import Recipe


recipe = Blueprint('recipe', __name__)

FOOD = Namespace(config.ONTO['BBC'])

store = SPARQLStore(config.SPARQL_ENDPOINT).getConnection()
graph = Graph(store, config.GRAPH_NAME)
# graph.bind('FOOD', 'www.bbc.co.uk/ontologies/fo/')


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


@recipe.route('/<id>.html')
@produces('text/html')
def getHTMLRecipe(id):
    result = {}

    entry = URIRef(request.url.replace('.html', ''))
    for predicate, obj in graph.predicate_objects(entry):
        result[predicate] = obj
        # TODO: adapt object to templates
    return render_template('recipe/recipe.html', recipe=result)


@recipe.route('/<id>.jsonld')
@produces('application/json+ld')
def getJSONLDRecipe(id):
    tmpGraph = Graph()

    entry = URIRef(request.url.replace('.jsonld', ''))
    for predicate, obj in graph.predicate_objects(entry):
        tmpGraph.add((entry, predicate, obj))

    return graph.serialize(format='json-ld')


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
