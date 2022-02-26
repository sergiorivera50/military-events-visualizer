from helper import fetch_api_key, connect_elasticsearch

api_id, api_key = fetch_api_key("python-inject-script")
es = connect_elasticsearch(api_id, api_key)


