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

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def receive(self, msg, sender, m_type):
        """update msg"""
        pass


class MsgObserver(Observer):
    """msg observer"""

    def __init__(self, name, msg_pipe):
        self.msg_pipe = msg_pipe
        super(MsgObserver, self).__init__(name)

    def send(self, reciver, msg, type):
        """ send msg """
        pass

    def receive(self, msg, sender, m_type):
        """
        update msg
        定义向前端发送信息的接口
        """
        msg = ('msg:{sender}:{reciver}:{type}:{msg}'.format(sender=sender, reciver=self.name, type=m_type, msg=msg))
        self.msg_pipe.write_message(msg)


class MailObserver(Observer):
    """mail observer"""

    def __init__(self, name, manager):
        super(MailObserver, self).__init__(name)

    def update(self, msg, sender, m_type):
        """update msg"""
        pass


class Broker(object):
    """User object"""
    def __init__(self, name):
        self.name = name
        self._users = {}

    def create(self, name, msg_pipe):
        """create user"""
        if name not in self._users:
            user = MsgObserver(name, msg_pipe)
            self._users.setdefault(name, user)
            msg_key_list = redis_cli.keys('msg:*:{reciver}'.format(reciver=name))
            for msg_key in msg_key_list:
                while True:
                    data = redis_cli.lpop(msg_key)
                    msg, msg_type = data.split(":")
                    _, sender, reciver = bytes.decode(msg_key).split(':')
                    user.receive(msg, sender, msg_type)
        print('{} is online ^_^ !!!'.format(name))

    def get(self, name):
        """get user"""
        return self._users.get(name, None)

    def delete(self, name):
        """delete user"""
        try:
            del self._users[name]
        except KeyError as e:
            print('KeyError: user {} not exists!'.format(name))


