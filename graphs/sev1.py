import os
import json
import random
from datetime import datetime
import pprint
from snowclient.client import Client
from snowclient.querybuilder import QueryBuilder

pp = pprint.PrettyPrinter(indent=2)

def build_query():
  qb = QueryBuilder()
  # we want to limit date/timespan to "recent incidents"
  start = datetime.strptime('2017-01-01 00:00:00', "%Y-%m-%d %H:%M:%S")
  end = datetime.strptime('2017-06-14 23:59:59', "%Y-%m-%d %H:%M:%S")
  qb.between(start, end)
  qb.orderbydesc("sys_created_on")

  # SEV1
  qb.field_equals("severity", "1")
  return qb.return_query

# set up the creds in ~/.snow-auth.json with ['user', 'pass']
with open(os.path.join(os.path.expanduser("~"), ".snow-auth.json")) as data_file:
    user, password = json.load(data_file)

# set up the client with the correct URL
client = Client("https://autodeskcloudops.service-now.com", user, password)
incidents = client.list("incident", sysparm_limit=10000, sysparm_query=build_query())

# print(incidents[4].__dict__)

results = map(lambda i: [client.resolve_link(i, "cmdb_ci").name, i], incidents)

for service, incident in results:
    print("#### SERVICE: %s" % service)
    print("Created: %s" % incident.sys_created_on)
    print("\t\t")
    print(incident.description)
    print
