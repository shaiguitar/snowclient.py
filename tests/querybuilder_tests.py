from nose.tools import *
from snowclient.querybuilder import *
import unittest
import tests.test_helpers as test_helpers

class TestSnowClientQuery(unittest.TestCase):
  def test_date_range(self):
      qb = QueryBuilder()
      # snow api sucks balls https://community.servicenow.com/thread/181519
      e = "sys_created_on_ze_dateBETWEENjavascript:gs.dateGenerate('2015-04-16','00:10:00')@javascript:gs.dateGenerate('2015-04-22','12:59:59')"
      start = test_helpers.to_date('2015-04-16 00:10:00')
      end = test_helpers.to_date('2015-04-22 12:59:59')
      qb.between(start,end, "sys_created_on_ze_date")
      assert_equal(qb.return_query, e)

  def test_orderby(self):
      qb = QueryBuilder()
      qb.orderby("name")
      assert_equal(qb.return_query, "ORDERBYname")

  def test_chained_queries(self):
      qb = QueryBuilder()
      qb = qb.orderby("name")
      qb = qb.orderbydesc("category")
      assert_equal(qb.return_query, "ORDERBYname^ORDERBYDESCcategory")

  def test_empty_field(self):
      qb = QueryBuilder()
      qb.field_empty("name")
      qb.OR()
      qb.field_empty_string("name")
      assert_equal(qb.return_query, "nameISEMPTY^ORnameEMPTYSTRING")

  def test_not_empty_field(self):
      qb = QueryBuilder()
      qb.field_not_empty("name")
      assert_equal(qb.return_query, "nameISNOTEMPTY")

  def test_chained_or_queries(self):
      qb = QueryBuilder()
      qb.field_equals("name", "bob")
      # OR is used only once. otherwise defaults to AND.
      qb.OR()
      qb.field_equals("name", "alice")
      assert_equal(qb.return_query, "name=bob^ORname=alice")

  def test_chained_or_queries_multi(self):
      qb = QueryBuilder()
      qb.field_equals("name", "bob")
      # OR is used only once. otherwise defaults to AND.
      qb.OR()
      qb.field_equals("name", "alice")
      qb.field_equals("gender", "female")
      assert_equal(qb.return_query, "name=bob^ORname=alice^gender=female")

# don't need to test a private method.
#  def test_format_date(self):
#      qb = QueryBuilder()
#      date = to_date("2015-11-28 12:59:59")
#      # who understands the ways of the snow syntax
#      s = qb.comma_snow_date(date)
#      assert_equal(s, "'2015-11-28','12:59:59'")

