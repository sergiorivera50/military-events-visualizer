from helper import connect_elasticsearch

es = connect_elasticsearch("python-inject-script")

es.indices.create(index="top-headlines")
