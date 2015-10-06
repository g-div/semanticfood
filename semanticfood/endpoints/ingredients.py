import config
from rdflib import Graph, Namespace, RDF, URIRef
from flask import Blueprint, render_template, request, redirect, url_for
from flask_rdf import flask_rdf
from flask_negotiate import produces
from utils import SPARQLStore, getSingle

ingredients = Blueprint('ingredients', __name__)

LOCAL = Namespace(config.INGREDIENT_NS)

store = SPARQLStore(config.SPARQL_ENDPOINT).getConnection()
graph = Graph(store, config.GRAPH_NAME)

graph.bind('fo', 'http://www.bbc.co.uk/ontologies/fo/')
graph.bind('schema', 'http://schema.org/')


@ingredients.route('/<id>')
@flask_rdf
@produces(
   'application/rdf+xml',
   'application/xml',
   'text/html',
   'application/n-triples',
   'text/n-triples',
   'text/rdf+nt',
   'application/n3',
   'text/n3',
   'text/rdf+n3',
)
def getRDFIngredient(id):
	return getSingle(graph, LOCAL, id)