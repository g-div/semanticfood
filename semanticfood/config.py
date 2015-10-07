DEBUG = True

HOST = 'localhost'
PORT = 8000
SERVER_NAME = '{}:{}'.format(HOST, PORT)

GRAPH_NAME = 'http://semanticfood.org/'

NS = {
    'ingredients': '{}ingredients/'.format(GRAPH_NAME)
}

RECIPE_PREFIX = '{}recipes/'.format(GRAPH_NAME)
INGREDIENT_PREFIX = '{}ingredients/'.format(GRAPH_NAME)
SPARQL_ENDPOINT = 'http://46.101.152.77:8890/sparql'

ONTO = {
    'BBC': 'http://www.bbc.co.uk/ontologies/fo/',
    'SCHEMA': 'http://schema.org/',
    'LIRMM': 'http://data.lirmm.fr/ontologies/food/#'
}

USDA_API = 'http://api.nal.usda.gov/ndb/reports/?ndbno={1}&api_key={0}'
USDA_API_KEY = 'V5zvO2rQuQAq36ajpuFhTaPLm74RsN9CrcCP3YG1'
