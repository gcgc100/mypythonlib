import unittest
import sys
from os import path
sys.path.insert(0, path.join(path.dirname(path.abspath(__file__)), ".."))
import sqliteDB  # nopep8


class TestSqliteDB(unittest.TestCase):

    """Test case docstring."""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_textWithQuote(self):
        if sqliteDB.engine is None:
            sqliteDB.create_engine('test.db')
        sqliteDB.update("create table if not exists test (key text)")
        print "aaa"
        sqliteDB.insert('test', **{"key": '<selenium."8f35c24c", "0.097-24")>'})
        print "bbb"
