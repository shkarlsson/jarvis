from elasticsearch import Elasticsearch

# Setting working dir two parents up
# import os

# os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# %%
from app.helpers.env_vars import ES_HOST, ES_API_KEY


def get_zigbee_device_names():
    """Returns a list of the names of the devices that have sent data to the ES index within the last 24 hours."""

    # , filtered by location 'Stockholm' and excluding devices starting with '0x'.

    # Initialize the client
    es = Elasticsearch([ES_HOST], api_key=ES_API_KEY, verify_certs=False)

    search_query = {
        "size": 0,
        "query": {
            "bool": {
                "must": [
                    {"term": {"location": "stockholm"}},
                    {"range": {"timestamp": {"gte": f"now-24h"}}},
                ],
                "must_not": [{"prefix": {"device": "0x"}}],
            }
        },
        "aggs": {
            "unique_devices": {
                "terms": {
                    "field": "device",
                    "size": 1000,
                    "order": {"latest": "desc"},
                },
                "aggs": {"latest": {"max": {"field": "timestamp"}}},
            }
        },
    }
    response = es.search(index="zigbees", body=search_query)
    es.transport.close()
    return [
        device["key"]
        for device in response["aggregations"]["unique_devices"]["buckets"]
    ]


# %%
