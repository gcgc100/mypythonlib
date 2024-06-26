#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
if db.engine is None:
    db.create_engine(user, password, database)
db.select("select * from table where id = ?", id)
db.insert(tableName, **ditc)
db.update("update table set name = ? where id = ?", name, id)


def _createEngine(func):
    @functools.wraps(func)
    def _wrapper(*args, **kw):
        if db.engine is None:
            db.create_engine(user, pwd, dbname)
        return func(*args, **kw)
    return _wrapper

@_createEngine
def myselect:
    pass
@_createEngine
def myinsert:
    pass
"""

__all__ = ["create_engine", "select", "update", "insert", "select_int", "select_one"]
import logging
import functools
import threading
import time


class Dict(dict):
    '''
    Simple dict but support access as x.y style.

    >>> d1 = Dict()
    >>> d1['x'] = 100
    >>> d1.x
    100
    >>> d1.y = 200
    >>> d1['y']
    200
    >>> d2 = Dict(a=1, b=2, c='3')
    >>> d2.c
    '3'
    >>> d2['empty']
    Traceback (most recent call last):
        ...
    KeyError: 'empty'
    >>> d2.empty
    Traceback (most recent call last):
        ...
    AttributeError: 'Dict' object has no attribute 'empty'
    >>> d3 = Dict(('a', 'b', 'c'), (1, 2, 3))
    >>> d3.a
    1
    >>> d3.b
    2
    >>> d3.c
    3
    '''

    def __init__(self, names=(), values=(), **kw):
        super(Dict, self).__init__(**kw)
        for k, value in zip(names, values):
            self[k] = value

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value


class DBError(Exception):
    """docstring for DBError"""
    pass


class MultiColumnsError(DBError):
    """
    MultiColumnsError
    """
    pass

class _LasyConnection(object):
    """
    lasy connect
    """
    def __init__(self):
        self.connection = None

    def cursor(self):
        """
        return cursor
        """
        if self.connection is None:
            _connection = engine.connect()
            logging.info('open connection <%s>...', hex(id(_connection)))
            self.connection = _connection
        return self.connection.cursor()

    def commit(self):
        """
        commit the operate
        """
        self.connection.commit()

    def rollback(self):
        """
        roll back the operate
        """
        self.connection.rollback()

    def cleanup(self):
        """
        Clean up the connection
        """
        if self.connection:
            _connection = self.connection
            self.connection = None
            logging.info('close connection <%s>...' , hex(id(_connection)))
            _connection.close()


class _DbCtx(threading.local):
    '''
    Thread local object that holds connection info.
    '''

    def __init__(self):
        self.connection = None
        self.transactions = 0

    def is_init(self):
        """
        check if it is inited
        """
        return self.connection is not None

    def init(self):
        """
        Open lazy connection
        """
        logging.info('open lazy connection...')
        self.connection = _LasyConnection()
        self.transactions = 0

    def cleanup(self):
        """
        Clean up the connection
        """
        self.connection.cleanup()

    def cursor(self):
        '''
        Return cursor
        '''
        return self.connection.cursor()

_db_ctx = _DbCtx()

engine = None


class _Engine(object):
    """
    Engine object
    """
    def __init__(self, connect):
        self._connect = connect

    def connect(self):
        """
        connect
        """
        return self._connect()


def create_engine(user, password, database, host='127.0.0.1', port=3306, **kw):
    """docstring for create_engine"""
    import mysql.connector
    global engine
    if engine is not None:
        raise DBError('Engine is already initialized.')
    params = dict(
        user=user,
        password=password,
        database=database,
        host=host,
        port=port)
    defaults = dict(
        use_unicode=True,
        charset='utf8',
        collation='utf8_general_ci',
        autocommit=False)
    for k, value in defaults.items():
        params[k] = kw.pop(k, value)
    params.update(kw)
    params['buffered'] = True
    engine = _Engine(lambda: mysql.connector.connect(**params))
    logging.info(engine.connect())
    logging.info('Init mysql engine <%s> ok.', hex(id(engine)))


class _ConnectionCtx(object):
    '''
    _ConnectionCtx object that can open and close
    connection context. _ConnectionCtx object can be nested and only the most
    outer connection has effect.

    with connection():
        pass
        with connection():
            pass
    '''

    def __enter__(self):
        global _db_ctx
        self.should_cleanup = False
        if not _db_ctx.is_init():
            _db_ctx.init()
            self.should_cleanup = True
        return self

    def __exit__(self, exctype, excvalue, traceback):
        global _db_ctx
        if self.should_cleanup:
            _db_ctx.cleanup()


def connection():
    '''
    Return _ConnectionCtx object that can be used by 'with' statement:

    with connection():
        pass
    '''
    return _ConnectionCtx()


def with_connection(func):
    """
    Decorator for reuse connection.

    @with_connection
    def foo(*args, **kw):
        f1()
        f2()
        f3()
    """
    @functools.wraps(func)
    def _wrapper(*args, **kw):
        with _ConnectionCtx():
            return func(*args, **kw)
    return _wrapper


def _select(sql, first, *args):
    """execute select SQL and return unique result or list results"""
    global _db_ctx
    cursor = None
    sql = sql.replace('?', '%s')
    logging.info('SQL: %s, ARGS: %s' , sql, args)
    try:
        cursor = _db_ctx.connection.cursor()
        cursor.execute(sql, args)
        if cursor.description:
            names = [x[0] for x in cursor.description]
        if first:
            values = cursor.fetchone()
            if not values:
                return None
            return Dict(names, values)
        return [Dict(names, x) for x in cursor.fetchall()]
    finally:
        if cursor:
            cursor.close()


@with_connection
def select_one(sql, *args):
    """
    Execute select SQL and expected one result.
    If no result found, return None.
    If multiple results found, the first one returned.

    >>> u1 = dict(id=100, name='Alice', email='alice@test.org', \
passwd='ABC-12345', last_modified=time.time())
    >>> u2 = dict(id=101, name='Sarah', email='sarah@test.org', \
 passwd='ABC-12345', last_modified=time.time())
    >>> insert('user', **u1)
    1
    >>> insert('user', **u2)
    1
    >>> u = select_one('select * from user where id=?', 100)
    >>> u.name
    u'Alice'
    >>> select_one('select * from user where email=?', 'abc@email.com')
    >>> u2 = select_one('select * from user where passwd=? order by email', \
'ABC-12345')
    >>> u2.name
    u'Alice'
    """
    return _select(sql, True, *args)


@with_connection
def select_int(sql, *args):
    '''
    Execute select SQL and expected one int and only one int result.

    >>> n = update('delete from user')
    >>> u1 = dict(id=96900, name='Ada', email='ada@test.org', \
passwd='A-12345', last_modified=time.time())
    >>> u2 = dict(id=96901, name='Adam', email='adam@test.org', \
passwd='A-12345', last_modified=time.time())
    >>> insert('user', **u1)
    1
    >>> insert('user', **u2)
    1
    >>> select_int('select count(*) from user')
    2
    >>> select_int('select count(*) from user where email=?', 'ada@test.org')
    1
    >>> select_int('select count(*) from user where email=?', \
'notexist@test.org')
    0
    >>> select_int('select id from user where email=?', 'ada@test.org')
    96900
    >>> select_int('select id, name from user where email=?', 'ada@test.org')
    Traceback (most recent call last):
        ...
    MultiColumnsError: Expect only one column.
    '''
    d = _select(sql, True, *args)
    if len(d) != 1:
        raise MultiColumnsError('Expect only one column.')
    return list(d.values())[0]


@with_connection
def select(sql, *args):
    '''
    Execute select SQL and return list or empty list if no result.

    >>> u1 = dict(id=200, name='Wall.E', email='wall.e@test.org', \
passwd='back-to-earth', last_modified=time.time())
    >>> u2 = dict(id=201, name='Eva', email='eva@test.org', \
passwd='back-to-earth', last_modified=time.time())
    >>> insert('user', **u1)
    1
    >>> insert('user', **u2)
    1
    >>> L = select('select * from user where id=?', 900900900)
    >>> L
    []
    >>> L = select('select * from user where id=?', 200)
    >>> L[0].email
    u'wall.e@test.org'
    >>> L = select('select * from user where passwd=? order by id desc', \
'back-to-earth')
    >>> L[0].name
    u'Eva'
    >>> L[1].name
    u'Wall.E'
    '''
    return _select(sql, False, *args)


@with_connection
def _update(sql, *args):
    global _db_ctx
    cursor = None
    sql = sql.replace('?', '%s')
    logging.info('SQL: %s, ARGS: %s' , sql, args)
    try:
        cursor = _db_ctx.connection.cursor()
        cursor.execute(sql, args)
        ret = cursor.rowcount
        if _db_ctx.transactions == 0:
            logging.info('auto commit')
            _db_ctx.connection.commit()
        return ret
    finally:
        if cursor:
            cursor.close()


def insert(table, **kw):
    '''
    Execute insert SQL.

    >>> u1 = dict(id=2000, name='Bob', email='bob@test.org',
    ... passwd='bobobob', last_modified=time.time())
    >>> insert('user', **u1)
    1
    >>> u2 = select_one('select * from user where id=?', 2000)
    >>> u2.name
    u'Bob'
    >>> insert('user', **u2)
    Traceback (most recent call last):
      ...
    IntegrityError: 1062 (23000): Duplicate entry '2000' for key 'PRIMARY'
    '''
    cols, args = zip(*kw.items())
    sql = 'insert into `%s` (%s) values (%s)' % (table, ','.join(['`%s`' % col for col in cols]),
                                                 ','.join(['?' for i in range(len(cols))]))
    return _update(sql, *args)


def update(sql, *args):
    r'''
    Execute update SQL.

    >>> u1 = dict(id=1000, name='Michael', email='michael@test.org',
    ... passwd='123456', last_modified=time.time())
    >>> insert('user', **u1)
    1
    >>> u2 = select_one('select * from user where id=?', 1000)
    >>> u2.email
    u'michael@test.org'
    >>> u2.passwd
    u'123456'
    >>> update('update user set email=?, passwd=? where id=?',
    ... 'michael@example.org', '654321', 1000)
    1
    >>> u3 = select_one('select * from user where id=?', 1000)
    >>> u3.email
    u'michael@example.org'
    >>> u3.passwd
    u'654321'
    >>> update('update user set passwd=? where id=?', '***',
    ... '123\' or id=\'456')
    0
    '''
    return _update(sql, *args)
