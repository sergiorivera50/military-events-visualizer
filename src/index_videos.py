import urllib.request
import json
import urllib
import pprint
import urllib.parse as urlparse
import http.client, urllib.parse
from helper import connect_elasticsearch, create_index

GEO_API_KEY = "a2ab751f096ce0b17661c201bcfc4919"
YT_API_KEY = "AIzaSyDWjXLqKU9YIzcD58a5tLau98lkId2U7TM"

def geo_locate(address):
  conn = http.client.HTTPConnection('api.positionstack.com')

  params = urllib.parse.urlencode({
    'access_key': GEO_API_KEY,
    'query': address,
    'limit': 1,
    })

  conn.request('GET', '/v1/forward?{}'.format(params))

  res = conn.getresponse()
  data = res.read()
  data = json.loads(data.decode())
  
  return data["data"][0]["latitude"], data["data"][0]["longitude"]

def get_video_id(url):
  url_data = urllib.parse.urlparse(url)
  query = urllib.parse.parse_qs(url_data.query)
  return query["v"][0]

def get_video_data(url):
  params = {'id': get_video_id(url), 'key': YT_API_KEY, 'part': 'snippet,contentDetails,statistics'}
  
  google_api_endpoint = 'https://www.googleapis.com/youtube/v3/videos'
  query_string = urllib.parse.urlencode(params)
  google_api_url = google_api_endpoint + "?" + query_string

  with urllib.request.urlopen(google_api_url) as response:
    response_text = response.read()
    data = json.loads(response_text.decode())
    return data

def index_json(file):
  es = connect_elasticsearch("python-inject-script")

  mapping = {
    "properties": {
      "geolocation": {
        "type": "geo_point"
      }
    }
  }

  create_index(es, "youtube-videos", mapping=mapping)

  with open(file, 'r') as f:
    videos = json.load(f)

    doc_id = 1
    for video in videos:
      url = video["url"]
      location = video["location"]

      yt_data = get_video_data(url)
      title = yt_data["items"][0]["snippet"]["title"]
      timestamp = yt_data["items"][0]["snippet"]["publishedAt"]
      lat, lon = geo_locate(location)

      doc = {
        "title": title,
        "url": url,
        "geolocation": {
          "lat": lat,
          "lon": lon
        },
        "location": location,
        "timestamp": timestamp,
      }

      es.index(index="youtube-videos", id=doc_id, document=doc)

      pprint.pprint(doc)

      doc_id += 1

index_json("./videos.json")
