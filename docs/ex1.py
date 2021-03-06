import os
import json
import random
import datetime
import pprint
from snowclient.client import Client
from snowclient.querybuilder import QueryBuilder

def build_query():
    qb = QueryBuilder()
    start = datetime.strptime('2015-11-17 00:00:00', "%Y-%m-%d %H:%M:%S")
    end = datetime.strptime('2015-11-20 23:59:59', "%Y-%m-%d %H:%M:%S")
    qb.between(start, end)
    qb.orderbydesc("sys_created_on")
    return qb.return_query

# set up the creds in ~/.snow-auth.json with ['user', 'pass']
with open(os.path.join(os.path.expanduser("~"), ".snow-auth.json")) as data_file:
    user, password = json.load(data_file)

# set up the client with the correct URL
client = Client("https://your-sandbox.service-now.com", user, password)

pp = pprint.PrettyPrinter(indent=4)

# use whatever table name is appropriate...
recent_incidents = client.list("incident", sysparm_limit=1000, sysparm_query=build_query())

pp.pprint("dates of incidents found:")
pp.pprint(list(map(lambda x: x.sys_created_on, recent_incidents)))

a_record = random.choice(recent_incidents)
a_record_attrs = a_record.__dict__

# do things with ze data
print("this recored has %s attributes/fields." % len(a_record_attrs))
print("for example:")
print("============")
print()

# eg
#
#  for an_attr, a_val in a_record_attrs.items():
#      if a_val and isinstance(a_val, str):
#          print("%s is %s" % [a_val, an_attr])
#
#  # you can dereference embeded <link> results
#  # this doesn't recurse, just goes one level deep
#  # and replaces the <link> with a new snow_record.
#  print("deferencing links from record...")
#  a_record.resolve_links()
#
#  # linked objects will show up as their own records.
#  print(a_record)
