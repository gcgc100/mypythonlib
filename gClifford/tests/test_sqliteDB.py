import unittest
import sys
from os import path
sys.path.insert(0, path.join(path.dirname(path.abspath(__file__)), ".."))
import sqliteDB  # nopep8


class TestSqliteDB(unittest.TestCase):

    """Test case docstring."""

    def setUp(self):
        if sqliteDB.engine is None:
            sqliteDB.create_engine('test.db')
        sqliteDB.update("create table if not exists test (key text, v text)")

    def tearDown(self):
        pass

    def test_textWithQuote(self):
        sqliteDB.insert('test', **{"key": 'aa'})
        sqliteDB.update("update test set key=?", "aaa")
        row = sqliteDB.select("select * from test where key=?", "aaa")
        self.assertEqual(len(row), 1)
        self.assertEqual(row[0].key, "aaa")
        sqliteDB.update("delete from test")

    def test_time(self):
        import time
        t1 = time.time()
        for i in range(100):
            sqliteDB.insertNoCommit('test', **{"key": 'a'})
        sqliteDB.insert('test', **{"key": 'a'})
        t2 = time.time()
        print(t2-t1)
        sqliteDB.update("delete from test")


    def test_rowid(self):
        ret = sqliteDB.insert('test', **{"key": 'aaaa'})
        rowcount = ret[0]
        rowid = ret[1]
        print("Insert %s rows, row id: %s" % (rowcount, rowid))
        for i in range(100):
            ret = sqliteDB.insertNoCommit('test', **{"key": 'bbb'})
            rowcount = ret[0]
            rowid = ret[1]
            print("Insert %s rows, row id: %s" % (rowcount, rowid))
        sqliteDB.update("delete from test")
