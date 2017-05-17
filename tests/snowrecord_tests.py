from nose.tools import *
from snowclient.snowrecord import *
import unittest
from unittest.mock import MagicMock

class TestSnowRecord(unittest.TestCase):
  def setUp(self):

      self.mock_client = MagicMock()
      self.record_data = {'a': 1, 'b': 2}
      self.snow_record = SnowRecord(self.mock_client, "table_name", **self.record_data)

      # with link
      self.record_data_links = {'a': 1, 'b': 2,
                                  'c': {'link': 'https://booboo.service-now.com/api/now/v1/table/c/id'},
                                  'd': {'link': 'https://booboo.service-now.com/api/now/v1/table/d/id'}
      }

      self.snow_record_2 = SnowRecord(self.mock_client, "table_name", **self.record_data_links)

  def test_tablename_from_link(self):
      assert_equal(
        SnowRecord.tablename_from_link("https://booboo.service-now.com/api/now/v1/table/foobar/id"),
        "foobar"
      )

  # some other time.
  #
  # def test_object_is_subscriptable(self):
  #   print(self.snow_record._attrs)
  #   assert_equal(self.snow_record['a'], 1)

  def test_object_has_links(self):
      assert_equal(
        self.snow_record_2.links(),
        {
          "c": "https://booboo.service-now.com/api/now/v1/table/c/id",
          "d": "https://booboo.service-now.com/api/now/v1/table/d/id"
        }
      )

  def test_object_read_attr(self):
      assert_equal(self.snow_record.a, 1)
      assert_equal(self.snow_record.b, 2)

  def test_object_write_attr(self):
      # do I really want this / should it be ro access?
      self.snow_record.d = 3
      assert_equal(self.snow_record.d, 3)

  def test_object_must_have_table_name(self):
      try:
        SnowRecord(self.mock_client, None, **self.record_data)
      except TypeError:
        assert("Must init with a table_name value")

  def test_table_name_private_attr(self):
      sr = SnowRecord(self.mock_client, "mytablename", **self.record_data)
      assert_equal(sr._table_name, "mytablename")
      try:
          sr.table_name = "other whatev"
      except:
        assert("table name is not assignable.")

  def test_has_a_not_found_placeholder(self):
    nf = SnowRecord.NotFound(self.mock_client, "tablename", "msg", [1, 2, 3])
    assert_equal(nf.msg, "msg")
    assert_equal(nf._table_name, "tablename")
    assert_equal(nf.data, [1, 2, 3]) #anything

    assert_equal(nf.identtuple(), ("tablename", "1,2,3")) #anything
