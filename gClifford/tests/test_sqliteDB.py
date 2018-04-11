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
        sqliteDB.insert('test', **{"key": 'aaa'})
        row = sqliteDB.select("select * from test where key=?", "aaa")
        self.assertEqual(len(row), 1)
        self.assertEqual(row[0].key, "aaa")
        sqliteDB.update("delete from test")
