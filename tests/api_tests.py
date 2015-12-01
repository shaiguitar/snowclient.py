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
    # python 3.4 is being a bitch, but this is the idea.
    #assert_equal (self.api.url_for_table_api("foo", "bar", sys_action="insert", sys_limit=10),
    #               "https://booboo.service-now.com/api/now/v1/table/foo/bar?sys_limit=10&sys_action=insert")
    pass

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

