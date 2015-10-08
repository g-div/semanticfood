"""
semanticfood.endpoints
~~~~~~~~~~~~~~~
This module contains the accessible HTTP endpoints for our project
"""

import config
from .recipe import recipe
from rdflib import Namespace
from flask import Blueprint, request
from flask_rdf import flask_rdf
from flask_negotiate import produces
from utils import getSingle, GraphWrapper

Recipe = recipe


class GenericBlueprint():
    """
    This is the implementation of a generic HTTP endpoint, which 
    can be used to expose RDF resources in different serializations
    formats.
    """

    def __init__(self, name):
        """
        Create the Flask Blueprint object and connect to the RDF graph

        :param name: the name of the resource-type (e.g.: ingredients)
        """
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
