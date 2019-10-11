#!/usr/bin/env python

"""
author: ares
date: 2019/9/3
desc:
"""

from abc import ABCMeta, abstractmethod

from database_clients.redis_cli import redis_cli


class Observer(metaclass=ABCMeta):
    """Observer"""

    def __init__(self, name, service):
        self.name = name
        service.register(self)

    @abstractmethod
    def update(self, msg, sender, m_type):
        """update msg"""
        pass


class MsgObserver(Observer):
    """msg observer"""

    def __init__(self, name, manager):
        super(MsgObserver, self).__init__(name, manager)

    def send(self, reciver, msg, type):
        """ send msg """
        msg_dict = {
            'type': type,
            'data': msg
        }
        redis_cli.hmset('msg:{sender}:{reciver}'.format(sender=self.name, reciver=reciver), msg_dict)

    def update(self, msg, sender, m_type):
        """
        update msg
        定义向前端发送信息的接口
        """
        print('\033[0;31;40m{sender}\033[0m[{type}]:\033[0;33;40m{msg}\033[0m'.format(sender=sender, type=m_type,
                                                                                      msg=msg))


class MailObserver(Observer):
    """mail observer"""

    def __init__(self, name, manager):
        super(MailObserver, self).__init__(name, manager)

    def update(self, msg, sender, m_type):
        """update msg"""
        pass


class Broker(object):
    """User object"""
    def __init__(self, name, msg_handler):
        self.name = name
        self.msg_handler = msg_handler
        self._users = {}

    def get(self, name):
        """get user"""
        if name not in self._users:
            user = MsgObserver(name, self.msg_handler)
            self._users.setdefault(name, user)
        return self._users[name]

    def delete(self, name):
        """delete user"""
        try:
            del self._users[name]
        except KeyError as e:
            print('KeyError: user {} not exists!'.format(name))


