from nose.tools import *
from snowclient.client import Client
from snowclient.querybuilder import QueryBuilder
from snowclient.errors import SnowError
import os
import json
import unittest
import tests.test_helpers as test_helpers
import responses
import re

class TestClient(unittest.TestCase):

# this doesn't work in python 3.4 :(
#  __metaclass__ = test_helpers.class_decorating_meta(
#          'test_',
#          responses.activate)

  def setUp(self):
      self.curr_dir = os.path.dirname(os.path.abspath(__file__))
      with open(os.path.join(self.curr_dir, "..", 'basic-auth.json')) as data_file:
          user, password = json.load(data_file)
      self._setup_mocking()
      self.client = Client("https://booboo.service-now.com", user, password)

  @responses.activate
  def test_list_limit(self):
      assert_equal(len(self.client.list("original_table", sysparm_limit=5)), 5)

  @responses.activate
  def test_list_date_range(self):
    qb = QueryBuilder()
    # xxxmockrefactor
    # this test needs refactoring: its just checking mock data
    # but service now server-side responds with the data correctly (the date query).
    start = test_helpers.to_date('2013-12-31 00:00:00')
    end = test_helpers.to_date('2014-01-01 00:00:00')
    qb.between(start, end)
    lst = self.client.list("original_table", sysparm_limit=5, sysparm_query=qb.return_query)
    # ensure they are all in the range.
    assert(all(map(lambda x, start=start: test_helpers.to_date(x.sys_created_on) > start,lst)))
    assert(all(map(lambda x, end=end: test_helpers.to_date(x.sys_created_on) < end,lst)))

  @responses.activate
  def test_order_by(self):
    # sysparm_query=active=true^ORDERBYnumber^ORDERBYDESCcategory
    #
    # xxxmockrefactor
    # this test needs refactoring: its just checking mock data
    # but service now server-side responds with the data correctly (the orderby query).
    qb = QueryBuilder()
    qb.orderby('sys_created_on')
    lst = self.client.list("original_table", sysparm_limit=5,sysparm_query=qb.return_query)
    # fixme this is a moot assertion, because I'm not actually comparing it with the limit
    # oh well this whole sanbox thing is kind of moot really.
    assert(lst[0].sys_created_on < lst[-1].sys_created_on)

  @responses.activate
  def test_get(self):
    # needs a self.client.get("original_table", "00a0ce4b6f76c24013260519ea3ee4ab") assertion. lazy now.
    pass

  @responses.activate
  def test_traversing_links(self):
    orig_record = self.client.list("original_table")[0]
    assert_equal(orig_record.test_key_orig, "test_val_orig")

    # get links, assert against those.
    linked_record = self.client.api.resolve_links(orig_record)[0]
    # no mutation
    assert_equal(orig_record.test_key_orig, "test_val_orig")

    assert_equal(linked_record.test_key_linked, "test_val_linked")
    assert_equal(linked_record._table_name, "linked_table")

  @responses.activate
  def test_traversing_link(self):
    orig_record = self.client.list("original_table")[0]

    # test kwargs on resolve_links()
    linked_record_resolved_links = self.client.api.resolve_link(orig_record, "linked_obj",sysparm_display_value=True)
    # get links, assert against those.
    linked_record = self.client.api.resolve_link(orig_record, "linked_obj")

    # no mutation
    assert_equal(orig_record.test_key_orig, "test_val_orig")

    assert_equal(linked_record.test_key_linked, "test_val_linked")
    assert_equal(linked_record._table_name, "linked_table")

  @responses.activate
  def test_no_field_to_resolve(self):
    orig_record = self.client.list("original_table")[0]
    try_to_get_field = self.client.api.resolve_link(orig_record, "NO_SUCH_LINK_OR_ATTR_EXISTS")
    assert_equal(try_to_get_field.__class__.__name__, "NotFound" )

  @responses.activate
  def test_record_not_found(self):
    try:
        record = self.client.list("not_found")
    except SnowError as e:
      assert_equal(e.msg, "No Record found")

  def _setup_mocking(self):
    # with ID's
    #
    # re_get_original = re.compile(r'https?://booboo.service-now.com/api/now/v1/table/original_table/\w+')
    # re_get_linked = re.compile(r'https?://booboo.service-now.com/api/now/v1/table/linked_table/\w+')
    #
    # collections
    #
    re_lst_original = re.compile(r'https?://booboo.service-now.com/api/now/v1/table/original_table.*')
    re_lst_linked = re.compile(r'https?://booboo.service-now.com/api/now/v1/table/linked_table.*')
    re_lst_not_found = re.compile(r'https?://booboo.service-now.com/api/now/v1/table/not_found.*')

    with open(os.path.join(self.curr_dir, "support/", 'original_table.json')) as data_file:
      original_json = data_file.read()
    with open(os.path.join(self.curr_dir, "support/", 'linked_table.json')) as data_file:
      linked_json = data_file.read()
    with open(os.path.join(self.curr_dir, "support/", 'error_not_found.json')) as data_file:
      not_found_json = data_file.read()

    responses.add(responses.GET, re_lst_original,
                  body=original_json,
                  status=200,
                  content_type='application/json')

    responses.add(responses.GET, re_lst_linked,
                  body=linked_json,
                  status=200,
                  content_type='application/json')

    responses.add(responses.GET, re_lst_not_found,
                  body=not_found_json,
                  status=200,
                  content_type='application/json')
