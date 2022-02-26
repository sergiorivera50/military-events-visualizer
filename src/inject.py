from helper import fetch_api_key, connect_elasticsearch
from datetime import datetime

es = connect_elasticsearch("python-inject-script")

mapping = {
  "properties": {
    "location": {
      "type": "geo_point"
    }
  }
}

es.indices.create(index="military-events", mappings=mapping)

kiev = {
    "text": "Capital of Ukraine",
    "location": {
      "lat": 50.450001,
      "lon": 30.523333
    },
    "timestamp": datetime.now(),
}

response = es.index(index="military-events", id=1, document=kiev)
print(response['result'])
