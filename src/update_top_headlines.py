from newsapi import NewsApiClient
from helper import connect_elasticsearch

es = connect_elasticsearch("python-inject-script")

newsapi = NewsApiClient(api_key="970bd1b9a4fc4dda8977fada1f2b32e6")

top_headlines = newsapi.get_top_headlines(q='ukraine', language='en')
articles = top_headlines["articles"]

doc_id = 1
for article in articles:
  article_doc = {
    "headline": article["title"],
    "source": article["source"]["name"],
    "url": article["url"],
    "timestamp": article["publishedAt"]
  }

  response = es.index(index="top-headlines", id=doc_id, document=article_doc)
  print(f"Doc #{doc_id} response: {response['result']}")
  doc_id += 1

