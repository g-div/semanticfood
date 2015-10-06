import config
from rdflib import Graph, Namespace, RDF, URIRef
from flask import Blueprint, render_template, request, redirect, url_for
from flask_rdf import flask_rdf
from utils import SPARQLStore, getSingle

ingredients = Blueprint('ingredients', __name__)

LOCAL = Namespace(config.INGREDIENT_NS)

store = SPARQLStore(config.SPARQL_ENDPOINT).getConnection()
graph = Graph(store, config.GRAPH_NAME)

graph.bind('fo', 'http://www.bbc.co.uk/ontologies/fo/')
graph.bind('schema', 'http://schema.org/')


@ingredients.route('/<id>.rdf')
@flask_rdf
def getRDFIngredient(id):
	return getSingle(graph, LOCAL, id)