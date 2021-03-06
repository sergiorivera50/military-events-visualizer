from elasticsearch import Elasticsearch
import elasticsearch
import requests
import os

ES_HOST = os.environ["ES_HOST"]
ES_USER = os.environ["ES_USER"]
ES_PASS = os.environ["ES_PASS"]

def fetch_api_key(name):
  headers = {
    "Content-Type": "application/json",
  }

  json_data = {
    "name": name,
  }

  print("\nDeleting old API key...")
  requests.delete(ES_HOST + "/_security/api_key", headers=headers, json=json_data, auth=(ES_USER, ES_PASS), verify=False)
  
  print("\nCreating new API key...")
  response = requests.post(ES_HOST + "/_security/api_key", headers=headers, json=json_data, auth=(ES_USER, ES_PASS), verify=False)
  
  data = response.json()
  return data["id"], data["api_key"]

def connect_elasticsearch(api_key_name):
  api_id, api_key = fetch_api_key(api_key_name)  # fetch api key

  client = Elasticsearch(ES_HOST, api_key=(api_id, api_key), verify_certs=False)

  if client.ping():
    print(f"\nElasticsearch connection established at {ES_HOST} using API key with id {api_id}")
  else:
    print(f"\nUnable to reach Elasticsearch cluster at {ES_HOST} using API key with id {api_id}")
  return client

def create_index(es, index, mapping=None):
  print(f"\nCreating index {index}...")
  try:
    es.indices.create(index=index, mappings=mapping)
    print("\nIndex created successfully!")
  except elasticsearch.exceptions.RequestError as ex:
    if ex.error == 'resource_already_exists_exception':
        print("\nIndex already exists, ignoring...")
        pass
    else: # other exception
        raise ex
