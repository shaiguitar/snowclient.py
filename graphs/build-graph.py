def debug(msg):
    print("\nDBG: %s\n" % msg)

import os
import pickle
import json
import random
import time
import ipdb
import pprint
import signal # ctr-c
from collections import defaultdict
from datetime import datetime

# use local
import sys
sys.path.append("/Users/shai/r/snowclient.py")
from snowclient.client import Client
from snowclient.client import SnowRecord
from snowclient.querybuilder import QueryBuilder

def recent_range():
    qb = QueryBuilder()
    start = datetime.strptime('2017-5-15 00:00:00', "%Y-%m-%d %H:%M:%S")
    end = datetime.strptime('2017-5-17 23:59:59', "%Y-%m-%d %H:%M:%S")
    qb.between(start, end)
    qb.orderbydesc("sys_created_on")
    return qb.return_query

# set up the client with the correct URL
with open(os.path.join(os.path.expanduser("~"), ".snow-auth.json")) as data_file:
    user, password = json.load(data_file)
client = Client("https://autodeskcloudops.service-now.com", user, password)

# snow_record = client.list("incident", sysparm_limit=1, sysparm_query=recent_range())[0]
# debug("Sys id for incident: %s" % snow_record.sys_id)

# graph can look like
# {
#   nodeA: [nodeB, NodeC]
#   nodeC: [nodeB]
#   nodeB: []
# }
#
# node identifiers are the type (the tablename), and it's sys_id.

ident_lookup = {} # keep track of records
graph_data = defaultdict(list) # hold the graph in this.
# start_from = snow_record

# me!
start_at_user_shai = client.get("sys_user", "7b4780ea6f6eb1005b6407321c3ee495")

def do_before_exit():
    print('You pressed Ctrl+C!')
    print('here is the graph so far:')
    pp = pprint.PrettyPrinter(depth=2)
    pp.pprint(graph_data)
    print('going to write it out to a file')
    afile = open(r'graph-from-shai.pickle', 'wb')
    pickle.dump(graph_data, afile)
    afile.close()
    sys.exit(0)

def signal_handler(signal, frame):
    do_before_exit()

# run this file, collect data into +graph_data+ and then ctr-c eventually.
signal.signal(signal.SIGINT, signal_handler)

def register(record):
    ident_lookup[record.identtuple()] = record

def visited(record):
    if record.identtuple() in ident_lookup:
        return True
    else:
        return False

def traverse_data(record):
    # vertex/and it's neigbour node variables
    v = record
    n = None

    # use for BFS
    queue = []

    # ident: bool
    queue.append(v)
    # keep track of {ident: record}
    register(v)

    while queue:

        # dequeue a vertex
        v = queue.pop(0)

        debug("popped: %s" % str(v.identtuple()))
        debug("registered already: %s" % str(ident_lookup.keys()))
        debug("will resolve these links: %s" % v.links())

        # could potentially make this better by just
        # getting the links we haven't visited already.
        # it's ok for now though I guess.
        new_records = v.resolve_links()

        # for the record's adjacent vertices...
        for n in new_records:

            # 'do the work' ... build a graph.
            # don't add in notfound
            if type(v) is SnowRecord:
                graph_data[v.identtuple()].append(n.identtuple())

            if isinstance(n, SnowRecord):
                # if we haven't visited it, mark it and enqueue.
                if not visited(n):
                    register(n)
                    queue.append(n)
            elif isinstance(n, SnowRecord.NotFound):
                debug("Record was not found? %s(%s)" % n.identtuple())
            else:
                debug("Problem? %s" % n)

    return "done"

traverse_data(start_at_user_shai)

do_before_exit()
