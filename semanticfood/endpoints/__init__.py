import config
from rdflib import Namespace
from flask import Blueprint, request
from flask_rdf import flask_rdf
from flask_negotiate import produces
from utils import getSingle, GraphWrapper


class GenericBlueprint():

    def __init__(self, name):
        self.route = Blueprint(name, __name__)

        LOCAL = Namespace(config.NS[name])

        graph = GraphWrapper().getConnection()

        @self.route.route('/<id>')
        @flask_rdf
        @produces(
           'application/rdf+xml',
           'application/xml',
           'text/html',
           'application/json+ld',
           'application/n-triples',
           'text/n-triples',
           'text/rdf+nt',
           'application/n3',
           'text/n3',
           'text/rdf+n3',
        )
        def getRDFIngredient(id):
            if 'application/json+ld' in request.headers.get('Accept'):
                return getSingle(graph, LOCAL, id).serialize(format='json-ld')
            return getSingle(graph, LOCAL, id)

    def getBlueprint(self):
        return self.route
