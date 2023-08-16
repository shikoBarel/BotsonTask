import json
from elasticsearch import Elasticsearch
from datetime import datetime
from decouple import config

es = Elasticsearch(
    [config('ELASTICSEARCH_URL')],
    basic_auth=(config('ELASTICSEARCH_USER'), config('ELASTICSEARCH_PASS'))
)

index_name = config('ELASTICSEARCH_INDEX_NAME')

# Load the test data
with open('test_data.json', 'r') as f:
    json_data = f.read()
data = json.loads(json_data)    

# Insert into Elasticsearch
for record in data:
    es.index(index=index_name, document=record)
