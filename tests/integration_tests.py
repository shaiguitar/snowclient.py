# REAL REQUESTS.

from nose.tools import *
from snowclient.client import Client
from snowclient.querybuilder import QueryBuilder
import os
import json
import unittest
import tests.test_helpers as test_helpers

import responses # mock
import re

class TestClient(unittest.TestCase):

  def setUp(self):
      curr_dir = os.path.dirname(os.path.abspath(__file__))
      with open(os.path.join(curr_dir, "..", 'basic-auth.json')) as data_file:
          user, password = json.load(data_file)
      self.client = Client("https://autodeskcloudops.service-now.com", user, password)

  def test_list_limit(self):
      assert_equal(len(self.client.list("cmdb_ci", sysparm_limit=5)), 5)

  def test_list_date_range(self):
    qb = QueryBuilder()
    start = test_helpers.to_date('2014-11-01 00:00:00')
    end = test_helpers.to_date('2015-11-01 00:00:00')
    qb.between(start, end)
    lst = self.client.list("cmdb_ci", sysparm_limit=5, sysparm_query=qb.return_query)
    # ensure they are all in the range.
    assert(all(map(lambda x, start=start: test_helpers.to_date(x.sys_created_on) > start,lst)))
    assert(all(map(lambda x, end=end: test_helpers.to_date(x.sys_created_on) < end,lst)))

  def test_order_by(self):
    # sysparm_query=active=true^ORDERBYnumber^ORDERBYDESCcategory
    qb = QueryBuilder()
    qb.orderbydesc('sys_created_on')
    lst = self.client.list("cmdb_ci", sysparm_limit=5,sysparm_query=qb.return_query)
    # fixme this is a moot assertion, because I'm not actually comparing it with the limit
    # oh well this whole sanbox thing is kind of moot really.
    assert(lst[0].sys_created_on > lst[-1].sys_created_on)

  def test_get(self):
    assert(self.client.get("cmdb_ci", "00a0ce4b6f76c24013260519ea3ee4ab"))

  def test_traversing_links(self):
    record = self.client.get("cmdb_ci", "00a0ce4b6f76c24013260519ea3ee4ab")
    assert(record.support_group)
    assert(not hasattr(record.support_group, "manager"))
    self.client.resolve_links(record)
    assert(record.support_group)
    assert(record.support_group.manager)
    assert_equal(record.support_group.table_name(), "sys_user_group")
