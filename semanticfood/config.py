DEBUG = True

HOST = 'localhost'
PORT = 8000
SERVER_NAME = '{}:{}'.format(HOST, PORT)

GRAPH_NAME = 'http://semanticfood.org/'

NS = {
    'ingredients': '{}ingredients/'.format(GRAPH_NAME),
    'recipes': '{}recipes/'.format(GRAPH_NAME),
    'steps': '{}steps/'.format(GRAPH_NAME),
}

SPARQL_ENDPOINT = 'http://46.101.152.77:8890/sparql'

ONTO = {
    'BBC': 'http://www.bbc.co.uk/ontologies/fo/',
    'LIRMM': 'http://data.lirmm.fr/ontologies/food/#',
    'LOCAL': '{}ontology/#'.format(GRAPH_NAME)
}

USDA_API = 'http://api.nal.usda.gov/ndb/reports/?ndbno={1}&api_key={0}'
USDA_API_KEY = 'V5zvO2rQuQAq36ajpuFhTaPLm74RsN9CrcCP3YG1'
