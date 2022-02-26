from helper import connect_elasticsearch
import http.client, urllib.parse

API_KEY = "a2ab751f096ce0b17661c201bcfc4919"

conn = http.client.HTTPConnection('api.positionstack.com')

params = urllib.parse.urlencode({
  'access_key': API_KEY,
  'query': 'Antonov Airport',
  'limit': 1,
  })

conn.request('GET', '/v1/forward?{}'.format(params))

res = conn.getresponse()
data = res.read()
print(data.decode('utf-8'))

#es = connect_elasticsearch("python-inject-script")

