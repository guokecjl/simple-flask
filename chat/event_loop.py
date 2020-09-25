#!/usr/bin/env python

"""
author: ares
date: 2019/8/27
desc:
"""


class MsgManager(object):
    """msg manager"""

    def __init__(self, name):
        self.name = name
        self.observers = []

    def register(self, observer):
        """ register users """
        self.observers.append(observer)

    def cancel(self, observer):
        """ logout users """
        self.observers.remove(observer)

    def notify_all(self):
        """ notify observer """
        pass


class EventLoop(object):
    """Event Loop"""

    def __init__(self, msg_manager):
        self._running = False
        self._stopped = False
        self._closing = False
        self.msg_manager = msg_manager



