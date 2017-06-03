from nose.tools import *
from snowclient.api import *
import os
import json
import unittest

import responses # mock
import re

class TestApi(unittest.TestCase):

  def setUp(self):
      self.api = Api("https://booboo.service-now.com", "foo", "pass")

  def test_url_for_table_api(self):
    assert_equal (self.api.url_for_table_api("foo", "bar", sys_action="insert", sys_limit=10),
                   "https://booboo.service-now.com/api/now/v1/table/foo/bar?sys_action=insert&sys_limit=10")

  # https://docs.servicenow.com/bundle/istanbul-servicenow-platform/page/integrate/inbound-rest/concept/c_ServiceCatalogAPI.html
  # def test_url_for_catalog_api(self):
  #   assert_equal (self.api.url_for_catalog_api("foo", "bar", sys_action="insert", sys_limit=10),
  #                  "https://booboo.service-now.com/api/sn_sc/v1/servicecatalog/items")

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

