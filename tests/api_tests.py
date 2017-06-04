from nose.tools import *
from snowclient.api import *
import os
import json
import unittest
import pprint
import responses # mock
import re

class TestApi(unittest.TestCase):

  def setUp(self):
      self.curr_dir = os.path.dirname(os.path.abspath(__file__))
      self.api = Api("https://booboo.service-now.com", "foo", "pass")
      self.catalog_api = self.api.catalog_api
      self._setup_mocking()

  def test_url_for_api(self):
    assert_equal (self.api.url_for_api("/api/now/v1/table", "foo", "bar", sys_action="insert", sys_limit=10),
                   "https://booboo.service-now.com/api/now/v1/table/foo/bar?sys_action=insert&sys_limit=10")

  @responses.activate
  def test_generic_request(self):
    """
    generic requests that is just a proxy for "requests" module
    but adds in the basic auth in real impl
    """
    responses.add(responses.GET, "http://foo.com/bar.json",
                  body= '{"1":2}',
                  status=200,
                  content_type='application/json')
    assert_equal(self.api.req("get", "http://foo.com/bar.json").json(), {u'1': 2})


  def _setup_mocking(self):
    # https://docs.servicenow.com/bundle/istanbul-servicenow-platform/page/integrate/inbound-rest/concept/c_ServiceCatalogAPI.html

    re_catalog_items = re.compile(r'https?://booboo.service-now.com/api/sn_sc/v1/servicecatalog/items')

    with open(os.path.join(self.curr_dir, "support/", 'catalog_items.json')) as data_file:
      catalog_items_json = data_file.read()

    responses.add(responses.GET, re_catalog_items,
                  body=catalog_items_json,
                  status=200,
                  content_type='application/json')

  @responses.activate
  def test_catalog_api(self):
    items = self.catalog_api.items()
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(items)
    assert_equal(len(items) > 0, True)

  # this can be tested if integration tests were a thing.
  #
  #  def test_catalog_api_limit(self):
  #    items = self.catalog_api.items(sysparm_limit=1)
  #    pp = pprint.PrettyPrinter(indent=4)
  #    pp.pprint(items)
  #    assert_equal(len(items) == 1, True)
