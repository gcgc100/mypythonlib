#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Dispatcher

Dispatch a task to a new thread.
"""

__all__ = ["dispatch", "handle"]

from threading import Thread
from functools import wraps
import os, time

class handle(object):
    """Handle for dispatcher. Returned by dispatch function. Used for complex operation, for example: Cancel delay task"""
    def __init__(self):
        super(handle, self).__init__()
        self._cancelDelay = False
    
    def cancelTheDelayTask(self):
        """Cancel the delay task"""
        self._cancelDelay = True
    
    def cancelDelay():
        doc = "The cancelDelay property."
        def fget(self):
            return self._cancelDelay
        def fset(self, value):
            self._cancelDelay = value
        def fdel(self):
            del self._cancelDelay
        return locals()
    cancelDelay = property(**cancelDelay())
    

def timeout(seconds):
    def decorator(func):

        def wrapper(*args, **kwargs):
            time.sleep(seconds)
            result = func(*args, **kwargs)
            return result

        return wraps(func)(wrapper)

    return decorator


def dispatch(target, delaytime=0):
    """Dispatch a task to a new trhead. Run the target after delay delaytime"""
    retHandle = handle()
    @timeout(delaytime)
    def func():
        if retHandle.cancelDelay is not True:
            target()
    t = Thread(target=func)
    t.start()
    return retHandle
