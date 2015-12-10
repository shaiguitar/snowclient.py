import os
import json
import pprint
from snowclient.client import Client

# set up the creds in ~/.snow-auth.json with ['user', 'pass']
with open(os.path.join(os.path.expanduser("~"), ".snow-auth.json")) as data_file:
    user, password = json.load(data_file)

# set up the client with the correct URL
client = Client("https://your-sandbox.service-now.com", user, password)

pp = pprint.PrettyPrinter(indent=4)

try:
    not_found = client.list("not_found_error_json_response")
except SnowError:
    print("could not find records...")
