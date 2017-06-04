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

## catalogs are the big picture "service catalogs" in the system.
## in our case, 1-1 snow system.
#catalogs = a.catalog_api.catalogs()
#
#pp.pprint("catalogs found:")
#pp.pprint(list(map(lambda x: [x.title, x.sys_id], catalogs)))
#
#catalog = a.catalog_api.catalog(catalogs[0].sys_id)
#
#pp.pprint("specific catalog found:")
#pp.pprint(catalog.__dict__)
#
#catalog_id = catalogs[0].sys_id
#
## categories are where groups of items are stored.
## for example, "Cloud Operations Engineering - Service"
## could be a category of items, wherein the specific items would be... (listed below)
#categories = a.catalog_api.categories(catalog_id)
#
#pp.pprint("categories found:")
#pp.pprint(list(map(lambda x: x.title, categories)))

items = a.catalog_api.items(sysparm_limit=10000)

pp.pprint("moniker items found len: %s" % len(items))
moniker_items = filter(lambda i: "moniker" in i.name.lower(),items)
pp.pprint(list(map(lambda x: [x.name, x.sys_id], items)))

# etc
item = a.catalog_api.item("dc1eaaf9870c7500537a9ffd19434db4")

pp.pprint("specific item found:")
pp.pprint(item.__dict__)




