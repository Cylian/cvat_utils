from pprint import pprint
from time import sleep
from cvat_sdk.api_client import Configuration, ApiClient, exceptions
from cvat_sdk.api_client.models import *

# Set up an API client
# Read Configuration class docs for more info about parameters and authentication methods
configuration = Configuration(
    host="http://43.204.240.199",
    username="cylian",
    password="draConian1",
    _parse_response = False
)

with ApiClient(configuration) as api_client:
    (_, response) = api_client.tasks_api.retrieve_dataset(
        id=42,
        format="COCO 1.0",
        _parse_response=False,
    )
    print(response)
