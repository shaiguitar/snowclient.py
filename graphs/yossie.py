import os
import json
import random
from datetime import datetime
import pprint

from itertools import chain # flatten
import sys
from snowclient.client import Client
from snowclient.querybuilder import QueryBuilder
import ipdb

user, password = os.environ['auth'].split(":")
moniker = 'WIPDM-S-EW1'
client = Client("https://boobooservicecloudops.service-now.com", user, password)
applications = client.list("u_cloudops_application_router", sysparm_display_value=True)
for app in applications:
  if 'u_service_moniker_id' in app.__dict__ and app.u_service_moniker_id == moniker:
    print moniker,app.business_service['display_value']
    service = app.resolve_link('business_service')
    print service
