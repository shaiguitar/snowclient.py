import os
import json
import pprint
from snowclient.client import Client
from snowclient.querybuilder import QueryBuilder

# set up the client with the correct URL
with open(os.path.join(os.path.expanduser("~"), ".snow-auth.json")) as data_file:
    user, password = json.load(data_file)
client = Client("https://autodeskcloudopsstg.service-now.com", user, password)

pp = pprint.PrettyPrinter(indent=4)
a = client.api

items = a.catalog_api.items()

pp.pprint("items found:")
pp.pprint(list(map(lambda x: x.name, items)))


catalogs = a.catalog_api.catalogs()

pp.pprint("catalogs found:")
pp.pprint(list(map(lambda x: [x.title, x.sys_id], catalogs)))

i = catalogs[0].sys_id
categories = a.catalog_api.categories(i)

pp.pprint("categories found:")
pp.pprint(categories[0].__dict__)

