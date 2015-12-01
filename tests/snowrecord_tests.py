from nose.tools import *
from snowclient.snowrecord import *
import unittest

class TestSnowRecord(unittest.TestCase):
  def setUp(self):
      self.record_data = {'a': 1, 'b': 2}
      self.snow_record = SnowRecord("table_name", **self.record_data)

  def test_object_read_attr(self):
      assert_equal(self.snow_record.a, 1)
      assert_equal(self.snow_record.b, 2)

  def test_object_write_attr(self):
      # do I really want this / should it be ro access?
      self.snow_record.d = 3
      assert_equal(self.snow_record.d, 3)

  def test_object_must_have_table_name(self):
      try:
        SnowRecord(None, **self.record_data)
      except TypeError:
        assert("Must init with a table_name value")

  def test_table_name_private_attr(self):
      sr = SnowRecord("mytablename", **self.record_data)
      assert_equal(sr.table_name(), "mytablename")
      try:
          sr.table_name = "other whatev"
      except:
        assert("table name is not assignable.")
